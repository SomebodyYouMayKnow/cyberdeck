"""Rotate the lid and its fit-check screen bodies open about the hinge pin."""
import adsk.core
import adsk.fusion
import math
import traceback

MM = 10.0  # Fusion internal length unit is cm.


def mm(v):
    return v * MM


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError('No active Fusion design.')
        root = design.rootComponent
        selected = []
        for i in range(root.bRepBodies.count):
            body = root.bRepBodies.item(i)
            if (body.name.startswith('Lid shell 238.6 x 138.6')
                    or body.name.startswith('Waveshare 7-inch LCD C retainer frame')
                    or body.name.startswith('Waveshare 7-inch LCD C fit-check board')
                    or body.name.startswith('Waveshare 7-inch LCD C active panel reference')
                    or body.name in ('Body26', 'Body27')):
                selected.append(body)
        if not any(b.name.startswith('Lid shell 238.6 x 138.6') for b in selected):
            raise RuntimeError('Lid shell not found.')
        lid = next(b for b in selected if b.name.startswith('Lid shell 238.6 x 138.6'))
        box = lid.boundingBox
        if box.maxPoint.z > 56.5 / MM or box.minPoint.z < 41.5 / MM:
            raise RuntimeError('Lid is already moved from its closed pose; refusing to rotate it again.')

        entities = adsk.core.ObjectCollection.create()
        for body in selected:
            entities.add(body)
        matrix = adsk.core.Matrix3D.create()
        # Hinge pin axis is X, centered at (0, 139.3, 50.0) mm.
        # -110 degrees raises the front of the lid away from the base.
        axis = adsk.core.Vector3D.create(1, 0, 0)
        pivot = adsk.core.Point3D.create(0, 139.3 / MM, 50.0 / MM)
        if not matrix.setToRotation(math.radians(-110), axis, pivot):
            raise RuntimeError('Could not create lid rotation transform.')
        move_input = root.features.moveFeatures.createInput2(entities)
        move_input.defineAsFreeMove(matrix)
        root.features.moveFeatures.add(move_input)

        app.activeViewport.fit()
        app.activeDocument.save('Open lid to show inside and screen fit')
        ui.messageBox('Opened the lid 110 degrees around the existing X-axis hinge pin. The HDMI screen, retainer, and ESP32 lid references moved with it; the base and hinge pin stayed in place.')
    except:
        if ui:
            ui.messageBox('Open-lid move failed.\n\n' + traceback.format_exc())


def stop(context):
    pass
