import adsk.core
import adsk.fusion
import json
import traceback

MM = 10.0
SKETCH_NAME = 'PCB Case HoldDown References'
OUT_JSON = (r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering'
            r'\cad\fusion_mount_sketch_audit.json')


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
        if not sketch:
            raise RuntimeError('PCB Case HoldDown References sketch was not found.')
        circles=[]
        cs=sketch.sketchCurves.sketchCircles
        for i in range(cs.count):
            c=cs.item(i)
            circles.append({'centerMm':[round(c.geometry.center.x*MM,4),round(c.geometry.center.y*MM,4)],
                            'diameterMm':round(c.geometry.radius*2*MM,4),
                            'construction':c.isConstruction})
        lines=[]
        ls=sketch.sketchCurves.sketchLines
        for i in range(ls.count):
            line=ls.item(i); g=line.geometry
            lines.append({'startMm':[round(g.startPoint.x*MM,4),round(g.startPoint.y*MM,4)],
                          'endMm':[round(g.endPoint.x*MM,4),round(g.endPoint.y*MM,4)],
                          'construction':line.isConstruction})
        data={'fusionDocument':design.parentDocument.name,'sketch':sketch.name,'units':'mm',
              'geometryCounts':{'circles':len(circles),'lines':len(lines)},
              'circles':circles,'lines':lines}
        with open(OUT_JSON,'w') as f: json.dump(data,f,indent=2)
        ui.messageBox('Read-only mount-sketch audit complete.\n\nCircles: {}\nLines: {}\nAudit: {}'.format(len(circles),len(lines),OUT_JSON))
    except:
        if ui: ui.messageBox('Mount sketch audit failed:\n'+traceback.format_exc())


def stop(context):
    pass
