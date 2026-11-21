"""Repair the open-lid LILYGO aperture and increase bank/HAT clearance.

The current document has an interrupted prior attempt: the patch sketch was
created and contains the correct 23 x 47 mm profile, but that attempt stopped
because the face sketch also contained projected profiles. This version picks
the exact area profile instead of assuming one profile per sketch.
"""
import adsk.core
import adsk.fusion
import json
import itertools
import math
import os
import traceback

MM = 10.0  # Fusion internal units are cm.
ROOT_DIR = r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering'
AUDIT = os.path.join(ROOT_DIR, 'cad', 'fusion_current_case_audit.json')
PATCH_NAME = 'LILYGO lid window correction patch old opening'
SLOT_NAME = 'LILYGO lid window corrected over A2 portrait board'
CUT_OLD_RAILS = 'Cut old INIU retention rails for HAT clearance'
NEW_RAILS = 'INIU retention rails after HAT clearance adjustment'


def mm_point(x, y, z=0):
    return adsk.core.Point3D.create(x/MM, y/MM, z/MM)


def bounds(body):
    b = body.boundingBox
    return [round(b.minPoint.x*MM, 3), round(b.minPoint.y*MM, 3), round(b.minPoint.z*MM, 3),
            round(b.maxPoint.x*MM, 3), round(b.maxPoint.y*MM, 3), round(b.maxPoint.z*MM, 3)]


def find_body(comp, name):
    for i in range(comp.bRepBodies.count):
        body = comp.bRepBodies.item(i)
        if body.name == name:
            return body
    return None


def find_sketch(comp, name):
    for i in range(comp.sketches.count):
        sketch = comp.sketches.item(i)
        if sketch.name == name:
            return sketch
    return None


def area_mm2(profile):
    return profile.areaProperties().area * MM * MM


def profile_by_area(sketch, target, tol=0.25):
    matches = []
    for i in range(sketch.profiles.count):
        p = sketch.profiles.item(i)
        a = area_mm2(p)
        if abs(a-target) <= tol:
            matches.append((abs(a-target), p))
    if len(matches) != 1:
        profile_areas = [round(area_mm2(sketch.profiles.item(i)), 3)
                         for i in range(sketch.profiles.count)]
        profile_stats = []
        for i in range(sketch.profiles.count):
            props = sketch.profiles.item(i).areaProperties()
            c = props.centroid
            profile_stats.append((round(props.area*MM*MM,3),
                                  [round(c.x*MM,3),round(c.y*MM,3),round(c.z*MM,3)]))
        line_data = []
        for i in range(min(sketch.sketchCurves.sketchLines.count, 4)):
            line = sketch.sketchCurves.sketchLines.item(i)
            a = line.startSketchPoint.geometry
            b = line.endSketchPoint.geometry
            line_data.append('({:.4f},{:.4f})->({:.4f},{:.4f})'.format(a.x*MM, a.y*MM, b.x*MM, b.y*MM))
        raise RuntimeError('{}: expected one {:.1f} mm2 profile; found {}.'.format(
            sketch.name, target, len(matches)) + ' areas={}, profiles={}, lines={}'.format(
            profile_areas, sketch.profiles.count, '; '.join(line_data)) + ' stats={}'.format(profile_stats))
    return matches[0][1]


def profile_set_by_area_centroid(sketch, target, expected_xy, area_tol=0.5, pos_tol=1.0):
    # Face edges projected into a Fusion sketch can split one intended
    # rectangle into adjacent profiles. Select the set that tiles the desired
    # aperture by total area and centroid, rather than cutting just one piece.
    profiles = [sketch.profiles.item(i) for i in range(sketch.profiles.count)]
    candidates = []
    for n in range(1, len(profiles)+1):
        for subset in itertools.combinations(profiles, n):
            weighted_x = weighted_y = total = 0.0
            for p in subset:
                props = p.areaProperties()
                area = props.area * MM * MM
                weighted_x += props.centroid.x * MM * area
                weighted_y += props.centroid.y * MM * area
                total += area
            if abs(total-target) > area_tol:
                continue
            cx, cy = weighted_x/total, weighted_y/total
            dist = math.hypot(cx-expected_xy[0], cy-expected_xy[1])
            if dist <= pos_tol:
                candidates.append((dist, subset, total, cx, cy))
    if len(candidates) != 1:
        raise RuntimeError('{}: expected one profile set totaling {:.1f} mm2 near {}; found {}.'.format(
            sketch.name, target, expected_xy,
            [(round(c[2],3),round(c[3],3),round(c[4],3),len(c[1])) for c in candidates]))
    return candidates[0][1]


def make_transform():
    matrix = adsk.core.Matrix3D.create()
    ok = matrix.setToRotation(math.radians(-110),
                              adsk.core.Vector3D.create(1, 0, 0),
                              mm_point(0, 139.3, 50.0))
    if not ok:
        raise RuntimeError('Could not reconstruct the documented 110-degree lid pose.')
    return matrix


def outer_lid_face(lid):
    target = (0.0, 0.93969262, -0.34202014)
    candidates = []
    for i in range(lid.faces.count):
        face = lid.faces.item(i)
        plane = adsk.core.Plane.cast(face.geometry)
        if not plane or face.area*MM*MM < 10000:
            continue
        dot = plane.normal.x*target[0] + plane.normal.y*target[1] + plane.normal.z*target[2]
        if dot < 0.995:
            continue
        level = (plane.origin.x*target[0] + plane.origin.y*target[1] + plane.origin.z*target[2]) * MM
        candidates.append((level, face))
    if len(candidates) < 2:
        raise RuntimeError('Could not identify both broad parallel lid roof faces.')
    candidates.sort(key=lambda item: item[0])
    gap = (candidates[-1][0]-candidates[0][0])
    if abs(gap-2.4) > 0.5:
        raise RuntimeError('The broad lid faces are separated by {:.3f} mm, expected 2.4 mm.'.format(gap))
    # The broad outward face is the one with the greatest signed distance in
    # its own outward normal direction.  A sketch on it keeps the slot datum
    # coincident with the actual exterior surface of the rotated lid.
    return candidates[-1][1]


def sketch_normal_flip(sketch):
    coordinate_system = sketch.transform.getAsCoordinateSystem()
    z_axis = coordinate_system[3]
    alignment = z_axis.y*0.93969262 + z_axis.z*(-0.34202014)
    return alignment < 0


def add_transformed_rectangle(sketch, bounds_xy, z_mm, matrix):
    x0, y0, x1, y1 = bounds_xy
    # Map all four corners. Two diagonal corners passed to
    # addTwoPointRectangle are not sufficient on a rotated sketch plane:
    # Fusion makes that rectangle axis-aligned in sketch coordinates, which
    # can collapse or distort the intended 23 x 47 mm loop.
    corners = [(x0,y0), (x1,y0), (x1,y1), (x0,y1)]
    pts = []
    for x, y in corners:
        p = mm_point(x, y, z_mm)
        p.transformBy(matrix)
        q = sketch.modelToSketchSpace(p)
        pts.append(adsk.core.Point3D.create(q.x, q.y, 0))
    lines = sketch.sketchCurves.sketchLines
    for i in range(4):
        lines.addByTwoPoints(pts[i], pts[(i+1) % 4])


def add_rect(sketch, x0, y0, x1, y1):
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(x0/MM, y0/MM, 0),
        adsk.core.Point3D.create(x1/MM, y1/MM, 0))


def make_extrude(comp, sketch, profile, body, operation, distance_mm, flipped=False):
    entity = profile
    if isinstance(profile, (list, tuple)):
        entity = adsk.core.ObjectCollection.create()
        for p in profile:
            entity.add(p)
    inp = comp.features.extrudeFeatures.createInput(entity, operation)
    if body:
        inp.participantBodies = [body]
    inp.setDistanceExtent(False, adsk.core.ValueInput.createByReal(distance_mm/MM))
    inp.isDirectionFlipped = flipped
    return comp.features.extrudeFeatures.add(inp)


def run(context):
    ui = None
    created_sketches = []
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError('No active Fusion design.')
        root = design.rootComponent
        doc = app.activeDocument
        case = find_body(root, 'Body1')
        lid = next((root.bRepBodies.item(i) for i in range(root.bRepBodies.count)
                    if root.bRepBodies.item(i).name.startswith('Lid shell 238.6 x 138.6')), None)
        bank = find_body(root, 'INIU BI-B5 power bank relocated clear of Pi/HAT - fit-check envelope')
        hat = find_body(root, 'Pi Zero 2 W + Waveshare USB Hub HAT underside stack - fit-check envelope')
        if not all((case, lid, bank, hat)):
            raise RuntimeError('Missing case, lid, bank, or Pi/HAT fit-check bodies. Nothing was changed.')
        bank_bounds = bounds(bank)
        hat_bounds = bounds(hat)
        if max(abs(a-b) for a,b in zip(bank_bounds, [49,56.5,0.5,183,127.5,26])) > 0.4:
            raise RuntimeError('Bank bounds no longer match the audited position: {}. Nothing was changed.'.format(bank_bounds))
        if max(abs(a-b) for a,b in zip(hat_bounds, [29.5,25,19,94.5,55,33])) > 0.4:
            raise RuntimeError('Pi/HAT bounds no longer match the audited position: {}. Nothing was changed.'.format(hat_bounds))
        if find_sketch(root, SLOT_NAME) or find_sketch(root, CUT_OLD_RAILS) or find_sketch(root, NEW_RAILS):
            raise RuntimeError('One or more correction features already exist. Nothing was changed.')

        patch_sketch = find_sketch(root, PATCH_NAME)
        if not patch_sketch:
            raise RuntimeError('The prior correction patch sketch is missing; cannot verify the old slot repair.')

        matrix = make_transform()
        board = [189.547, 27.267, 215.047, 81.083]
        cx = (board[0]+board[2])/2.0
        cy = (board[1]+board[3])/2.0
        new_window = [cx-11.5, cy-23.5, cx+11.5, cy+23.5]

        # Preflight the battery rail edits before changing any solids.
        old_rail_rects = [
            (49,53.5,108,55.5), (124,53.5,183,55.5),
            (49,128.5,183,130.5),
            (46.5,56.5,48.5,87.0), (46.5,101.5,48.5,127.5),
            (183.5,56.5,185.5,87.0), (183.5,101.5,185.5,127.5)
        ]
        old_cut_sk = root.sketches.add(root.xYConstructionPlane)
        created_sketches.append(old_cut_sk)
        old_cut_sk.name = CUT_OLD_RAILS
        offset_input = root.constructionPlanes.createInput()
        offset_input.setByOffset(root.xYConstructionPlane, adsk.core.ValueInput.createByReal(-2.0/MM))
        rail_plane = root.constructionPlanes.add(offset_input)
        new_rail_sk = root.sketches.add(rail_plane)
        created_sketches.append(new_rail_sk)
        new_rail_sk.name = NEW_RAILS
        for r in old_rail_rects:
            add_rect(old_cut_sk, *r)
            add_rect(new_rail_sk, r[0], r[1]+2.5, r[2], r[3]+2.5)
        if old_cut_sk.profiles.count != 7 or new_rail_sk.profiles.count != 7:
            raise RuntimeError('Rail sketch preflight expected 7 separated profiles (got {} and {}). Nothing was changed.'.format(
                old_cut_sk.profiles.count, new_rail_sk.profiles.count))

        # The previous attempt already joined a plug over the misplaced hole.
        # Verify that the patch sketch still contains the 23 x 47 mm profile,
        # then cut the new window on the exterior roof face. The z datum is the
        # 52.4 mm outer roof surface in the lid's closed pose before its hinge
        # transform. A z=50.0 point is 2.4 mm off this face and produced an
        # open, zero-area sketch in the previous run.
        profile_by_area(patch_sketch, 23.0*47.0)
        face = outer_lid_face(lid)
        slot = root.sketches.add(face)
        created_sketches.append(slot)
        slot.name = SLOT_NAME
        add_transformed_rectangle(slot, new_window, 52.4, matrix)
        center = mm_point(cx, cy, 52.4)
        center.transformBy(matrix)
        center_sketch = slot.modelToSketchSpace(center)
        slot_profiles = profile_set_by_area_centroid(
            slot, 23.0*47.0, (center_sketch.x*MM, center_sketch.y*MM))
        make_extrude(root, slot, slot_profiles, lid,
                     adsk.fusion.FeatureOperations.CutFeatureOperation, 3.0, True)
        slot.isVisible = False
        patch_sketch.isVisible = False

        for i in range(old_cut_sk.profiles.count):
            make_extrude(root, old_cut_sk, old_cut_sk.profiles.item(i), case,
                         adsk.fusion.FeatureOperations.CutFeatureOperation, 6.5)
        for i in range(new_rail_sk.profiles.count):
            make_extrude(root, new_rail_sk, new_rail_sk.profiles.item(i), case,
                         adsk.fusion.FeatureOperations.JoinFeatureOperation, 8.5)
        old_cut_sk.isVisible = False
        new_rail_sk.isVisible = False

        move = adsk.core.Matrix3D.create()
        move.translation = adsk.core.Vector3D.create(0, 2.5/MM, 0)
        entities = adsk.core.ObjectCollection.create()
        entities.add(bank)
        move_in = root.features.moveFeatures.createInput2(entities)
        move_in.defineAsFreeMove(move)
        root.features.moveFeatures.add(move_in)
        bank.name = 'INIU BI-B5 power bank shifted for 4 mm HAT clearance - fit-check envelope'

        moved = bounds(bank)
        y_gap = round(moved[1]-hat_bounds[4], 3)
        rear_wall_gap = round(131.7-moved[4], 3)
        if y_gap < 3.9 or rear_wall_gap < 1.5:
            raise RuntimeError('Post-move fit check failed: HAT gap {} mm, cavity rear gap {} mm.'.format(y_gap, rear_wall_gap))

        audit = {}
        try:
            with open(AUDIT, 'r') as f:
                audit = json.load(f)
        except Exception:
            pass
        audit['lilygoWindowCorrection'] = {
            'status': 'old misplaced 23 x 47 mm opening patched; new 23 x 47 mm opening cut through the actual open-lid roof',
            'oldClosedCaseBoundsMm': [170.25,54.5,193.25,101.5],
            'newClosedCaseBoundsMm': [round(v,3) for v in new_window],
            'boardEnvelopeMm': board,
            'displayWindowEstimate': '23 x 47 mm centered on the A2 portrait board outline; confirm active-area offset against the exact LILYGO revision.'
        }
        audit.setdefault('piAndHubHatUnderside', {})['batteryBoundsMm'] = moved
        audit['piAndHubHatUnderside']['separationMm'] = {'y': y_gap, 'batteryToRearCavityWall': rear_wall_gap}
        audit['piAndHubHatUnderside']['overlapStatus'] = 'No nominal intersection in the simplified envelopes. HAT-to-bank edge clearance is {:.1f} mm; bank-to-rear-cavity clearance is {:.1f} mm. Actual HAT connector height and bank casing tolerance remain to be measured.'.format(y_gap, rear_wall_gap)
        audit['powerBank'] = {
            'model': 'INIU BI-B5 20000 mAh', 'nominalSizeMm': [134,71,25.5],
            'boundsMm': moved, 'placement': 'Shifted 2.5 mm toward the rear with the retention rails moved to match.'
        }
        with open(AUDIT, 'w') as f:
            json.dump(audit, f, indent=2)
        app.activeViewport.fit()
        doc.save('Corrected LILYGO window and improved Pi-HAT battery clearance')
        ui.messageBox('Correction saved. Replaced the misplaced LILYGO opening with a centered 23 x 47 mm aperture. Pi/HAT-to-bank edge gap is {:.1f} mm; bank-to-rear-wall gap is {:.1f} mm. Check against physical module revisions before printing.'.format(y_gap, rear_wall_gap))
    except:
        # Remove any validation-only sketches if preflight did not complete.
        try:
            for sketch in reversed(created_sketches):
                if sketch and sketch.isValid:
                    sketch.deleteMe()
        except:
            pass
        if ui:
            ui.messageBox('Fit correction stopped. No component bodies were deliberately moved before preflight completed.\n\n' + traceback.format_exc())


def stop(context):
    pass
