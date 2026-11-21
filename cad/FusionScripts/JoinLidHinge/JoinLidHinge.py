import adsk.core
import adsk.fusion
import json
import traceback

MM = 10.0
OUT_JSON = r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering\cad\fusion_lid_hinge_audit.json'


def mm(v):
    return v / MM


def body_named(comp, name):
    for i in range(comp.bRepBodies.count):
        b = comp.bRepBodies.item(i)
        if b.name == name:
            return b
    return None


def xy_rect(comp, name, x0, y0, z0, x1, y1, z1):
    plane_input = comp.constructionPlanes.createInput()
    plane_input.setByOffset(comp.xYConstructionPlane,
                            adsk.core.ValueInput.createByReal(mm(z0)))
    plane = comp.constructionPlanes.add(plane_input)
    sketch = comp.sketches.add(plane)
    a = adsk.core.Point3D.create(mm(x0), mm(y0), 0)
    b = adsk.core.Point3D.create(mm(x1), mm(y1), 0)
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(a, b)
    feature_input = comp.features.extrudeFeatures.createInput(
        sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    feature_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(mm(z1-z0)))
    body = comp.features.extrudeFeatures.add(feature_input).bodies.item(0)
    body.name = name
    return body


def join(comp, target, tools):
    collection = adsk.core.ObjectCollection.create()
    for tool in tools:
        collection.add(tool)
    combine_input = comp.features.combineFeatures.createInput(target, collection)
    combine_input.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
    combine_input.isKeepToolBodies = False
    comp.features.combineFeatures.add(combine_input)


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        root = design.rootComponent
        base = body_named(root, 'Body1')
        lid = body_named(root, 'Lid shell 238.6 x 138.6 x 10.4 mm')
        if not base or not lid:
            raise RuntimeError('Could not find the existing case body and lid shell.')

        base_l = body_named(root, 'Base hinge knuckle L')
        base_r = body_named(root, 'Base hinge knuckle R')
        lid_mid = body_named(root, 'Lid center hinge knuckle')
        old_parts = [body_named(root, n) for n in [
            'Base hinge leaf L - print with base', 'Base hinge leaf R - print with base',
            'Lid hinge leaf - print with lid']]
        if not all([base_l, base_r, lid_mid]):
            raise RuntimeError('Existing hinge barrel bodies are missing; no geometry was changed.')

        # Bridge solids overlap the case/lid and their corresponding barrel bodies so
        # the hinge becomes structurally part of the printable case and lid.
        bridge_l = xy_rect(root, 'Base hinge bridge L', 70, 128.0, 44.0, 99.4, 140.0, 50.5)
        bridge_r = xy_rect(root, 'Base hinge bridge R', 130.6, 128.0, 44.0, 160.0, 140.0, 50.5)
        bridge_mid = xy_rect(root, 'Lid hinge bridge', 100.0, 130.0, 49.5, 130.0, 140.0, 56.0)

        join(root, base, [bridge_l, base_l])
        join(root, base, [bridge_r, base_r])
        join(root, lid, [bridge_mid, lid_mid])

        for b in old_parts:
            if b:
                b.isVisible = False

        # Save final body bounds for a dimension check.
        body_data = []
        for b in [base, lid, body_named(root, 'Hinge pin 3 mm x 91 mm - use smooth rod')]:
            if not b:
                continue
            bb = b.boundingBox
            body_data.append({'name': b.name,
                              'minMm': [round(bb.minPoint.x*MM, 3), round(bb.minPoint.y*MM, 3), round(bb.minPoint.z*MM, 3)],
                              'maxMm': [round(bb.maxPoint.x*MM, 3), round(bb.maxPoint.y*MM, 3), round(bb.maxPoint.z*MM, 3)]})
        with open(OUT_JSON, 'r') as f:
            data = json.load(f)
        data['hinge']['integratedIntoCaseAndLid'] = True
        data['hinge']['printParts'] = ['case with two integrated hinge knuckles', 'lid with integrated center knuckle', '3 mm smooth pin']
        data['hinge']['bodyBoundsAfterJoin'] = body_data
        data['caveat'] = 'PCB envelope and case hole locations were compared to the latest PCB export. Lid has no screen window because the display mounting position is unconfirmed. Verify screen, cables, module heights, print tolerance, hinge swing and screw access with a physical prototype.'
        with open(OUT_JSON, 'w') as f:
            json.dump(data, f, indent=2)
        app.activeViewport.fit()
        ui.messageBox('Joined the hinge barrels into the existing case and lid bodies. Body1 and the original sketches were preserved. Review the 3D model and save this design.')
    except:
        if ui:
            ui.messageBox('Hinge integration did not complete cleanly. Use Undo once if the timeline shows partial bridge bodies, then inspect the error:\n\n' + traceback.format_exc())


def stop(context):
    pass
