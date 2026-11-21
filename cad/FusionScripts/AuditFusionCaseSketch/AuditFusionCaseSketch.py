import adsk.core
import adsk.fusion
import json
import traceback

MM = 10.0
SKETCH_NAME = 'Sketch1'
OUT_JSON = (r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering'
            r'\cad\fusion_sketch_geometry_audit.json')


def pt(p):
    return [round(p.x * MM, 4), round(p.y * MM, 4)]


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError('No active Fusion design.')
        root = design.rootComponent
        sketch = None
        for i in range(root.sketches.count):
            candidate = root.sketches.item(i)
            if candidate.name == SKETCH_NAME:
                sketch = candidate
                break
        if not sketch:
            raise RuntimeError('Sketch1 was not found in the active design.')

        circles = []
        cs = sketch.sketchCurves.sketchCircles
        for i in range(cs.count):
            c = cs.item(i)
            circles.append({'centerMm': pt(c.geometry.center),
                            'diameterMm': round(c.geometry.radius * 2 * MM, 4),
                            'construction': c.isConstruction})
        lines = []
        ls = sketch.sketchCurves.sketchLines
        for i in range(ls.count):
            line = ls.item(i)
            g = line.geometry
            lines.append({'startMm': pt(g.startPoint), 'endMm': pt(g.endPoint),
                          'construction': line.isConstruction})
        arcs = []
        ars = sketch.sketchCurves.sketchArcs
        for i in range(ars.count):
            a = ars.item(i)
            g = a.geometry
            arcs.append({'centerMm': pt(g.center), 'radiusMm': round(g.radius * MM, 4),
                         'startMm': pt(g.startPoint), 'endMm': pt(g.endPoint),
                         'construction': a.isConstruction})
        data = {'fusionDocument': design.parentDocument.name,
                'sketch': sketch.name,
                'units': 'mm',
                'sketchDimensions': {'lines': len(lines), 'circles': len(circles), 'arcs': len(arcs)},
                'circles': circles, 'lines': lines, 'arcs': arcs}
        with open(OUT_JSON, 'w') as f:
            json.dump(data, f, indent=2)
        ui.messageBox('Read-only Sketch1 geometry audit complete.\n\nLines: {}\nCircles: {}\nArcs: {}\n\nAudit file: {}'.format(len(lines), len(circles), len(arcs), OUT_JSON))
    except:
        if ui:
            ui.messageBox('Fusion sketch audit failed:\n' + traceback.format_exc())


def stop(context):
    pass
