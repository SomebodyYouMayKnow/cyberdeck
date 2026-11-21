"""Update live cyberdeck CAD with the Pi/HAT underside and device envelopes.

The Pi/HAT underside stack is an explicit conservative fit-check envelope, not
vendor-specific connector CAD. Existing PCB, lid, display, and case placements
are retained. The battery is moved within the existing base to clear the stack.
"""
import adsk.core
import adsk.fusion
import json
import os
import traceback

MM = 10.0  # Fusion's internal length units are centimeters.
ROOT_DIR = r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering\cad'
AUDIT = os.path.join(ROOT_DIR, 'fusion_case_fit_and_ports_audit.json')
PCB_BOTTOM = 33.0
PCB_TOP = 34.6


def pt(x, y, z=0):
    return adsk.core.Point3D.create(x / MM, y / MM, z / MM)


def offset_plane(comp, base, mm):
    inp = comp.constructionPlanes.createInput()
    inp.setByOffset(base, adsk.core.ValueInput.createByReal(mm / MM))
    return comp.constructionPlanes.add(inp)


def rect(sk, x0, y0, x1, y1):
    sk.sketchCurves.sketchLines.addTwoPointRectangle(pt(x0, y0), pt(x1, y1))


def find_body(comp, name):
    for i in range(comp.bRepBodies.count):
        b = comp.bRepBodies.item(i)
        if b.name == name:
            return b
    return None


def extrude(comp, profile, depth_mm, operation, participant=None):
    inp = comp.features.extrudeFeatures.createInput(profile, operation)
    if participant:
        inp.participantBodies = [participant]
    inp.setDistanceExtent(False, adsk.core.ValueInput.createByReal(depth_mm / MM))
    return comp.features.extrudeFeatures.add(inp)


def body_bounds(body):
    b = body.boundingBox
    return [round(b.minPoint.x * MM, 3), round(b.minPoint.y * MM, 3), round(b.minPoint.z * MM, 3),
            round(b.maxPoint.x * MM, 3), round(b.maxPoint.y * MM, 3), round(b.maxPoint.z * MM, 3)]


def box(comp, name, bounds, label):
    x0, y0, z0, x1, y1, z1 = bounds
    sk = comp.sketches.add(offset_plane(comp, comp.xYConstructionPlane, z0))
    sk.name = name + ' footprint'
    rect(sk, x0, y0, x1, y1)
    ex = extrude(comp, sk.profiles.item(0), z1-z0, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    b = ex.bodies.item(0)
    b.name = name + ' - fit-check envelope'
    return b


def run(context):
    ui = None
    created = []
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError('No active Fusion design.')
        doc = app.activeDocument
        root = design.rootComponent
        case = find_body(root, 'Body1')
        pcb = find_body(root, 'NEONRED PCB 226x126 fit-check')
        bank = find_body(root, 'INIU BI-B5 power bank fit-check')
        if not case or not pcb or not bank:
            raise RuntimeError('Expected Body1, the PCB envelope, and the INIU bank envelope. No geometry was changed.')
        if find_body(root, 'Pi Zero 2 W + Waveshare USB Hub HAT underside stack - fit-check envelope'):
            raise RuntimeError('This fit-check update is already present. No duplicate geometry was added.')
        if abs(pcb.boundingBox.minPoint.z*MM - PCB_BOTTOM) > 0.2:
            raise RuntimeError('PCB Z datum is not the audited 33 mm plane. No geometry was changed.')

        # Move the nominal bank upward in the case datum by 26 mm. This places it
        # behind the Pi/HAT underside envelope and clears all four PCB corner
        # support rings. Existing PCB and case coordinates remain unchanged.
        old_bank = body_bounds(bank)
        expected_old = [49.0, 30.5, 0.5, 183.0, 101.5, 26.0]
        if max(abs(a-b) for a, b in zip(old_bank, expected_old)) > 0.3:
            raise RuntimeError('Power bank bounds differ from the known fit-check placement; no automatic move was made.')
        # The original upper retention rail crosses the relocated bank. Remove
        # only its raised portion above the case floor (z=0), preserving floor.
        if not any(root.sketches.item(i).name == 'Clear obsolete battery rail from old position'
                   for i in range(root.sketches.count)):
            old_rail = root.sketches.add(offset_plane(root, root.xYConstructionPlane, 0.0))
            old_rail.name = 'Clear obsolete battery rail from old position'
            rect(old_rail, 49.0, 102.5, 183.0, 104.5)
            cut = root.features.extrudeFeatures.createInput(old_rail.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
            cut.participantBodies = [case]
            cut.setDistanceExtent(False, adsk.core.ValueInput.createByReal(7.0/MM))
            root.features.extrudeFeatures.add(cut)

        # Rebuild the battery rails around the new envelope, 1 mm away from the
        # bank perimeter. The front rail is interrupted at the cable exit.
        if not any(root.sketches.item(i).name == 'INIU bank retention rails at relocated fit-check position'
                   for i in range(root.sketches.count)):
            rails = root.sketches.add(offset_plane(root, root.xYConstructionPlane, -2.0))
            rails.name = 'INIU bank retention rails at relocated fit-check position'
            for r in [
                (49, 53.5, 108, 55.5), (124, 53.5, 183, 55.5),
                (49, 128.5, 183, 130.5),
                (46.5, 56.5, 48.5, 87.0), (46.5, 101.5, 48.5, 127.5),
                (183.5, 56.5, 185.5, 87.0), (183.5, 101.5, 185.5, 127.5)
            ]:
                rect(rails, *r)
            for i in range(rails.profiles.count):
                extrude(root, rails.profiles.item(i), 8.5, adsk.fusion.FeatureOperations.JoinFeatureOperation, case)

        # Pi Zero + Waveshare 4-port USB Hub HAT board envelope: 65 x 30 mm.
        # Stack below the carrier is conservatively 14 mm, Z=19..33. Its exact
        # connector/pogo-pin projection varies; this block is a keepout, not CAD.
        fit = root
        moved_bank = box(fit, 'INIU BI-B5 power bank relocated clear of Pi/HAT',
                         [49.0, 56.5, 0.5, 183.0, 127.5, 26.0], '134 x 71 x 25.5 mm')
        created.append(moved_bank)
        bank.isVisible = False
        bank.name = 'INIU BI-B5 centered position (legacy, hidden)'
        pi_hat = box(fit, 'Pi Zero 2 W + Waveshare USB Hub HAT underside stack',
                     [29.5, 25.0, 19.0, 94.5, 55.0, PCB_BOTTOM], '65 x 30 x 14 mm estimate')
        created.append(pi_hat)

        # Scale-positioned top-side devices. CardKB and Chameleon dimensions are
        # from their published product dimensions. LILYGO outline and placement
        # follow A2's footprint on the live EasyEDA PCB (height remains an estimate).
        created.append(box(fit, 'M5Stack CardKB', [20.7, 23.9, PCB_TOP, 105.3, 78.1, PCB_TOP+6.5],
                           '84.6 x 54.2 x 6.5 mm'))
        created.append(box(fit, 'Chameleon Ultra SE3', [159.0, 93.0, PCB_TOP, 199.0, 117.0, PCB_TOP+8.0],
                           '40 x 24 x 8 mm published nominal device body'))
        created.append(box(fit, 'LILYGO T-Display-S3 AMOLED 1.91', [189.547, 27.267, PCB_TOP, 215.047, 81.083, PCB_TOP+10.0],
                           '25.5 x 53.85 x 10 mm envelope; A2 live EasyEDA outline/placement, estimated height'))

        # Five 6 x 6 x 4 mm tactile button envelopes at current PCB footprint
        # centers, plus the rotary encoder. Locations converted from the live
        # EasyEDA export using the audited board datum.
        buttons = {
            'BACK button': (157.0, 44.0), 'MENU button': (157.0, 34.0),
            'UP button': (169.0, 44.0), 'DOWN button': (182.0, 39.0),
            'SELECT button': (169.0, 34.0)
        }
        for name, (cx, cy) in buttons.items():
            created.append(box(fit, name, [cx-3, cy-3, PCB_TOP, cx+3, cy+3, PCB_TOP+4], '6 x 6 x 4 mm'))
        # Round rotary-encoder shaft/body envelope at the PCB footprint center.
        enc_sk = fit.sketches.add(offset_plane(fit, fit.xYConstructionPlane, PCB_TOP))
        enc_sk.name = 'Rotary encoder 12 mm fit-check footprint'
        enc_sk.sketchCurves.sketchCircles.addByCenterRadius(pt(172.0, 62.3), 6.0/MM)
        en = extrude(fit, enc_sk.profiles.item(0), 14.0, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        enc = en.bodies.item(0)
        enc.name = 'Rotary encoder - 12 x 14 mm fit-check envelope'
        created.append(enc)

        # Stand-off fit checks at the existing four PCB mounting-hole centers.
        # PCB clearance holes are Ø6.299; M3 case holes are Ø3.2. A 10 mm OD
        # ring supports the board flat; a top washer spans the PCB clearance hole.
        supports = [(16,16),(16,116),(213.55,16),(213.55,114.61)]
        support_sk = fit.sketches.add(offset_plane(fit, fit.xYConstructionPlane, 0.0))
        support_sk.name = 'M3 PCB standoffs OD10 ID3.2 at current board holes'
        for x, y in supports:
            support_sk.sketchCurves.sketchCircles.addByCenterRadius(pt(x,y), 5.0/MM)
            support_sk.sketchCurves.sketchCircles.addByCenterRadius(pt(x,y), 1.6/MM)
        for i in range(support_sk.profiles.count):
            prof = support_sk.profiles.item(i)
            if prof.profileLoops.count == 2:
                post = extrude(fit, prof, PCB_BOTTOM, adsk.fusion.FeatureOperations.NewBodyFeatureOperation).bodies.item(0)
                post.name = 'PCB support ring OD10 ID3.2 height33 - fit-check'
                created.append(post)
        washer_sk = fit.sketches.add(offset_plane(fit, fit.xYConstructionPlane, PCB_TOP))
        washer_sk.name = 'M3 washers OD10 ID3.2 above PCB clearance holes'
        for x, y in supports:
            washer_sk.sketchCurves.sketchCircles.addByCenterRadius(pt(x,y), 5.0/MM)
            washer_sk.sketchCurves.sketchCircles.addByCenterRadius(pt(x,y), 1.6/MM)
        for i in range(washer_sk.profiles.count):
            prof = washer_sk.profiles.item(i)
            if prof.profileLoops.count == 2:
                w = extrude(fit, prof, 1.0, adsk.fusion.FeatureOperations.NewBodyFeatureOperation).bodies.item(0)
                w.name = 'M3 washer OD10 ID3.2 x1 fit-check'
                created.append(w)

        # Hide the two tiny legacy floating cylinders rather than deleting them;
        # their purpose is unclear and they should not obscure the current fit.
        hidden = []
        for name in ('Body26', 'Body27'):
            b = find_body(root, name)
            if b:
                b.isVisible = False
                b.name = name + ' - legacy cylinder reference (hidden)'
                hidden.append(name)

        # Retain all geometry visible for review. The new occurrence can be
        # toggled as one group in the Fusion browser.
        app.activeViewport.fit()
        doc.save('Added Pi/HAT underside and device fit checks; moved bank clear of HAT')

        # Update auditable placement and conservative clearance calculations.
        bank_bounds = body_bounds(moved_bank)
        pi_bounds = [29.5,25.0,19.0,94.5,55.0,33.0]
        x_gap = round(bank_bounds[0] - pi_bounds[3], 3)
        y_gap = round(bank_bounds[1] - pi_bounds[4], 3)
        audit = {}
        if os.path.isfile(AUDIT):
            with open(AUDIT, 'r') as f:
                audit = json.load(f)
        audit['piAndHubHatUnderside'] = {
            'model': 'Raspberry Pi Zero 2 W with Waveshare 4-Port USB Hub HAT',
            'boardFootprintMm': [65.0,30.0],
            'boardBoundsMm': pi_bounds,
            'boardSource': 'https://www.waveshare.com/product/raspberry-pi/hats/interface-power/usb-hub-hat-b.htm',
            'protrusionBelowPcbMm': 14.0,
            'zBoundsMm': [19.0,33.0],
            'protrusionAssumption': 'Conservative envelope for the Pi/HAT board, underside USB/pogo/connector hardware and mating stack; exact HAT revision and connector stack height not measured.',
            'batteryBoundsMm': bank_bounds,
            'separationMm': {'x': x_gap, 'y': y_gap},
            'overlapStatus': 'No nominal 3D intersection; battery is moved to y=56.5..127.5 mm. Nominal edge clearance from the underside envelope is 1.5 mm in Y, with 7 mm Z overlap, so verify the actual connector projection before printing.'
        }
        audit['powerBank'] = {
            'model': 'INIU BI-B5 20000 mAh', 'nominalSizeMm': [134.0,71.0,25.5],
            'boundsMm': bank_bounds, 'source': 'https://manuals.plus/asin/B09XZZKKSW',
            'placement': 'Moved 26 mm toward rear to clear Pi Zero + hub HAT underside stack and PCB corner supports; USB-C reaches the existing front opening via an assumed short extension lead.'
        }
        audit['powerBankRetention'] = {
            'style': 'repositioned partial rails joined to case floor', 'wallThicknessMm': 2.0,
            'nominalGapFromBankMm': 0.5, 'heightAboveFloorMm': 6.5,
            'bankEnvelopeMm': bank_bounds,
            'cableExit': 'front rail opening x=108..124 mm for a short USB-C extension lead.'
        }
        audit['componentFitEnvelopes'] = {
            'CardKB': {'dimensionsMm':[84.6,54.2,6.5], 'boundsMm':[20.7,23.9,34.6,105.3,78.1,41.1], 'source':'https://docs.m5stack.com/en/hat/Hat_CardKB'},
            'ChameleonUltra': {'dimensionsMm':[40,24,8], 'boundsMm':[159,93,34.6,199,117,42.6], 'source':'https://github.com/ChameleonUltra/docs/blob/main/hardware.md'},
            'LilyGoTDisplayS3Amoled': {'dimensionsMm':[25.5,53.85,10], 'boundsMm':[189.547,27.267,34.6,215.047,81.083,44.6], 'estimate':True, 'orientation':'portrait, A2 rotation 0', 'source':'EasyEDA cyberdeck-completed / PCB_cyberdeck-completed A2; height from https://github.com/Xinyuan-LILYGO/LilyGo-AMOLED-Series'},
            'buttons': {k: [v[0],v[1],6,6,4] for k,v in buttons.items()},
            'rotaryEncoder': {'centerMm':[172,62.3], 'bodyEnvelopeMm':[12,12,14], 'estimate':True}
        }
        audit['pcbSupportFit'] = {
            'pcbHoleDiameterMm': 6.299, 'caseM3HoleDiameterMm': 3.2,
            'supportRingMm': {'outerDiameter':10.0, 'innerDiameter':3.2, 'height':33.0},
            'washerMm': {'outerDiameter':10.0, 'innerDiameter':3.2, 'thickness':1.0},
            'mountCentersMm': supports,
            'note': 'Different diameters are intentional: PCB holes are M3 clearance/large fit-check holes; case bores are M3 screw clearance. The larger support rings bear on PCB material outside the Ø6.299 hole; top washers span the board hole so it can clamp flat.'
        }
        audit['mechanicalCautions'] = [
            'Pi/HAT underside stack is a conservative 14 mm envelope, not revision-specific STEP geometry. Measure the actual through-board connector/pogo projection; current model leaves only 1.5 mm nominal Y edge clearance to the relocated power bank.',
            'The INIU BI-B5 bank is shifted 26 mm toward the rear. Its USB-C connection uses an assumed short extension lead through the existing front case opening; confirm the actual bank port face/orientation.',
            'CardKB and Chameleon dimensions are vendor-published; LILYGO A2 outline/placement follows EasyEDA but its 10 mm height and button/encoder heights are estimates. Confirm exact module revision before printing.',
            'PCB support rings and washers are shown as fit-check parts. Choose screw length and washer style after measuring the actual case and board stack.',
            'The 7-inch lid display and closed-lid component/cable clearance still need physical revision-specific checking.'
        ]
        audit['legacyGeometryHidden'] = hidden
        with open(AUDIT, 'w') as f:
            json.dump(audit, f, indent=2)
        ui.messageBox('Fit-check updated. The Pi/HAT underside envelope is separated from the relocated battery by 1.5 mm nominal in Y (their Z ranges overlap by 7 mm, so that clearance is essential). PCB/case positions were retained. Added module envelopes and 10 mm support rings with M3 bores; legacy cylinders were hidden, not deleted. Inspect actual HAT connector height and bank USB-C orientation before printing.')
    except:
        if ui:
            ui.messageBox('Fit-check update stopped. Check the Fusion timeline for any partial features; the PCB and lid were not moved.\n\n' + traceback.format_exc())


def stop(context):
    pass
