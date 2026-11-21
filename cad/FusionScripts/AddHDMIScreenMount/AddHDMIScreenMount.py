"""Upgrade the Fusion lid fit-check to the Waveshare 7-inch HDMI LCD (C)."""

import adsk.core
import adsk.fusion
import json
import traceback

MM = 10.0  # Fusion API internal units are centimetres.
AUDIT = (r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering'
         r'\cad\fusion_screen_mount_audit.json')


def point(x, y, z=0):
    return adsk.core.Point3D.create(x / MM, y / MM, z / MM)


def plane_at_z(comp, z_mm):
    plane_input = comp.constructionPlanes.createInput()
    plane_input.setByOffset(comp.xYConstructionPlane,
                            adsk.core.ValueInput.createByReal(z_mm / MM))
    return comp.constructionPlanes.add(plane_input)


def rect(sketch, x0, y0, x1, y1):
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(point(x0, y0), point(x1, y1))


def extrude(comp, profile, length_mm, operation, participant=None, flip=False):
    feature_input = comp.features.extrudeFeatures.createInput(profile, operation)
    if participant:
        feature_input.participantBodies = [participant]
    feature_input.setDistanceExtent(False,
        adsk.core.ValueInput.createByReal(length_mm / MM))
    feature_input.isDirectionFlipped = flip
    return comp.features.extrudeFeatures.add(feature_input)


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError('No active Fusion design.')
        root = design.rootComponent
        document = app.activeDocument

        if any(root.bRepBodies.item(i).name.startswith('Waveshare 7-inch LCD C')
               for i in range(root.bRepBodies.count)):
            ui.messageBox('The 7-inch LCD C fit-check already exists; no duplicate geometry was added.')
            return

        # Hide the obsolete provisional 3.5-inch fit-check solids. The case, lid,
        # hinge, PCB, and all existing hardware remain in their original locations.
        for i in range(root.bRepBodies.count):
            body = root.bRepBodies.item(i)
            if body.name.startswith('HDMI LCD'):
                body.isVisible = False
        for i in range(root.sketches.count):
            sketch = root.sketches.item(i)
            if sketch.name.startswith('HDMI LCD'):
                sketch.isVisible = False

        lid = next((root.bRepBodies.item(i) for i in range(root.bRepBodies.count)
                    if root.bRepBodies.item(i).name.startswith('Lid shell 238.6 x 138.6')),
                   None)
        if not lid:
            raise RuntimeError('Could not find the expected lid shell. No screen geometry was created.')

        roof_top = lid.boundingBox.maxPoint.z * MM
        roof_thickness = 2.4
        roof_bottom = roof_top - roof_thickness
        if abs(roof_top - 56.0) > 0.5:
            raise RuntimeError('Unexpected lid roof top Z: {:.2f} mm.'.format(roof_top))

        # Waveshare 7inch HDMI LCD (C), official nominal dimensions 164.90 x
        # 106.96 x 8 mm. This is a fit envelope; the board hole pattern is not
        # dimensioned in the accessible drawing, so the retainer uses case-side
        # holes in rails outside the display envelope instead of guessed LCD holes.
        board_w, board_h, assembly_h = 164.90, 106.96, 8.0
        board_x, board_y = -2.8, 14.52
        board_cx, board_cy = board_x + board_w / 2, board_y + board_h / 2
        active_w, active_h = 154.21, 85.92
        view_x0 = board_cx - active_w / 2
        view_x1 = board_cx + active_w / 2
        view_y0 = board_cy - active_h / 2
        view_y1 = board_cy + active_h / 2

        # Cut the Waveshare panel opening through the lid. It intentionally
        # encompasses the old 3.5-inch opening, replacing that provisional size.
        display_window = root.sketches.add(plane_at_z(root, roof_top))
        display_window.name = 'Waveshare 7-inch LCD C active-area window 154.21 x 85.92'
        rect(display_window, view_x0, view_y0, view_x1, view_y1)
        extrude(root, display_window.profiles.item(0), 3.0,
                adsk.fusion.FeatureOperations.CutFeatureOperation, lid, True)

        # Separate top-lid aperture for the LILYGO 1.91-inch AMOLED. The existing
        # case layout's window datum is retained, so this is not shifted to suit
        # the larger panel. 23 x 47 mm is the current case-layout opening.
        amoled_w, amoled_h = 23.0, 47.0
        amoled_x, amoled_y = 164.0, 38.0
        amoled = root.sketches.add(plane_at_z(root, roof_top))
        amoled.name = 'LILYGO 1.91-inch AMOLED lid window 23 x 47'
        rect(amoled, amoled_x, amoled_y, amoled_x + amoled_w, amoled_y + amoled_h)
        extrude(root, amoled.profiles.item(0), 3.0,
                adsk.fusion.FeatureOperations.CutFeatureOperation, lid, True)

        # Plug the two obsolete right-side 3.5-inch retainer holes that fall under
        # the new LCD board envelope. The other pair is inside the enlarged LCD
        # viewing aperture and has already disappeared into that opening.
        plug = root.sketches.add(plane_at_z(root, roof_bottom))
        plug.name = 'Close obsolete 3.5-inch mount holes under 7-inch panel'
        for y in (34.5, 97.5):
            plug.sketchCurves.sketchCircles.addByCenterRadius(point(161.5, y), 1.15 / MM)
        for i in range(plug.profiles.count):
            extrude(root, plug.profiles.item(i), roof_thickness,
                    adsk.fusion.FeatureOperations.JoinFeatureOperation, lid, False)

        # Support frame under the panel. It is fixed through four M2 clearance
        # holes in the lid's top/bottom margins, outside the LCD board footprint.
        frame_outer = (-3.3, 8.0, 162.8, 128.0)
        frame_inner = (-2.5, 14.2, 162.3, 121.8)
        frame_sketch = root.sketches.add(plane_at_z(root, roof_bottom - 4.0))
        frame_sketch.name = 'Waveshare 7-inch LCD C retaining frame outline'
        rect(frame_sketch, *frame_outer)
        frame = extrude(root, frame_sketch.profiles.item(0), 4.0,
                        adsk.fusion.FeatureOperations.NewBodyFeatureOperation).bodies.item(0)
        frame.name = 'Waveshare 7-inch LCD C retainer frame'

        frame_clearance = root.sketches.add(plane_at_z(root, roof_bottom - 4.0))
        frame_clearance.name = 'Waveshare 7-inch LCD C board clearance 165.4 x 107.6'
        rect(frame_clearance, *frame_inner)
        extrude(root, frame_clearance.profiles.item(0), 4.0,
                adsk.fusion.FeatureOperations.CutFeatureOperation, frame, False)

        screw_d = 2.2
        screw_centres = [(10.0, 10.0), (155.0, 10.0),
                         (10.0, 126.0), (155.0, 126.0)]
        lid_holes = root.sketches.add(plane_at_z(root, roof_top))
        lid_holes.name = 'Waveshare LCD retainer M2 lid holes'
        for x, y in screw_centres:
            lid_holes.sketchCurves.sketchCircles.addByCenterRadius(
                point(x, y), (screw_d / 2) / MM)
        for i in range(lid_holes.profiles.count):
            extrude(root, lid_holes.profiles.item(i), 3.0,
                    adsk.fusion.FeatureOperations.CutFeatureOperation, lid, True)

        frame_holes = root.sketches.add(plane_at_z(root, roof_bottom - 4.0))
        frame_holes.name = 'Waveshare LCD retainer M2 through holes'
        for x, y in screw_centres:
            frame_holes.sketchCurves.sketchCircles.addByCenterRadius(
                point(x, y), (screw_d / 2) / MM)
        for i in range(frame_holes.profiles.count):
            extrude(root, frame_holes.profiles.item(i), 4.0,
                    adsk.fusion.FeatureOperations.CutFeatureOperation, frame, False)

        # Visible solid envelope: 8 mm thickness from lid underside toward the
        # case. This lets the user inspect the real panel volume and nearby window.
        board_sketch = root.sketches.add(plane_at_z(root, roof_bottom - assembly_h))
        board_sketch.name = 'Waveshare 7-inch LCD C board envelope 164.9 x 106.96'
        rect(board_sketch, board_x, board_y, board_x + board_w, board_y + board_h)
        board = extrude(root, board_sketch.profiles.item(0), assembly_h,
                        adsk.fusion.FeatureOperations.NewBodyFeatureOperation).bodies.item(0)
        board.name = 'Waveshare 7-inch LCD C fit-check board 164.9 x 106.96 x 8'

        panel_sketch = root.sketches.add(plane_at_z(root, roof_bottom))
        panel_sketch.name = 'Waveshare 7-inch LCD C active panel reference'
        rect(panel_sketch, view_x0, view_y0, view_x1, view_y1)
        panel = extrude(root, panel_sketch.profiles.item(0), roof_thickness,
                        adsk.fusion.FeatureOperations.NewBodyFeatureOperation).bodies.item(0)
        panel.name = 'Waveshare 7-inch LCD C active panel reference'

        audit = {
            'document': document.name,
            'units': 'mm',
            'display': 'Waveshare 7inch HDMI LCD (C), SKU 11199 / Rev 4.1 reference',
            'source': 'https://www.waveshare.com/7inch-hdmi-lcd-c.htm',
            'nominalDisplayBoardMm': [board_w, board_h, assembly_h],
            'boardEnvelopeBoundsMm': [board_x, board_y, board_x + board_w, board_y + board_h],
            'activeAreaMm': [active_w, active_h],
            'activeAreaBoundsMm': [view_x0, view_y0, view_x1, view_y1],
            'activeWindowToLILYGOWindowGapMm': amoled_x - view_x1,
            'lilygoAmoledWindowMm': [amoled_w, amoled_h],
            'lilygoAmoledWindowBoundsMm': [amoled_x, amoled_y,
                                           amoled_x + amoled_w, amoled_y + amoled_h],
            'liveLidRoofMm': {'topZ': roof_top, 'undersideZ': roof_bottom,
                              'thickness': roof_thickness},
            'retainer': {'outerBoundsMm': list(frame_outer),
                         'clearanceBoundsMm': list(frame_inner),
                         'fastener': '4 x M2 screws, 2.2 mm clearance, through top/bottom rails',
                         'centresMm': screw_centres},
            'obsolete3p5inMountHoles': 'Two right-side holes plugged under panel envelope; left pair is inside enlarged display opening.',
            'caveat': 'The envelope dimensions are manufacturer nominal, but exact mount-hole pattern, connector position, and cable bend clearance are not provided by this CAD fit check. Verify actual screen revision before printing/order.'
        }
        with open(AUDIT, 'w') as f:
            json.dump(audit, f, indent=2)
        app.activeViewport.fit()
        document.save('Upgraded lid to Waveshare 7-inch display and LILYGO window')
        ui.messageBox('Added the Waveshare 7-inch LCD C active-area opening and a separate LILYGO AMOLED window, plus an 8 mm screen envelope and top/bottom retainer. The Fusion document was saved. Review the fit-check bodies and verify exact screen mounting/cable details before printing.')
    except:
        if ui:
            ui.messageBox('7-inch display CAD update stopped. Review the model before retrying.\n\n' + traceback.format_exc())


def stop(context):
    pass
