import adsk.core
import adsk.fusion
import json
import traceback

MM = 10.0  # Fusion's internal length unit is centimeters.
INNER_DIA_MM = 6.2992
OLD_OUTER_DIA_MM = 9.0
NEW_OUTER_DIA_MM = 9.5
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
        changed = []
        for name, x_mm, y_mm in HOLES:
            centered = []
            for i in range(circles.count):
                c = circles.item(i)
                p = c.geometry.center
                if abs(p.x * MM - x_mm) < 0.001 and abs(p.y * MM - y_mm) < 0.001:
                    centered.append(c)
            inner = [c for c in centered if abs(c.geometry.radius * 2 * MM - INNER_DIA_MM) < 0.001]
            if len(inner) != 1:
                raise RuntimeError('{} must have exactly one 6.2992 mm PCB-hole circle; found {}.'.format(name, len(inner)))
            old = [c for c in centered if abs(c.geometry.radius * 2 * MM - OLD_OUTER_DIA_MM) < 0.001]
            new = [c for c in centered if abs(c.geometry.radius * 2 * MM - NEW_OUTER_DIA_MM) < 0.001]
            if len(new) > 1:
                raise RuntimeError('{} has duplicate 9.5 mm support circles.'.format(name))
            for c in old:
                c.deleteMe()
                changed.append(name + ': replaced 9.0 mm circle')
            if not new:
                center = adsk.core.Point3D.create(x_mm / MM, y_mm / MM, 0)
                circles.addByCenterRadius(center, (NEW_OUTER_DIA_MM / 2) / MM)
                changed.append(name + ': added 9.5 mm circle')

        result = []
        for name, x_mm, y_mm in HOLES:
            centered = []
            for i in range(circles.count):
                c = circles.item(i)
                p = c.geometry.center
                if abs(p.x * MM - x_mm) < 0.001 and abs(p.y * MM - y_mm) < 0.001:
                    centered.append(c)
            ids = [c for c in centered if abs(c.geometry.radius * 2 * MM - INNER_DIA_MM) < 0.001]
            ods = [c for c in centered if abs(c.geometry.radius * 2 * MM - NEW_OUTER_DIA_MM) < 0.001]
            if len(ids) != 1 or len(ods) != 1:
                raise RuntimeError('{} ring verification failed.'.format(name))
            result.append({'hole': name, 'centerSketchXYMm': [x_mm, y_mm],
                           'pcbOpeningDiameterMm': INNER_DIA_MM,
                           'supportRingOuterDiameterMm': NEW_OUTER_DIA_MM,
                           'radialRingWidthMm': round((NEW_OUTER_DIA_MM - INNER_DIA_MM) / 2, 4),
                           'nearestPcbEdgeClearanceMm': 0.25 if name in ('CASE_TL', 'CASE_BL') else None})

        with open(OUT_JSON, 'w') as f:
            json.dump({'fusionDocument': design.parentDocument.name,
                       'sketch': SKETCH_NAME,
                       'purpose': 'Four concentric annular profiles around inner PCB hold-down holes; opening matches PCB NPTH and surrounding ring can be extruded as a raised support. Existing lip geometry remains unchanged.',
                       'pcbOpeningDiameterMm': INNER_DIA_MM,
                       'outerDiameterMm': NEW_OUTER_DIA_MM,
                       'radialRingWidthMm': round((NEW_OUTER_DIA_MM - INNER_DIA_MM) / 2, 4),
                       'createdOrReplaced': changed,
                       'holes': result}, f, indent=2)
        ui.messageBox('Updated and verified all four inner support rings.\n\nPCB opening: 6.2992 mm (unchanged)\nOuter diameter: 9.5 mm\nRadial ring thickness: 1.6004 mm\nMinimum edge margin at left holes: 0.25 mm\n\nPerimeter lips were not changed; both lip and ring profiles are ready for your extrusion.')
    except:
        if ui:
            ui.messageBox('Updating inner PCB support rings failed:\n' + traceback.format_exc())


def stop(context):
    pass
