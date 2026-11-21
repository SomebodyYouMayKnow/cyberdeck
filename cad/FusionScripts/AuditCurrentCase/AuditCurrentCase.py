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
            lines = []
            for k in range(s.sketchCurves.sketchLines.count):
                line = s.sketchCurves.sketchLines.item(k)
                lines.append({'startMm': vec(line.startSketchPoint.geometry),
                              'endMm': vec(line.endSketchPoint.geometry),
                              'construction': line.isConstruction})
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
                'profiles': [
                    {
                        'areaMm2': round(s.profiles.item(p).areaProperties().area * MM * MM, 3),
                        'centroidMm': vec(s.profiles.item(p).areaProperties().centroid)
                    }
                    for p in range(s.profiles.count)
                ],
                'circles': circles
                , 'lines': lines
            })
        lid_faces = []
        lid_extrusions = []
        for i in range(root.features.extrudeFeatures.count):
            feature = root.features.extrudeFeatures.item(i)
            profile_rows = []
            try:
                profiles = feature.profile
                for j in range(profiles.profileLoops.count):
                    pass
            except Exception:
                pass
            try:
                profile = feature.profile
                if profile:
                    profile_rows.append({
                        'areaMm2': round(profile.areaProperties().area * MM * MM, 3),
                        'centroidMm': vec(profile.areaProperties().centroid),
                        'sketchName': profile.sketch.name
                    })
            except Exception:
                pass
            lid_extrusions.append({
                'name': feature.name,
                'operation': str(feature.operation),
                'isSuppressed': feature.isSuppressed,
                'profiles': profile_rows
            })
        for i in range(root.bRepBodies.count):
            b = root.bRepBodies.item(i)
            if not b.name.startswith('Lid shell 238.6 x 138.6'):
                continue
            for j in range(b.faces.count):
                f = b.faces.item(j)
                plane = adsk.core.Plane.cast(f.geometry)
                if plane:
                    box = f.boundingBox
                    lid_faces.append({
                        'faceIndex': j,
                        'areaMm2': round(f.area * MM * MM, 3),
                        'normal': [round(plane.normal.x, 5), round(plane.normal.y, 5), round(plane.normal.z, 5)],
                        'originMm': vec(plane.origin),
                        'boundsMm': [mm(box.minPoint.x), mm(box.minPoint.y), mm(box.minPoint.z),
                                     mm(box.maxPoint.x), mm(box.maxPoint.y), mm(box.maxPoint.z)]
                    })
        data = {'document': design.parentDocument.name, 'units': 'mm', 'bodies': bodies,
                'sketches': sketches, 'lidHorizontalFaces': lid_faces,
                'extrusionFeatures': lid_extrusions}
        with open(OUT_JSON, 'w') as f:
            json.dump(data, f, indent=2)
        ui.messageBox('Read-only case audit saved. Bodies: {}. Sketches: {}.\n{}'.format(len(bodies), len(sketches), OUT_JSON))
    except:
        if ui:
            ui.messageBox('Current case audit failed:\n' + traceback.format_exc())


def stop(context):
    pass
