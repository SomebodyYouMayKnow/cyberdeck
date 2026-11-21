import adsk.core
import adsk.fusion
import json
import traceback

MM = 10.0
OLD_INNER_DIA_MM = 6.2992
OLD_OUTER_DIA_MM = 9.5
INNER_DIA_MM = 3.2
OUTER_DIA_MM = 6.5
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
            raise RuntimeError('PCB Case HoldDown References sketch was not found.')

        circles = sketch.sketchCurves.sketchCircles
        result = []
        for name, x_mm, y_mm in HOLES:
            centered = []
            for i in range(circles.count):
                c = circles.item(i)
                p = c.geometry.center
                if abs(p.x * MM - x_mm) < 0.001 and abs(p.y * MM - y_mm) < 0.001:
                    centered.append(c)
            old_inner = [c for c in centered if abs(c.geometry.radius * 2 * MM - OLD_INNER_DIA_MM) < 0.001]
            old_outer = [c for c in centered if abs(c.geometry.radius * 2 * MM - OLD_OUTER_DIA_MM) < 0.001]
            if len(old_inner) != 1 or len(old_outer) != 1:
                raise RuntimeError('{} expected one old inner (6.2992) and outer (9.5) circle; found {} and {}.'.format(name, len(old_inner), len(old_outer)))
            old_inner[0].deleteMe()
            old_outer[0].deleteMe()
            center = adsk.core.Point3D.create(x_mm / MM, y_mm / MM, 0)
            circles.addByCenterRadius(center, (INNER_DIA_MM / 2) / MM)
            circles.addByCenterRadius(center, (OUTER_DIA_MM / 2) / MM)
            result.append({'hole': name, 'centerSketchXYMm': [x_mm, y_mm],
                           'pcbOpeningDiameterMm': INNER_DIA_MM,
                           'supportRingOuterDiameterMm': OUTER_DIA_MM,
                           'radialRingWidthMm': round((OUTER_DIA_MM - INNER_DIA_MM) / 2, 4)})

        for name, x_mm, y_mm in HOLES:
            found = {'inner': 0, 'outer': 0}
            for i in range(circles.count):
                c = circles.item(i)
                p = c.geometry.center
                d = c.geometry.radius * 2 * MM
                if abs(p.x * MM - x_mm) < 0.001 and abs(p.y * MM - y_mm) < 0.001:
                    if abs(d - INNER_DIA_MM) < 0.001:
                        found['inner'] += 1
                    if abs(d - OUTER_DIA_MM) < 0.001:
                        found['outer'] += 1
            if found != {'inner': 1, 'outer': 1}:
                raise RuntimeError('{} corrected ring verification failed: {}'.format(name, found))

        with open(OUT_JSON, 'w') as f:
            json.dump({'fusionDocument': design.parentDocument.name,
                       'sketch': SKETCH_NAME,
                       'source': 'Live EasyEDA PCB_cyberdeck-completed, Hole Properties verified: CASE_TL inner hole 3.200 mm and case-ear TOP_L hole 3.200 mm.',
                       'purpose': 'Concentric annular support profiles around the four inner case mounting holes; inner opening matches the PCB hole and ring profile is ready for extrusion. Perimeter lips remain unchanged.',
                       'pcbOpeningDiameterMm': INNER_DIA_MM,
                       'supportRingOuterDiameterMm': OUTER_DIA_MM,
                       'radialRingWidthMm': round((OUTER_DIA_MM - INNER_DIA_MM) / 2, 4),
                       'holes': result}, f, indent=2)
        ui.messageBox('Corrected and verified all four internal PCB support rings.\n\nPCB opening: 3.2 mm, matching the live EasyEDA hole\nOuter support circle: 6.5 mm\nRadial ring thickness: 1.65 mm\n\nPerimeter lip geometry was not changed.')
    except:
        if ui:
            ui.messageBox('Correcting inner PCB support rings failed:\n' + traceback.format_exc())


def stop(context):
    pass
