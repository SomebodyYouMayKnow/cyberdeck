import adsk.core
import adsk.fusion
import os
import traceback

ROOT_DIR = r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering'
OUT_STL = os.path.join(ROOT_DIR, 'cad', 'PrusaFast15h', 'NEONRED_Case_Lid_Fast15h_WindowThrough.stl')
MM = 10.0

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError('No active Fusion design.')
        comp = design.rootComponent
        lid = next((comp.bRepBodies.item(i) for i in range(comp.bRepBodies.count)
                    if comp.bRepBodies.item(i).name.startswith('Lid shell 238.6 x 138.6')),
                   None)
        if not lid:
            raise RuntimeError('Could not find the lid shell. No geometry changed.')

        # The shallow screen recess has a 23 x 47 mm planar floor. Cut through
        # from that exact face so the new opening follows the existing lid pose
        # and does not depend on a closed-case coordinate transform.
        target = None
        for i in range(lid.faces.count):
            face = lid.faces.item(i)
            if abs(face.area * MM * MM - 1081.0) < 0.05 and adsk.core.Plane.cast(face.geometry):
                target = face
                break
        if not target:
            raise RuntimeError('Expected 23 x 47 mm ESP32 screen-window floor was not found. No geometry changed.')
        if target.edges.count != 4:
            raise RuntimeError('Screen-window floor is not a four-edge rectangle. No geometry changed.')

        sketch = comp.sketches.add(target)
        sketch.name = 'Cut ESP32 screen aperture fully through lid'
        for i in range(target.edges.count):
            sketch.project(target.edges.item(i))
        if sketch.profiles.count != 1:
            raise RuntimeError('Projected screen-window boundary produced {} profiles; expected exactly one. No cut was made.'.format(sketch.profiles.count))
        profile = sketch.profiles.item(0)
        if abs(profile.areaProperties().area * MM * MM - 1081.0) > 0.1:
            raise RuntimeError('Projected screen profile is not 23 x 47 mm. No cut was made.')

        ex_input = comp.features.extrudeFeatures.createInput(
            profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        ex_input.participantBodies = [lid]
        if not ex_input.setAllExtent(adsk.fusion.ExtentDirections.SymmetricExtentDirection):
            raise RuntimeError('Fusion rejected the symmetric through-all cut. No cut was made.')
        feature = comp.features.extrudeFeatures.add(ex_input)
        if not feature or not feature.isValid:
            raise RuntimeError('Fusion did not create a valid through-cut.')
        feature.name = 'ESP32 screen window through-cut (23 x 47 mm)'

        # Confirm the planar floor is gone, then write the actual lid body mesh.
        remaining = []
        for i in range(lid.faces.count):
            f = lid.faces.item(i)
            if abs(f.area * MM * MM - 1081.0) < 0.05 and adsk.core.Plane.cast(f.geometry):
                remaining.append(i)
        if remaining:
            raise RuntimeError('The 23 x 47 mm planar floor remains at lid faces {}. The export was not written.'.format(remaining))

        os.makedirs(os.path.dirname(OUT_STL), exist_ok=True)
        export_mgr = design.exportManager
        options = export_mgr.createSTLExportOptions(lid, OUT_STL)
        if not export_mgr.execute(options):
            raise RuntimeError('Fusion could not export the corrected lid STL.')
        app.activeDocument.save('Cut the ESP32 screen window through the lid roof')
        ui.messageBox('Cut the 23 x 47 mm screen window through the lid and exported the corrected STL:\n' + OUT_STL)
    except:
        if ui:
            ui.messageBox('Lid aperture fix stopped. Review before retrying.\n\n' + traceback.format_exc())

def stop(context):
    pass
