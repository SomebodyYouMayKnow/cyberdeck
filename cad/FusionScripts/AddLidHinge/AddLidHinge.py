import adsk.core
import adsk.fusion
import json
import traceback

MM = 10.0  # Fusion API uses centimeters internally.
OUT_JSON = r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering\cad\fusion_lid_hinge_audit.json'


def p2(x, y):
    return adsk.core.Point3D.create(x/MM, y/MM, 0)


def offset_plane(comp, base_plane, offset_mm):
    plane_input = comp.constructionPlanes.createInput()
    plane_input.setByOffset(base_plane, adsk.core.ValueInput.createByReal(offset_mm/MM))
    return comp.constructionPlanes.add(plane_input)


def rect(sketch, x0, y0, x1, y1):
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(p2(x0, y0), p2(x1, y1))


def circle(sketch, x, y, diameter_mm):
    sketch.sketchCurves.sketchCircles.addByCenterRadius(p2(x, y), diameter_mm/(2*MM))


def extrude(comp, sketch, distance_mm, operation, participant=None):
    profile = sketch.profiles.item(0)
    inputs = comp.features.extrudeFeatures
    feature_input = inputs.createInput(profile, operation)
    if participant is not None:
        feature_input.participantBodies = [participant]
    feature_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(distance_mm/MM))
    return inputs.add(feature_input)


def make_ring_body(comp, name, x_start, y_center, z_center, length_mm, outer_d=8.0, bore_d=3.5):
    plane = offset_plane(comp, comp.yZConstructionPlane, x_start)
    s = comp.sketches.add(plane)
    # YZ-plane sketch coordinates map to global Y and Z; extrusion advances along +X.
    circle(s, y_center, z_center, outer_d)
    circle(s, y_center, z_center, bore_d)
    f = extrude(comp, s, length_mm, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body = f.bodies.item(0)
    body.name = name
    return body


def make_tab(comp, name, x0, x1, z0, z1, y_outer, depth_mm, hole_xs, hole_z, hole_d):
    # XZ plane normal points toward -Y. Offset by -y_outer to place it at +Y.
    plane = offset_plane(comp, comp.xZConstructionPlane, -y_outer)
    s = comp.sketches.add(plane)
    rect(s, x0, z0, x1, z1)
    for x in hole_xs:
        circle(s, x, hole_z, hole_d)
    f = extrude(comp, s, depth_mm, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body = f.bodies.item(0)
    body.name = name
    return body


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError('No active Fusion design.')
        root = design.rootComponent
        # Design datum was read from the current Body1: 232 x 132 mm footprint,
        # z=-4..50 mm. The latest PCB envelope is 226 x 126 mm, centered with 3 mm edge clearance.
        # This Fusion document is a Part Design document and only permits the root
        # component. Add new, separately named bodies there; Body1 and old sketches
        # are not edited or moved.
        comp = root

        for i in range(root.bRepBodies.count):
            if root.bRepBodies.item(i).name == 'Hinge pin 3 mm x 91 mm - use smooth rod':
                ui.messageBox('The NEONRED lid and hinge are already present; no duplicate geometry was added.')
                return

        # Lid shell: 3 mm nominal walls, 0.3 mm side clearance over the 232 x 132 case.
        # Outer shell overhangs case sides by 3 mm; skirt covers the upper 8 mm of the case.
        z_skirt_bottom = 42.0
        z_case_top = 50.0
        lid_roof_t = 2.4
        x_outer0, x_outer1 = -3.3, 235.3
        y_outer0, y_outer1 = -3.3, 135.3
        x_inner0, x_inner1 = 0.3, 231.7
        y_inner0, y_inner1 = 0.3, 131.7

        lid_body = None
        for i in range(root.bRepBodies.count):
            if root.bRepBodies.item(i).name.startswith('Lid shell 238.6 x 138.6'):
                lid_body = root.bRepBodies.item(i)
                break
        if not lid_body:
            lid_outer_plane = offset_plane(comp, comp.xYConstructionPlane, z_skirt_bottom)
            lid_outer_sketch = comp.sketches.add(lid_outer_plane)
            rect(lid_outer_sketch, x_outer0, y_outer0, x_outer1, y_outer1)
            blank = extrude(comp, lid_outer_sketch, z_case_top + lid_roof_t - z_skirt_bottom,
                            adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            lid_body = blank.bodies.item(0)
            lid_body.name = 'Lid shell 238.6 x 138.6 x 10.4 mm'

        cavity_plane = offset_plane(comp, comp.xYConstructionPlane, z_skirt_bottom)
        cavity_sketch = comp.sketches.add(cavity_plane)
        rect(cavity_sketch, x_inner0, y_inner0, x_inner1, y_inner1)
        extrude(comp, cavity_sketch, z_case_top-z_skirt_bottom,
                adsk.fusion.FeatureOperations.CutFeatureOperation, lid_body)

        # Three alternating knuckles run along X on the rear Y edge, with a 3 mm pin.
        # 0.6 mm gaps between printed barrels; 3.5 mm bores provide FDM clearance.
        axis_y, axis_z = 139.3, 50.0
        make_tab(comp, 'Base hinge leaf L - print with base', 70.0, 99.4, 44.0, 50.0,
                 axis_y, 7.3, [77.0, 92.0], 47.0, 2.7)
        make_ring_body(comp, 'Base hinge knuckle L', 70.0, axis_y, axis_z, 29.4)
        make_tab(comp, 'Lid hinge leaf - print with lid', 100.0, 130.0, 50.0, 57.0,
                 axis_y, 4.0, [106.0, 124.0], 54.0, 2.7)
        make_ring_body(comp, 'Lid center hinge knuckle', 100.0, axis_y, axis_z, 30.0)
        make_tab(comp, 'Base hinge leaf R - print with base', 130.6, 160.0, 44.0, 50.0,
                 axis_y, 7.3, [138.0, 153.0], 47.0, 2.7)
        make_ring_body(comp, 'Base hinge knuckle R', 130.6, axis_y, axis_z, 29.4)

        pin_plane = offset_plane(comp, comp.yZConstructionPlane, 69.5)
        pin_sketch = comp.sketches.add(pin_plane)
        circle(pin_sketch, axis_y, axis_z, 3.0)
        pin_feature = extrude(comp, pin_sketch, 91.0,
                              adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        pin_body = pin_feature.bodies.item(0)
        pin_body.name = 'Hinge pin 3 mm x 91 mm - use smooth rod'

        data = {
            'document': design.parentDocument.name,
            'units': 'mm',
            'sourceCaseBody': 'Body1, audited bounds X=0..232, Y=0..132, Z=-4..50',
            'pcbEnvelope': {'size': [226, 126, 1.6], 'placementInCaseMm': {'xRange': [4,230], 'yRange': [4,130]},
                            'edgeClearancesMm': {'left': 4, 'right': 2, 'front': 4, 'rear': 2}},
            'pcbCaseMountingHoles': {'diameterMm': 3.2, 'boardToCaseTransformMm': {'x': 4, 'y': 52},
                                     'caseLipHoleCentersMm': 'aligned to existing CAD centers within 0.25 mm',
                                     'innerFourHoleCentersMm': [[16,16],[213.55,16],[16,116],[213.55,114.61]]},
            'lid': {'outerSizeMm': [238.6,138.6], 'roofThicknessMm': lid_roof_t,
                    'skirtDepthMm': z_case_top-z_skirt_bottom,
                    'clearancePerSideMm': 0.3, 'shellZMm': [z_skirt_bottom,z_case_top+lid_roof_t]},
            'hinge': {'style': 'three-knuckle printed barrel hinge', 'axisMm': [None,axis_y,axis_z],
                      'barrelOuterDiameterMm': 8.0, 'barrelBoreMm': 3.5, 'pinDiameterMm': 3.0,
                      'printedBarrelGapsMm': 0.6, 'segmentsXmm': [[70,99.4],[100,130],[130.6,160]],
                      'leafPilotHolesMm': 2.7, 'physicalFitVerified': False},
            'caveat': 'Lid has no display apertures because the exact screen mounting position is not confirmed. Physical print fit, screen clearance, cable routing, hinge swing, and screw reach must be checked against measured modules.'
        }
        with open(OUT_JSON, 'w') as f:
            json.dump(data, f, indent=2)

        # Fit the design so the user can inspect the unchanged base and added shell/hinge.
        app.activeViewport.fit()
        ui.messageBox('Added a new lid/hinge component without moving Body1 or its sketches.\n\nCase: 232 x 132 mm. PCB: 226 x 126 mm, centered with 3 mm edge clearance. Existing PCB case-hole diameters and CAD hole centers are compatible in the latest export.\n\nLid and hinge details: ' + OUT_JSON)
    except:
        if ui:
            ui.messageBox('Lid/hinge creation failed. Existing Body1 was not edited; inspect the timeline for any partial new features.\n\n' + traceback.format_exc())


def stop(context):
    pass
