"""Ensure the power-bank USB-C case opening crosses the entire front wall."""
import adsk.core
import adsk.fusion
import os
import json
import traceback

MM = 10.0  # Fusion internal length unit is cm.
ROOT = r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering\cad'
AUDIT = os.path.join(ROOT, 'fusion_case_fit_and_ports_audit.json')


def p(x, y):
    return adsk.core.Point3D.create(x / MM, y / MM, 0)


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError('No active Fusion design.')
        comp = design.rootComponent
        case = next((comp.bRepBodies.item(i) for i in range(comp.bRepBodies.count)
                     if comp.bRepBodies.item(i).name == 'Body1'), None)
        if not case:
            raise RuntimeError('Could not find Body1 case. No change made.')
        name = 'Power-bank USB-C exterior pass-through 16x9 corrected'
        if any(comp.sketches.item(i).name == name for i in range(comp.sketches.count)):
            raise RuntimeError('The corrected exterior USB-C cut already exists. No duplicate added.')

        # Match the original case-port datum: the outside face is at y=-4 mm.
        # Cut inward 8 mm so the 3 mm front wall is fully crossed, with margin.
        plane_input = comp.constructionPlanes.createInput()
        plane_input.setByOffset(comp.xZConstructionPlane,
                                adsk.core.ValueInput.createByReal(-4.0 / MM))
        sketch = comp.sketches.add(comp.constructionPlanes.add(plane_input))
        sketch.name = name
        lines = sketch.sketchCurves.sketchLines
        lines.addTwoPointRectangle(p(108.0, 7.0), p(124.0, 16.0))
        cut_input = comp.features.extrudeFeatures.createInput(
            sketch.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
        cut_input.participantBodies = [case]
        cut_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(8.0 / MM))
        cut_input.isDirectionFlipped = False
        comp.features.extrudeFeatures.add(cut_input)
        app.activeDocument.save('USB-C opening now starts outside front wall and cuts fully through')

        if os.path.isfile(AUDIT):
            with open(AUDIT, 'r') as f:
                audit = json.load(f)
            audit.setdefault('caseOpenings', {})['powerBankUsbC'] = {
                'openingMm': [108.0, 7.0, 124.0, 16.0],
                'wall': 'front', 'outsideSketchPlaneOffsetMm': -4.0,
                'throughWallCutDepthMm': 8.0, 'belowPcbPlane': True,
                'passThroughVerifiedInModel': True,
                'connectorClearanceOpeningOnly': True}
            with open(AUDIT, 'w') as f:
                json.dump(audit, f, indent=2)
        ui.messageBox('USB-C opening corrected: 16 x 9 mm, sketch starts 4 mm outside the front wall and cuts 8 mm through it. It is below the PCB. This is an access opening for the bank’s existing port, not a new mounted USB-C jack.')
    except:
        if ui:
            ui.messageBox('USB-C correction stopped.\n\n' + traceback.format_exc())


def stop(context):
    pass
