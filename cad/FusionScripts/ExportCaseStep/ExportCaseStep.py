"""Export current Fusion assembly STEP and the two printable case shells."""

import adsk.core
import adsk.fusion
import os
import traceback


CAD_DIR = r"C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering\cad"
OUTPUT = os.path.join(CAD_DIR, "NEONRED_Cyberdeck_Case_FitCheck_2026-11-21.step")
BASE_STL = os.path.join(CAD_DIR, "NEONRED_Case_Base_2026-11-21.stl")
LID_STL = os.path.join(CAD_DIR, "NEONRED_Case_Lid_2026-11-21.stl")


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError("No active Fusion design.")
        document = app.activeDocument
        if document and document.isModified:
            document.save("Saved before STEP export")
        manager = design.exportManager
        options = manager.createSTEPExportOptions(OUTPUT, design.rootComponent)
        if not manager.execute(options):
            raise RuntimeError("Fusion STEP export returned failure.")
        root = design.rootComponent
        base = next((root.bRepBodies.item(i) for i in range(root.bRepBodies.count)
                     if root.bRepBodies.item(i).name == "Body1"), None)
        lid = next((root.bRepBodies.item(i) for i in range(root.bRepBodies.count)
                    if root.bRepBodies.item(i).name.startswith("Lid shell 238.6 x 138.6")), None)
        if not base or not lid:
            raise RuntimeError("Could not find Body1 base or lid shell for print meshes.")
        for body, path in ((base, BASE_STL), (lid, LID_STL)):
            mesh = manager.createSTLExportOptions(body, path)
            mesh.isBinaryFormat = True
            if not manager.execute(mesh):
                raise RuntimeError("Fusion STL export returned failure for " + body.name)
        ui.messageBox("STEP and print meshes exported:\n{}\n{}\n{}".format(OUTPUT, BASE_STL, LID_STL))
    except:
        if ui:
            ui.messageBox("STEP export failed:\n" + traceback.format_exc())


def stop(context):
    pass

