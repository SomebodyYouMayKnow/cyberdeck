import adsk.core
import adsk.fusion
import json
import traceback

MM = 10.0
OUT_JSON = r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering\cad\fusion_lid_hinge_audit.json'


def pt(x, y):
    return adsk.core.Point3D.create(x / MM, y / MM, 0)


def find_body(comp, name):
    for i in range(comp.bRepBodies.count):
        b = comp.bRepBodies.item(i)
        if b.name == name:
            return b
    return None


def yz_plane(comp, x_mm):
    pi = comp.constructionPlanes.createInput()
    pi.setByOffset(comp.yZConstructionPlane, adsk.core.ValueInput.createByReal(x_mm/MM))
    return comp.constructionPlanes.add(pi)


def circle_sketch(comp, x_mm, y_mm, z_mm, dia_mm):
    s = comp.sketches.add(yz_plane(comp, x_mm))
    # Fusion's YZ sketch X axis maps to world -Z; sketch Y maps to world +Y.
    s.sketchCurves.sketchCircles.addByCenterRadius(pt(-z_mm, y_mm), dia_mm/(2*MM))
    return s


def extrude_new(comp, sketch, length_mm, name):
    inp = comp.features.extrudeFeatures.createInput(
        sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    inp.setDistanceExtent(False, adsk.core.ValueInput.createByReal(length_mm/MM))
    body = comp.features.extrudeFeatures.add(inp).bodies.item(0)
    body.name = name
    return body


def join_body(comp, target, tool):
    coll = adsk.core.ObjectCollection.create()
    coll.add(tool)
    inp = comp.features.combineFeatures.createInput(target, coll)
    inp.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
    inp.isKeepToolBodies = False
    comp.features.combineFeatures.add(inp)


def cut_bore(comp, target, x0, length):
    s = circle_sketch(comp, x0, 139.3, 50.0, 3.5)
    inp = comp.features.extrudeFeatures.createInput(
        s.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
    inp.participantBodies = [target]
    inp.setDistanceExtent(False, adsk.core.ValueInput.createByReal(length/MM))
    comp.features.extrudeFeatures.add(inp)


def create_pin(comp):
    s = circle_sketch(comp, 69.5, 139.3, 50.0, 3.0)
    return extrude_new(comp, s, 91.0, 'Hinge pin 3 mm x 91 mm - correct world axis')


def bounds(body):
    b = body.boundingBox
    return {'name': body.name,
            'minMm': [round(b.minPoint.x*MM, 3), round(b.minPoint.y*MM, 3), round(b.minPoint.z*MM, 3)],
            'maxMm': [round(b.maxPoint.x*MM, 3), round(b.maxPoint.y*MM, 3), round(b.maxPoint.z*MM, 3)]}


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        comp = design.rootComponent
        base = find_body(comp, 'Body1')
        lid = find_body(comp, 'Lid shell 238.6 x 138.6 x 10.4 mm')
        if not base or not lid:
            raise RuntimeError('Case Body1 or original lid shell was not found.')

        # The previous YZ sketch used local coordinates as if they mapped X->Y, Y->Z.
        # Actual Fusion mapping is local X->-Z, local Y->+Y. Hide those misplaced parts.
        obsolete_names = ['Base hinge knuckle L', 'Base hinge knuckle R',
                          'Lid center hinge knuckle',
                          'Hinge pin 3 mm x 91 mm - use smooth rod',
                          'Lid shell 238.6 x 138.6 x 10.4 mm (1)']
        for name in obsolete_names:
            b = find_body(comp, name)
            if b:
                b.isVisible = False

        # Correctly oriented annular knuckles are joined to the existing bridge-reinforced bodies.
        # Base hinge segments: x 70..99.4 and 130.6..160. Lid segment: x 100..130.
        for x0, length, target, label in [
            (70.0, 29.4, base, 'base left'),
            (130.6, 29.4, base, 'base right'),
            (100.0, 30.0, lid, 'lid center')]:
            s = comp.sketches.add(yz_plane(comp, x0))
            # Fusion's YZ sketch X axis maps to world -Z, sketch Y to world +Y.
            s.sketchCurves.sketchCircles.addByCenterRadius(pt(-50.0, 139.3), 4.0/MM)
            s.sketchCurves.sketchCircles.addByCenterRadius(pt(-50.0, 139.3), 1.75/MM)
            tube = extrude_new(comp, s, length, 'Integrated hinge barrel ' + label)
            join_body(comp, target, tube)
            cut_bore(comp, target, x0, length)

        # Keep old exploded leaf bodies hidden for recoverability; hide the old misoriented pin.
        for name in ['Base hinge leaf L - print with base', 'Lid hinge leaf - print with lid',
                     'Base hinge leaf R - print with base']:
            b = find_body(comp, name)
            if b:
                b.isVisible = False
        pin = create_pin(comp)
        data = {'units': 'mm', 'pcbEnvelopeMm': [226, 126],
                'caseOuterXYMm': [232, 132], 'lidOuterXYMm': [238.6, 138.6],
                'pcbPlacementMm': {'x': 4, 'y': 4},
                'pcbEdgeClearancesMm': {'left': 4, 'right': 2, 'front': 4, 'rear': 2},
                'caseHoleDiameterMm': 3.2,
                'hinge': {'worldAxis': 'X', 'axisCenterMm': [None, 139.3, 50.0],
                          'barrelODmm': 8.0, 'boreMm': 3.5, 'pinMm': 3.0,
                          'segmentsXmm': [[70.0, 99.4], [100.0, 130.0], [130.6, 160.0]],
                          'integratedIntoCaseAndLid': True,
                          'pinBounds': bounds(pin)},
                'resultBodies': [bounds(base), bounds(lid)],
                'caveat': 'Nominal PCB outline and mounting-hole centers align to the Fusion tray. Electronics height, screen window position, cable routing, lid swing, and physical FDM tolerance need a fit prototype.'}
        with open(OUT_JSON, 'w') as f:
            json.dump(data, f, indent=2)
        app.activeViewport.fit()
        ui.messageBox('Corrected Fusion plane orientation and integrated three hinge barrels into the case and lid bodies. Misoriented draft hinge bodies were hidden, not deleted. Inspect and save the 3D model.\n\n' + OUT_JSON)
    except:
        if ui:
            ui.messageBox('Hinge orientation repair failed. Do not order/print this CAD yet.\n\n' + traceback.format_exc())


def stop(context):
    pass
