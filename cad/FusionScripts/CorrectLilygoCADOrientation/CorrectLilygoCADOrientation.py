"""Make the LILYGO CAD fit envelope match live EasyEDA A2 orientation and placement."""
import adsk.core
import adsk.fusion
import json
import os
import traceback

MM = 10.0
ROOT_DIR = r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering\cad'
AUDIT = os.path.join(ROOT_DIR, 'fusion_case_fit_and_ports_audit.json')
LILY_BOUNDS = [189.547, 27.267, 34.6, 215.047, 81.083, 44.6]
OLD_LILY_BOUNDS = [160.5, 68.5, 34.6, 218.5, 93.5, 44.6]
OLD_NAME = 'LILYGO T-Display-S3 AMOLED 1.91 - fit-check envelope'
NEW_NAME = 'LILYGO T-Display-S3 AMOLED 1.91 - EasyEDA-aligned portrait envelope'


def point(x, y, z):
    return adsk.core.Point3D.create(x / MM, y / MM, z / MM)


def body_bounds(body):
    b = body.boundingBox
    return [round(b.minPoint.x * MM, 3), round(b.minPoint.y * MM, 3), round(b.minPoint.z * MM, 3),
            round(b.maxPoint.x * MM, 3), round(b.maxPoint.y * MM, 3), round(b.maxPoint.z * MM, 3)]


def find_body(root, name):
    for i in range(root.bRepBodies.count):
        body = root.bRepBodies.item(i)
        if body.name == name:
            return body
    return None


def add_envelope(root):
    x0, y0, z0, x1, y1, z1 = LILY_BOUNDS
    plane_input = root.constructionPlanes.createInput()
    plane_input.setByOffset(root.xYConstructionPlane, adsk.core.ValueInput.createByReal(z0 / MM))
    plane = root.constructionPlanes.add(plane_input)
    sketch = root.sketches.add(plane)
    sketch.name = 'LILYGO A2 live EasyEDA portrait outline 25.5x53.85'
    # Sketch coordinates are local to the offset construction plane, so Z must
    # be zero here. Including z0 would double the plane offset.
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(point(x0, y0, 0), point(x1, y1, 0))
    extrude_input = root.features.extrudeFeatures.createInput(
        sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extrude_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal((z1 - z0) / MM))
    body = root.features.extrudeFeatures.add(extrude_input).bodies.item(0)
    body.name = NEW_NAME
    return body


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError('No active Fusion design; no edits made.')
        root = design.rootComponent
        doc = app.activeDocument

        old = find_body(root, OLD_NAME)
        current = find_body(root, NEW_NAME)
        if old:
            old_bounds = body_bounds(old)
            if max(abs(a-b) for a, b in zip(old_bounds, OLD_LILY_BOUNDS)) > 0.2:
                raise RuntimeError('Old LILYGO envelope differs from expected bounds: {}. No edits made.'.format(old_bounds))
        else:
            old_bounds = OLD_LILY_BOUNDS

        if current:
            current_bounds = body_bounds(current)
            if max(abs(a-b) for a, b in zip(current_bounds, LILY_BOUNDS)) > 0.05:
                # Remove only the known first-run mistake: correct XY and an
                # exact duplicate +34.6 mm Z offset caused by the old script.
                expected_bad = [LILY_BOUNDS[0], LILY_BOUNDS[1], 69.2,
                                LILY_BOUNDS[3], LILY_BOUNDS[4], 79.2]
                if max(abs(a-b) for a, b in zip(current_bounds, expected_bad)) > 0.05:
                    raise RuntimeError('Existing named LILYGO body is not the known temporary script output: {}. No edits made.'.format(current_bounds))
                current.deleteMe()
                current = None
        if not current:
            current = add_envelope(root)
            final_bounds = body_bounds(current)
        else:
            final_bounds = body_bounds(current)
        if max(abs(a-b) for a, b in zip(final_bounds, LILY_BOUNDS)) > 0.05:
            raise RuntimeError('New portrait envelope bounds mismatch: {}.'.format(final_bounds))

        chameleon = next((root.bRepBodies.item(i) for i in range(root.bRepBodies.count)
                          if root.bRepBodies.item(i).name.startswith('Chameleon Ultra SE3')), None)
        encoder = next((root.bRepBodies.item(i) for i in range(root.bRepBodies.count)
                        if root.bRepBodies.item(i).name.startswith('Rotary encoder -')), None)

        def gap_y(a, b):
            aa, bb = body_bounds(a), body_bounds(b)
            return round(max(bb[1]-aa[4], aa[1]-bb[4], 0), 3)

        def gap_x(a, b):
            aa, bb = body_bounds(a), body_bounds(b)
            return round(max(bb[0]-aa[3], aa[0]-bb[3], 0), 3)

        chameleon_gap = gap_y(current, chameleon) if chameleon else None
        encoder_gap = gap_x(current, encoder) if encoder else None
        if chameleon_gap is not None and chameleon_gap < 1.0:
            raise RuntimeError('Portrait LILYGO/Chameleon Y clearance is only {} mm.'.format(chameleon_gap))
        if encoder_gap is not None and encoder_gap < 1.0:
            raise RuntimeError('Portrait LILYGO/encoder X clearance is only {} mm.'.format(encoder_gap))

        if old and old != current:
            old.deleteMe()

        audit = {}
        with open(AUDIT, 'r') as f:
            audit = json.load(f)
        audit['lilygoEasyEDAAlignment'] = {
            'project': 'cyberdeck-completed / PCB_cyberdeck-completed',
            'prefix': 'A2', 'rotationDegrees': 0,
            'easyedaAnchorMm': [185.547, 29.083],
            'easyedaOutlineRaw': [4750.5, 3205.0, 4850.894, 3417.008],
            'boardOutlineMmEasyEDA': {'x': [-1.0, 225.0], 'y': [-49.0, 77.0]},
            'fusionBoardBoundsMm': {'x': [3.0, 229.0], 'y': [3.0, 129.0]},
            'caseDatumTranslationMm': [4.0, 52.0],
            'fusionBodyBoundsMm': final_bounds,
            'bodyFootprintMm': [25.5, 53.85],
            'bodyHeightEstimateMm': 10.0,
            'clearanceToChameleonMm': chameleon_gap,
            'clearanceToRotaryEncoderMm': encoder_gap,
            'oldWrongLandscapeEnvelopeRemoved': old_bounds,
            'lidScreenWindow': 'Unchanged in this correction; its location must be compared with the actual A2 panel revision before final lid printing.'
        }
        existing = audit.get('componentFitEnvelopes', {})
        existing['LilyGoTDisplayS3Amoled'] = {
            'dimensionsMm': [25.5, 53.85, 10.0],
            'boundsMm': final_bounds,
            'rotationDegrees': 0,
            'orientationSource': 'A2 footprint outline from the live EasyEDA PCB; 10 mm height is a fit estimate.',
            'source': 'EasyEDA cyberdeck-completed / PCB_cyberdeck-completed, component A2'
        }
        audit['componentFitEnvelopes'] = existing
        with open(AUDIT, 'w') as f:
            json.dump(audit, f, indent=2)

        app.activeViewport.fit()
        doc.save('Correct LILYGO portrait fit envelope to live EasyEDA A2 placement')
        ui.messageBox('LILYGO fit-check corrected to the live EasyEDA A2 footprint: portrait, rotation 0, 25.5 x 53.85 mm, located at the PCB-mapped case coordinates. The previous landscape fit body was removed. The EasyEDA PCB and its placement were not changed. The LILYGO lid opening was left untouched because its lid component is hinged and rotated in this assembly.')
    except:
        if ui:
            ui.messageBox('LILYGO CAD correction stopped. Review the Fusion timeline before retrying.\n\n' + traceback.format_exc())


def stop(context):
    pass
