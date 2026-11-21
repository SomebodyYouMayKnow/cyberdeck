import adsk.core
import adsk.fusion
import json
import traceback

MM = 10.0  # Fusion internal units are centimeters.
OUTER_DIA_MM = 9.0
SKETCH_NAME = 'PCB Case HoldDown References'
HOLES = [
    ('CASE_TL', 16.0, 16.0),
    ('CASE_TR', 213.55, 17.39),
    ('CASE_BL', 16.0, 116.0),
    ('CASE_BR', 213.55, 116.0),
]
OUT_JSON = (r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering'
            r'\cad\case_inner_mount_rings_audit.json')


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
            raise RuntimeError('The PCB Case HoldDown References sketch was not found.')

        circles = sketch.sketchCurves.sketchCircles
        created = []
        for name, x_mm, y_mm in HOLES:
            matches = []
            for i in range(circles.count):
                c = circles.item(i)
                p = c.geometry.center
                if abs(p.x * MM - x_mm) < 0.001 and abs(p.y * MM - y_mm) < 0.001:
                    matches.append(c)
            if len(matches) != 1:
                raise RuntimeError('{} inner hole reference missing or duplicated.'.format(name))
            inner = matches[0].geometry.radius * 2 * MM
            if abs(inner - 6.2992) > 0.001:
                raise RuntimeError('{} inner hole is {:.4f} mm, expected 6.2992 mm.'.format(name, inner))
            outer_matches = []
            for i in range(circles.count):
                c = circles.item(i)
                p = c.geometry.center
                d = c.geometry.radius * 2 * MM
                if (abs(p.x * MM - x_mm) < 0.001 and abs(p.y * MM - y_mm) < 0.001
                        and abs(d - OUTER_DIA_MM) < 0.001):
                    outer_matches.append(c)
            if not outer_matches:
                center = adsk.core.Point3D.create(x_mm / MM, y_mm / MM, 0)
                circles.addByCenterRadius(center, (OUTER_DIA_MM / 2) / MM)
                created.append(name)
            elif len(outer_matches) > 1:
                raise RuntimeError('{} surrounding circle is duplicated.'.format(name))

        result = []
        for name, x_mm, y_mm in HOLES:
            result.append({'hole': name, 'centerSketchXYMm': [x_mm, y_mm],
                           'pcbClearanceDiameterMm': 6.2992,
                           'supportRingOuterDiameterMm': OUTER_DIA_MM,
                           'radialRingWidthMm': round((OUTER_DIA_MM - 6.2992) / 2, 4)})
        with open(OUT_JSON, 'w') as f:
            json.dump({'fusionDocument': design.parentDocument.name,
                       'sketch': SKETCH_NAME,
                       'purpose': 'Concentric support-ring outlines around the existing PCB inner hold-down hole references; ring profiles can be extruded as raised supports.',
                       'outerDiameterMm': OUTER_DIA_MM,
                       'createdThisRun': created,
                       'holes': result}, f, indent=2)
        ui.messageBox('Added and verified surrounding support circles at all four PCB hold-down holes.\n\nOuter diameter: 9.0 mm\nPCB hole diameter kept clear: 6.2992 mm\nRing profile radial width: 1.3504 mm\n\nThe four annular profiles can be selected and extruded for raised supports.')
    except:
        if ui:
            ui.messageBox('Adding PCB mount rings failed:\n' + traceback.format_exc())


def stop(context):
    pass
