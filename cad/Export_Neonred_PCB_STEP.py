"""Build and export the current NEONRED carrier PCB as a STEP solid in Fusion 360.

Run this file from Fusion 360's Utilities > Scripts and Add-Ins in the Design
workspace. It creates a new design, sketches the 226 x 126 mm tabbed outline
and 24 NPTHs, extrudes a 1.6 mm board, then writes the STEP beside this script.
It intentionally exports the carrier PCB plate only, not the enclosure/modules.
"""

import adsk.core
import adsk.fusion
import os
import traceback


def mm(v):
    # Fusion API internal length unit is centimetres.
    return v / 10.0


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = adsk.fusion.Design.cast(app.activeProduct)
        root = design.rootComponent
        sketches = root.sketches
        sketch = sketches.add(root.xYConstructionPlane)
        sketch.name = 'NEONRED PCB outline and NPTHs (mm)'
        lines = sketch.sketchCurves.sketchLines

        outline = [
            [8, 8], [55.5, 8], [55.5, 1.5], [57, 0], [64, 0], [65.5, 1.5], [65.5, 8],
            [160.5, 8], [160.5, 1.5], [162, 0], [169, 0], [170.5, 1.5], [170.5, 8], [218, 8],
            [218, 30.5], [224.5, 30.5], [226, 32], [226, 39], [224.5, 40.5], [218, 40.5],
            [218, 85.5], [224.5, 85.5], [226, 87], [226, 94], [224.5, 95.5], [218, 95.5],
            [218, 118], [170.5, 118], [170.5, 124.5], [169, 126], [162, 126], [160.5, 124.5], [160.5, 118],
            [65.5, 118], [65.5, 124.5], [64, 126], [57, 126], [55.5, 124.5], [55.5, 118], [8, 118],
            [8, 95.5], [1.5, 95.5], [0, 94], [0, 87], [1.5, 85.5], [8, 85.5], [8, 40.5],
            [1.5, 40.5], [0, 39], [0, 32], [1.5, 30.5], [8, 30.5]
        ]
        for i, p in enumerate(outline):
            q = outline[(i + 1) % len(outline)]
            lines.addByTwoPoints(
                adsk.core.Point3D.create(mm(p[0]), mm(p[1]), 0),
                adsk.core.Point3D.create(mm(q[0]), mm(q[1]), 0),
            )

        # Twelve case holes: four in the PCB field and eight on the perimeter lips.
        case_holes = [
            [13, 13], [210.56, 14.4], [13, 113], [210.56, 113],
            [60.5, 4], [164.5, 4], [222, 35.5], [222, 90.5],
            [164.5, 122], [60.5, 122], [4, 90.5], [4, 35.5],
        ]
        # Pi Zero mounting pattern measured from the exported NPTH drill file.
        pi_holes = [[116.557, 52.147], [139.557, 52.147], [116.557, 110.147], [139.557, 110.147]]
        # CardKB and Chameleon support holes added in the current candidate.
        support_holes = [
            [13.5, 48.5], [106.5, 48.5], [13.5, 107.5], [106.5, 107.5],
            [150, 14], [202, 14], [150, 34], [202, 34],
        ]
        circles = sketch.sketchCurves.sketchCircles
        for x, y in case_holes:
            circles.addByCenterRadius(adsk.core.Point3D.create(mm(x), mm(y), 0), mm(1.6))
        for x, y in pi_holes + support_holes:
            circles.addByCenterRadius(adsk.core.Point3D.create(mm(x), mm(y), 0), mm(2.751 / 2))

        # Fusion exposes each hole interior as a separate profile as well as
        # the board face. Select the board face by its many loops (outer edge
        # plus all NPTHs), not by assuming the sketch contains one profile.
        profile = None
        max_loop_count = 0
        for index in range(sketch.profiles.count):
            candidate = sketch.profiles.item(index)
            loop_count = candidate.profileLoops.count
            if loop_count > max_loop_count:
                profile = candidate
                max_loop_count = loop_count
        expected_loop_count = 1 + len(case_holes) + len(pi_holes) + len(support_holes)
        if profile is None or max_loop_count != expected_loop_count:
            raise RuntimeError('Expected board face with {} loops; found max {}'.format(expected_loop_count, max_loop_count))
        extrudes = root.features.extrudeFeatures
        ext_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(mm(1.6))
        ext_input.setDistanceExtent(False, distance)
        extrusion = extrudes.add(ext_input)
        extrusion.name = 'NEONRED PCB 1.6 mm'
        body = extrusion.bodies.item(0)
        body.name = 'NEONRED carrier PCB with lips and 24 NPTH'

        step_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'NEONRED_PCB_component-mounts_2026-10-19.step')
        options = design.exportManager.createSTEPExportOptions(step_path)
        if not design.exportManager.execute(options):
            raise RuntimeError('Fusion STEP export failed: ' + step_path)
        ui.messageBox('STEP exported:\n' + step_path + '\n\nBoard outline: 226 x 126 mm; thickness: 1.6 mm; NPTH: 24.')
    except:
        if ui:
            ui.messageBox('NEONRED STEP export failed:\n{}'.format(traceback.format_exc()))
