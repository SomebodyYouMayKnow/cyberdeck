import adsk.core
import adsk.fusion
import json
import traceback


MM = 10.0  # Fusion's internal length unit is centimeters.
HOLE_DIA_MM = 6.2992  # Measured NPTH diameter from the dated EasyEDA PCB export.
SKETCH_NAME = 'PCB Case HoldDown References'

# EasyEDA PCB CASE_TL/TR/BL/BR holes transformed to the Fusion case sketch:
# the PCB's 210 x 110 mm base is aligned to the 210 x 110 mm inner rectangle.
HOLES = [
    ('CASE_TL', 16.0, 16.0, 5.0, 5.0),
    ('CASE_TR', 213.55, 17.39, 202.55, 6.39),
    ('CASE_BL', 16.0, 116.0, 5.0, 105.0),
    ('CASE_BR', 213.55, 116.0, 202.55, 105.0),
]

OUT_JSON = (r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering'
            r'\cad\case_inner_mount_reference_audit.json')


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError('No active Fusion design.')
        root = design.rootComponent
        sketch = next((root.sketches.item(i) for i in range(root.sketches.count)
                       if root.sketches.item(i).name == SKETCH_NAME), None)
        if sketch is None:
            sketch = root.sketches.add(root.xYConstructionPlane)
            sketch.name = SKETCH_NAME
            for _, x_mm, y_mm, _, _ in HOLES:
                center = adsk.core.Point3D.create(x_mm / MM, y_mm / MM, 0)
                sketch.sketchCurves.sketchCircles.addByCenterRadius(
                    center, (HOLE_DIA_MM / 2) / MM)
        else:
            if sketch.sketchCurves.sketchCircles.count != len(HOLES):
                raise RuntimeError('Existing reference sketch has an unexpected circle count.')

        result = []
        circles = sketch.sketchCurves.sketchCircles
        for name, x_mm, y_mm, base_x, base_y in HOLES:
            found = []
            for i in range(circles.count):
                c = circles.item(i)
                p = c.geometry.center
                if abs(p.x * MM - x_mm) < 0.001 and abs(p.y * MM - y_mm) < 0.001:
                    found.append(c)
            if len(found) != 1:
                raise RuntimeError('{} reference is missing or duplicated.'.format(name))
            actual_d = found[0].geometry.radius * 2 * MM
            if abs(actual_d - HOLE_DIA_MM) > 0.001:
                raise RuntimeError('{} diameter is {:.4f} mm, expected {:.4f} mm.'.format(name, actual_d, HOLE_DIA_MM))
            result.append({'hole': name, 'diameterMm': round(actual_d, 4),
                           'caseSketchXYMm': [x_mm, y_mm],
                           'fromPcbBaseBottomLeftMm': [base_x, base_y]})

        audit = {
            'fusionDocument': design.parentDocument.name,
            'referenceSketch': SKETCH_NAME,
            'pcbSource': 'EasyEDA/NEONRED_PCB_2026-10-19.json',
            'holeType': 'Existing PCB NPTH CASE mounting holes, represented as reference circles for case support placement',
            'pcbHoleDiameterMm': HOLE_DIA_MM,
            'pcbMainBodySizeMm': [210, 110],
            'fusionBaseRectangleSizeMm': [210, 110],
            'mapping': 'PCB main-body origin at board-local (8, 8) mm maps to Fusion inner-rectangle origin (11, 11) mm.',
            'holes': result,
        }
        with open(OUT_JSON, 'w') as f:
            json.dump(audit, f, indent=2)
        ui.messageBox('Added and verified the four internal PCB hold-down locations in a separate reference sketch.\n\nPCB clearance-hole diameter: 6.2992 mm\nThey align with CASE_TL/TR/BL/BR from the EasyEDA export.\n\nAudit: ' + OUT_JSON)
    except:
        if ui:
            ui.messageBox('Inner PCB mounting-reference script failed:\n' + traceback.format_exc())


def stop(context):
    pass
