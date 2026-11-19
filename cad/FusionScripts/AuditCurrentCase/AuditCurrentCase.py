import adsk.core
import adsk.fusion
import json
import traceback

MM = 10.0  # Fusion API internal length units are centimeters.
OUT_JSON = r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering\cad\fusion_current_case_audit.json'


def mm(v):
    return round(v * MM, 3)


def vec(p):
    return [mm(p.x), mm(p.y), mm(p.z)]


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError('No active Fusion design.')
        root = design.rootComponent
        bodies = []
        for i in range(root.bRepBodies.count):
            b = root.bRepBodies.item(i)
            box = b.boundingBox
            bodies.append({
                'name': b.name,
                'isVisible': b.isVisible,
                'solid': b.isSolid,
                'minMm': vec(box.minPoint),
                'maxMm': vec(box.maxPoint),
                'sizeMm': [mm(box.maxPoint.x-box.minPoint.x), mm(box.maxPoint.y-box.minPoint.y), mm(box.maxPoint.z-box.minPoint.z)]
            })
        sketches = []
        for i in range(root.sketches.count):
            s = root.sketches.item(i)
            circles = []
            for j in range(s.sketchCurves.sketchCircles.count):
                c = s.sketchCurves.sketchCircles.item(j)
                circles.append({'centerMm': vec(c.geometry.center), 'diameterMm': mm(c.geometry.radius*2), 'construction': c.isConstruction})
            sketches.append({
                'name': s.name,
                'isVisible': s.isVisible,
                'originMm': vec(s.origin),
                'lineCount': s.sketchCurves.sketchLines.count,
                'circleCount': len(circles),
                'arcCount': s.sketchCurves.sketchArcs.count,
                'profileCount': s.profiles.count,
                'circles': circles
            })
        data = {'document': design.parentDocument.name, 'units': 'mm', 'bodies': bodies, 'sketches': sketches}
        with open(OUT_JSON, 'w') as f:
            json.dump(data, f, indent=2)
        ui.messageBox('Read-only case audit saved. Bodies: {}. Sketches: {}.\n{}'.format(len(bodies), len(sketches), OUT_JSON))
    except:
        if ui:
            ui.messageBox('Current case audit failed:\n' + traceback.format_exc())


def stop(context):
    pass
