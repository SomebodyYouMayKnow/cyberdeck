import adsk.core
import adsk.fusion
import json
import traceback

MM = 10.0
OUT_JSON = r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering\cad\fusion_screen_mount_audit.json'


def p(x, y):
    return adsk.core.Point3D.create(x / MM, y / MM, 0)


def xy_plane(comp, z_mm):
    inp = comp.constructionPlanes.createInput()
    inp.setByOffset(comp.xYConstructionPlane, adsk.core.ValueInput.createByReal(z_mm / MM))
    return comp.constructionPlanes.add(inp)


def find_lid(comp):
    for i in range(comp.bRepBodies.count):
        body = comp.bRepBodies.item(i)
        if body.name.startswith('Lid shell 238.6 x 138.6'):
            return body
    raise RuntimeError('Current lid shell body was not found; no geometry changed.')


def rectangle(sketch, x0, y0, x1, y1):
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(p(x0, y0), p(x1, y1))


def circle(sketch, x, y, d):
    sketch.sketchCurves.sketchCircles.addByCenterRadius(p(x, y), d / (2 * MM))


def polygon(sketch, points):
    lines = sketch.sketchCurves.sketchLines
    for i, (x0, y0) in enumerate(points):
        x1, y1 = points[(i + 1) % len(points)]
        lines.addByTwoPoints(p(x0, y0), p(x1, y1))


def largest_profile(sketch):
    best = None
    best_area = -1
    for i in range(sketch.profiles.count):
        profile = sketch.profiles.item(i)
        area = profile.areaProperties().area
        if area > best_area:
            best, best_area = profile, area
    return best


def extrude(comp, profile, distance_mm, operation, flip=False, body=None):
    inp = comp.features.extrudeFeatures.createInput(profile, operation)
    inp.setDistanceExtent(False, adsk.core.ValueInput.createByReal(distance_mm / MM))
    inp.isDirectionFlipped = flip
    if body:
        inp.participantBodies = [body]
    return comp.features.extrudeFeatures.add(inp)


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError('No active Fusion design.')
        comp = design.rootComponent
        lid = find_lid(comp)

        for i in range(comp.sketches.count):
            if comp.sketches.item(i).name == 'NEONRED HDMI LCD aperture 76.6 x 51.8 mm':
                ui.messageBox('HDMI screen mount already exists; no duplicate features added.')
                return

        # Use the actual highest horizontal planar face of the live lid shell.
        top_z = None
        largest_area = 0
        for i in range(lid.faces.count):
            face = lid.faces.item(i)
            plane = adsk.core.Plane.cast(face.geometry)
            if not plane:
                continue
            n = plane.normal
            if n.z < 0.999:
                continue
            z = face.pointOnFace.z * MM
            if z > largest_area:
                top_z = z
                largest_area = z
        if top_z is None:
            raise RuntimeError('Could not identify the lid top plane; no features were added.')

        # Legacy CAD and BOM history point to the Waveshare 3.5-inch HDMI LCD, 480x320.
        # Vendor drawing: PCB 85 x 56.5 mm, visible lens area 75.96 x 51.24 mm,
        # maximum thickness 8.3 mm. Display is centered at the existing SCAD datum (16,34).
        sx, sy = 16.0, 34.0
        sw, sh = 85.0, 56.5
        window_w, window_h = 76.6, 51.8
        cx, cy = sx + sw / 2.0, sy + sh / 2.0
        screw_xy = [(13.0, 31.0), (104.0, 31.0), (13.0, 93.5), (104.0, 93.5)]

        aperture = comp.sketches.add(xy_plane(comp, top_z))
        aperture.name = 'NEONRED HDMI LCD aperture 76.6 x 51.8 mm'
        rectangle(aperture, cx - window_w / 2, cy - window_h / 2,
                  cx + window_w / 2, cy + window_h / 2)
        extrude(comp, aperture.profiles.item(0), 2.6,
                adsk.fusion.FeatureOperations.CutFeatureOperation, True, lid)

        # Four M2 clearance bores sit outside the display PCB envelope.
        for i, (x, y) in enumerate(screw_xy):
            hs = comp.sketches.add(xy_plane(comp, top_z))
            hs.name = 'HDMI mount screw clearance {}'.format(i + 1)
            circle(hs, x, y, 2.6)
            extrude(comp, hs.profiles.item(0), 2.6,
                    adsk.fusion.FeatureOperations.CutFeatureOperation, True, lid)

        # Four integral, hollow screw towers extend down to the display board back plane.
        # Their centers are outside the 85 x 56.5 mm module, so they do not collide with it.
        roof_t = 2.4
        module_depth = 8.3
        boss_drop = module_depth - roof_t
        bosses = []
        for i, (x, y) in enumerate(screw_xy):
            bs = comp.sketches.add(xy_plane(comp, top_z - roof_t))
            bs.name = 'HDMI retainer boss annulus {}'.format(i + 1)
            circle(bs, x, y, 7.0)
            circle(bs, x, y, 2.0)
            f = extrude(comp, largest_profile(bs), boss_drop, adsk.fusion.FeatureOperations.NewBodyFeatureOperation, True)
            b = f.bodies.item(0)
            b.name = 'HDMI screen screw boss {}'.format(i + 1)
            bosses.append(b)

        if bosses:
            coll = adsk.core.ObjectCollection.create()
            for b in bosses:
                coll.add(b)
            ci = comp.features.combineFeatures.createInput(lid, coll)
            ci.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
            ci.isKeepToolBodies = False
            comp.features.combineFeatures.add(ci)

        # Four removable corner clips retain the module without drilling its PCB or
        # assuming its factory hole pattern. Each overlaps the board edge by 3-4 mm.
        clip_z = top_z - module_depth
        clip_profiles = [
            ([(10, 28), (28, 28), (28, 37), (19, 37), (19, 46), (10, 46)], screw_xy[0]),
            ([(92, 28), (110, 28), (110, 46), (101, 46), (101, 37), (92, 37)], screw_xy[1]),
            ([(10, 78.5), (19, 78.5), (19, 87.5), (28, 87.5), (28, 105.5), (10, 105.5)], screw_xy[2]),
            ([(92, 87.5), (101, 87.5), (101, 78.5), (110, 78.5), (110, 105.5), (92, 105.5)], screw_xy[3]),
        ]
        clips = []
        for i, (outline, (x, y)) in enumerate(clip_profiles):
            cs = comp.sketches.add(xy_plane(comp, clip_z))
            cs.name = 'HDMI removable corner clip {}'.format(i + 1)
            polygon(cs, outline)
            circle(cs, x, y, 2.6)
            # The profile nearest the outside origin is the clip outline with its screw bore.
            prof = largest_profile(cs)
            if not prof:
                raise RuntimeError('Could not form removable clip {}.'.format(i + 1))
            f = extrude(comp, prof, 1.6, adsk.fusion.FeatureOperations.NewBodyFeatureOperation, True)
            clip = f.bodies.item(0)
            clip.name = 'HDMI screen removable corner clip {}'.format(i + 1)
            clips.append(clip)

        # Report exact geometry dimensions and all placement assumptions.
        data = {
            'units': 'mm', 'displayAssumption': 'Waveshare 3.5-inch HDMI LCD 480x320',
            'displayPcbMm': [sw, sh], 'displayMaxThicknessMm': module_depth,
            'displayOriginMm': [sx, sy], 'viewWindowMm': [window_w, window_h],
            'viewWindowCenterMm': [round(cx, 3), round(cy, 3)],
            'screenMountScrewCentersMm': screw_xy, 'screenMountHoleDiameterMm': 2.6,
            'clipCount': len(clips), 'caseLidTopZmm': round(top_z, 3),
            'caveat': 'Mount uses four printed corner clips, not the LCD PCB screw holes. Confirm connector side, cable bend, actual display revision, and fit with the physical module before final printing.'
        }
        with open(OUT_JSON, 'w') as out:
            json.dump(data, out, indent=2)
        ui.messageBox('Added centered HDMI display aperture, four screw towers and removable corner clips. Assumed Waveshare 3.5-inch HDMI LCD 480x320. Saved audit: ' + OUT_JSON)
    except:
        if ui:
            ui.messageBox('HDMI screen mount failed:\n' + traceback.format_exc())


def stop(context):
    pass
