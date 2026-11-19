"""Export the active Fusion case assembly as a STEP file into cad/."""

import adsk.core
import adsk.fusion
import os
import traceback


OUTPUT = r"C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering\cad\NEONRED_Case_Lid_Hinge.step"


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
        ui.messageBox("STEP export completed:\n" + OUTPUT)
    except:
        if ui:
            ui.messageBox("STEP export failed:\n" + traceback.format_exc())


def stop(context):
    pass
