"""Cut display apertures through the actual lid roof and seat the LCD inside it."""
import adsk.core
import adsk.fusion
import json
import traceback

MM = 10.0
ROOT = r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering\cad'
AUDIT = ROOT + r'\fusion_screen_mount_audit.json'

def point(x, y, z):
    return adsk.core.Point3D.create(x / MM, y / MM, z / MM)

def plane_at_z(comp, z_mm):
    pi = comp.constructionPlanes.createInput()
    pi.setByOffset(comp.xYConstructionPlane, adsk.core.ValueInput.createByReal(z_mm / MM))
    return comp.constructionPlanes.add(pi)

def rect(sketch, x0, y0, x1, y1):
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(point(x0, y0, sketch.offset),
                                                        point(x1, y1, sketch.offset))

def cut_rect(comp, lid, name, bounds, sketch_z):
    sk = comp.sketches.add(plane_at_z(comp, sketch_z))
    sk.name = name
    x0, y0, x1, y1 = bounds
    sk.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(x0 / MM, y0 / MM, 0),
        adsk.core.Point3D.create(x1 / MM, y1 / MM, 0))
    ex = comp.features.extrudeFeatures.createInput(sk.profiles.item(0),
                         adsk.fusion.FeatureOperations.CutFeatureOperation)
    ex.participantBodies = [lid]
    ex.setDistanceExtent(True, adsk.core.ValueInput.createByReal(0.5))
    comp.features.extrudeFeatures.add(ex)

def body_bbox(body):
    b = body.boundingBox
    return [b.minPoint.x*MM, b.minPoint.y*MM, b.minPoint.z*MM,
            b.maxPoint.x*MM, b.maxPoint.y*MM, b.maxPoint.z*MM]

def shift_body(body, dz_mm):
    m = adsk.core.Matrix3D.create()
    m.translation = adsk.core.Vector3D.create(0, 0, dz_mm / MM)
    entities = adsk.core.ObjectCollection.create()
    entities.add(body)
    move_input = body.parentComponent.features.moveFeatures.createInput2(entities)
    move_input.defineAsFreeMove(m)
    body.parentComponent.features.moveFeatures.add(move_input)

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError('No active Fusion design.')
        root = design.rootComponent
        document = app.activeDocument
        if any(root.sketches.item(i).name == 'Through-slot above LILYGO ESP32 AMOLED'
               for i in range(root.sketches.count)):
            raise RuntimeError('An earlier LILYGO slot already exists at the old landscape location. This script will not add a second hole; reposition/delete the old cut in Fusion first, then rerun only after checking the closed-lid transform.')
        lid = next((root.bRepBodies.item(i) for i in range(root.bRepBodies.count)
                    if root.bRepBodies.item(i).name.startswith('Lid shell 238.6 x 138.6')),
                   None)
        if not lid:
            raise RuntimeError('Lid shell not found. No geometry changed.')

        # The inspected lid roof is the broad upward planar face at Z=52.4 mm;
        # its inside face is Z=50.0 mm. Earlier cuts started above the roof.
        roof_z = 52.4
        planar_roof_found = False
        for i in range(lid.faces.count):
            f = lid.faces.item(i)
            pl = adsk.core.Plane.cast(f.geometry)
            if pl and abs(pl.normal.z) > 0.99 and abs(pl.origin.z*MM - roof_z) < 0.05 and f.area*100 > 30000:
                planar_roof_found = True
                break
        if not planar_roof_found:
            raise RuntimeError('Expected lid roof face at Z=52.4 mm was not found. No geometry changed.')

        # Remove only the erroneous floating patch created by the earlier bad
        # Z datum; it is not joined to the lid and is identified by its exact box.
        for i in range(root.bRepBodies.count - 1, -1, -1):
            b = root.bRepBodies.item(i)
            bb = body_bbox(b)
            if (b.name == 'Body31' and abs(bb[0]-163.7)<0.1 and abs(bb[1]-37.7)<0.1
                    and abs(bb[2]-53.6)<0.1 and abs(bb[3]-187.3)<0.1
                    and abs(bb[4]-85.3)<0.1 and abs(bb[5]-56.0)<0.1):
                b.deleteMe()

        # Seat the Waveshare module inward: fit envelope z=42..50, panel/glass
        # reference z=50..52.4, retaining frame z=46..50.
        for i in range(root.bRepBodies.count):
            b = root.bRepBodies.item(i)
            bb = body_bbox(b)
            if b.name.startswith('Waveshare 7-inch LCD C fit-check board'):
                if abs(bb[2]-45.6)<0.1 and abs(bb[5]-53.6)<0.1:
                    shift_body(b, -3.6)
            elif b.name.startswith('Waveshare 7-inch LCD C active panel reference'):
                if abs(bb[2]-53.6)<0.1 and abs(bb[5]-56.0)<0.1:
                    shift_body(b, -3.6)
            elif b.name.startswith('Waveshare 7-inch LCD C retainer frame'):
                if abs(bb[2]-49.6)<0.1 and abs(bb[5]-53.6)<0.1:
                    shift_body(b, -3.6)

        # The 7-inch LCD's active area and the separate ESP32 status screen are
        # distinct openings. The LILYGO aperture is a centered 23 x 47 mm
        # estimate over the current portrait A2 board envelope. Its actual
        # active-area offset should be confirmed from the exact board revision.
        # Use a mid-roof construction plane and a symmetric cut to avoid the
        # previous outward-face sketch that left the lid uncut.
        cut_z = 51.2
        cut_rect(root, lid, 'Through-cut Waveshare 7-inch LCD active window',
                 (2.545, 25.04, 156.755, 110.96), cut_z)
        lily_bounds = (190.797, 30.675, 213.797, 77.675)
        cut_rect(root, lid, 'Through-slot above LILYGO ESP32 AMOLED', lily_bounds, cut_z)

        roof_area = 0.0
        for i in range(lid.faces.count):
            f = lid.faces.item(i)
            pl = adsk.core.Plane.cast(f.geometry)
            if pl and pl.normal.z > 0.99 and abs(pl.origin.z * MM - roof_z) < 0.05:
                roof_area += f.area * MM * MM
        expected_roof_area = 32910.96 - (154.21 * 85.92) - (23.0 * 47.0)
        if abs(roof_area - expected_roof_area) > 1.0:
            raise RuntimeError('Cut verification failed: remaining outer lid planar area is {:.2f} mm2; expected about {:.2f} mm2. The openings are not verified.'.format(roof_area, expected_roof_area))

        audit = {}
        try:
            with open(AUDIT, 'r') as f:
                audit = json.load(f)
        except Exception:
            pass
        audit.update({
            'liveLidRoofMm': {'outerFaceZ': 52.4, 'innerFaceZ': 50.0, 'thickness': 2.4},
            'lcdMountedInsideLid': True,
            'lcdActiveAreaThroughCutBoundsMm': [2.545, 25.04, 156.755, 110.96],
            'lilygoBoardEnvelopeCaseMm': [189.547, 27.267, 215.047, 81.083],
            'lilygoAmoledWindowMm': [23.0, 47.0],
            'lilygoAmoledWindowBoundsMm': list(lily_bounds),
            'lilygoWindow': 'Through-cut in the actual lid roof above the planned ESP32/LILYGO board position; separate from the 7-inch LCD opening.',
            'screenMounting': 'Waveshare fit envelope is inside the lid cavity; active panel reference is flush with the outer roof face; retainer is below the board.',
            'verifiedLidTopPlanarAreaMm2': round(roof_area, 3),
            'expectedLidTopPlanarAreaMm2': round(expected_roof_area, 3),
            'lilygoWindowFitCaveat': 'Window is centered on the 25.5 x 53.85 mm portrait A2 board envelope at rotation 0. The 23 x 47 mm opening is an estimate because the active-area offset is not present in the EasyEDA footprint. Verify against the exact LILYGO DWG before printing.'
        })
        with open(AUDIT, 'w') as f:
            json.dump(audit, f, indent=2)
        app.activeViewport.fit()
        document.save('Cut separate ESP32 slot and seat HDMI display inside lid')
        ui.messageBox('Cut the 7-inch LCD aperture and a separate 23 x 47 mm LILYGO slot through the actual Z=52.4 mm lid roof. Seated the HDMI fit-check inside the lid and removed the misplaced floating patch. The lid and PCB positions were not moved.')
    except:
        if ui:
            ui.messageBox('Lid correction stopped. Review before retrying.\n\n' + traceback.format_exc())

def stop(context):
    pass
