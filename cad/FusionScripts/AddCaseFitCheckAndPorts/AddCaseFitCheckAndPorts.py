"""Add scale fit-check geometry and conservative enclosure openings to live NEONRED Fusion case."""
import adsk.core
import adsk.fusion
import json
import math
import os
import traceback

MM = 10.0  # Fusion internal length unit is cm.
ROOT_DIR = r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering\cad'
AUDIT = os.path.join(ROOT_DIR, 'fusion_case_fit_and_ports_audit.json')
PCB_Z = 33.0
PCB_T = 1.6
BANK_Z = 0.5
BANK_SIZE = (134.0, 71.0, 25.5)  # INIU BI-B5 published/packaging dimension estimate.

# EasyEDA 2026-11-18 outline converted to mm and translated into the Fusion case datum.
# Exact perimeter includes all eight mounting lips and the 1.5 mm corner chamfers.
PCB_OUTLINE = [
    (11.0, 121.0), (58.5, 121.0), (58.5, 127.5), (60.0, 129.0),
    (67.0, 129.0), (68.5, 127.5), (68.5, 121.0), (163.5, 121.0),
    (163.5, 127.5), (165.0, 129.0), (172.0, 129.0), (173.5, 127.5),
    (173.5, 121.0), (221.0, 121.0), (221.0, 98.5), (227.5, 98.5),
    (229.0, 97.0), (229.0, 90.0), (227.5, 88.5), (221.0, 88.5),
    (221.0, 43.5), (227.5, 43.5), (229.0, 42.0), (229.0, 35.0),
    (227.5, 33.5), (221.0, 33.5), (221.0, 11.0), (173.5, 11.0),
    (173.5, 4.5), (172.0, 3.0), (165.0, 3.0), (163.5, 4.5),
    (163.5, 11.0), (68.5, 11.0), (68.5, 4.5), (67.0, 3.0),
    (60.0, 3.0), (58.5, 4.5), (58.5, 11.0), (11.0, 11.0),
    (11.0, 33.5), (4.5, 33.5), (3.0, 35.0), (3.0, 42.0),
    (4.5, 43.5), (11.0, 43.5), (11.0, 88.5), (4.5, 88.5),
    (3.0, 90.0), (3.0, 97.0), (4.5, 98.5), (11.0, 98.5), (11.0, 121.0)
]

# Hole locations are transformed from the committed EasyEDA export using the same
# PCB-to-case datum as the existing Fusion case sketch: board origin (3, 3) mm.
PCB_HOLES = [
    (16.0, 116.0, 6.299), (213.55, 114.61, 6.299),
    (16.0, 16.0, 6.299), (213.55, 16.0, 6.299),
    (63.5, 125.0, 6.299), (168.5, 125.0, 6.299),
    (225.0, 93.5, 6.299), (225.0, 38.5, 6.299),
    (168.5, 7.0, 6.299), (63.5, 7.0, 6.299),
    (7.0, 38.5, 6.299), (7.0, 93.5, 6.299),
    (16.5, 80.5, 5.415), (109.5, 80.5, 5.415),
    (16.5, 21.5, 5.415), (109.5, 21.5, 5.415),
    (153.0, 115.0, 5.415), (205.0, 115.0, 5.415),
    (153.0, 95.0, 5.415), (205.0, 95.0, 5.415),
]


def p(x, y, z=0):
    return adsk.core.Point3D.create(x / MM, y / MM, z / MM)


def offset_plane(comp, base, distance_mm):
    pi = comp.constructionPlanes.createInput()
    pi.setByOffset(base, adsk.core.ValueInput.createByReal(distance_mm / MM))
    return comp.constructionPlanes.add(pi)


def make_rect(sk, x0, y0, x1, y1):
    sk.sketchCurves.sketchLines.addTwoPointRectangle(p(x0, y0), p(x1, y1))


def make_polygon(sk, points):
    lines = sk.sketchCurves.sketchLines
    for a, b in zip(points[:-1], points[1:]):
        lines.addByTwoPoints(p(a[0], a[1]), p(b[0], b[1]))


def extrude_profile(comp, profile, distance_mm, operation, participant=None):
    inp = comp.features.extrudeFeatures.createInput(profile, operation)
    if participant is not None:
        inp.participantBodies = [participant]
    inp.setDistanceExtent(False, adsk.core.ValueInput.createByReal(distance_mm / MM))
    return comp.features.extrudeFeatures.add(inp)


def find_body(comp, exact_name):
    for i in range(comp.bRepBodies.count):
        body = comp.bRepBodies.item(i)
        if body.name == exact_name:
            return body
    return None


def make_rounded_slot(sk, cx, cy, width, height):
    """Simple rounded slot in a sketch plane; sketch coordinates are mm."""
    r = height / 2.0
    half_straight = (width - height) / 2.0
    left_cx, right_cx = cx - half_straight, cx + half_straight
    curves = sk.sketchCurves
    lines, arcs = curves.sketchLines, curves.sketchArcs
    # Top and bottom tangents.
    lines.addByTwoPoints(p(left_cx, cy + r), p(right_cx, cy + r))
    lines.addByTwoPoints(p(right_cx, cy - r), p(left_cx, cy - r))
    # Semi-circles, with tangent endpoints shared by adjacent straight lines.
    arcs.addByCenterStartSweep(p(right_cx, cy), p(right_cx, cy + r), -math.pi)
    arcs.addByCenterStartSweep(p(left_cx, cy), p(left_cx, cy - r), -math.pi)


def run(context):
    ui = None
    made = []
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError('No active Fusion design.')
        doc = app.activeDocument
        comp = design.rootComponent
        case = find_body(comp, 'Body1')
        if case is None:
            raise RuntimeError('Could not find existing Body1 case. Nothing was changed.')
        if find_body(comp, 'NEONRED PCB 226x126 fit-check') or find_body(comp, 'INIU BI-B5 power bank fit-check'):
            raise RuntimeError('The PCB/power-bank fit-check geometry already exists. No duplicate geometry added.')
        bb = case.boundingBox
        case_bounds = [bb.minPoint.x*MM, bb.minPoint.y*MM, bb.minPoint.z*MM,
                       bb.maxPoint.x*MM, bb.maxPoint.y*MM, bb.maxPoint.z*MM]
        if abs(case_bounds[3] - 232.0) > 0.5 or abs(case_bounds[4] - 143.3) > 1.0:
            raise RuntimeError('Case datum differs from audited Body1 (expected X max 232 mm and hinge-inclusive Y max about 143.3 mm). No geometry changed.')

        # Widen the original nominal 226 x 126 mm cavity by 1 mm per side.
        # This leaves the 226 x 126 mm PCB with 1 mm clearance while keeping the
        # existing outside dimensions, hinge, openings, and board hole datum intact.
        reliefs = [
            ('left', 2.0, 3.0, 3.0, 129.0),
            ('right', 229.0, 230.0, 3.0, 129.0),
            ('front', 3.0, 229.0, 2.0, 3.0),
            ('rear', 3.0, 229.0, 129.0, 130.0),
        ]
        for side, x0, x1, y0, y1 in reliefs:
            relief = comp.sketches.add(offset_plane(comp, comp.xYConstructionPlane, 0.0))
            relief.name = 'PCB 1 mm clearance relief ' + side
            make_rect(relief, x0, y0, x1, y1)
            cut = comp.features.extrudeFeatures.createInput(
                relief.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
            cut.participantBodies = [case]
            cut.setDistanceExtent(False, adsk.core.ValueInput.createByReal(50.0 / MM))
            comp.features.extrudeFeatures.add(cut)

        # Add a PCB silhouette at the exact outline scale and its actual mounting holes.
        pcb_sk = comp.sketches.add(offset_plane(comp, comp.xYConstructionPlane, PCB_Z))
        pcb_sk.name = 'EasyEDA PCB outline 226 x 126 mm, case datum x3 y3'
        make_polygon(pcb_sk, PCB_OUTLINE)
        pcb_ex = extrude_profile(comp, pcb_sk.profiles.item(0), PCB_T,
                                 adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        pcb = pcb_ex.bodies.item(0)
        pcb.name = 'NEONRED PCB 226x126 fit-check'
        made.append(pcb)

        holes_sk = comp.sketches.add(offset_plane(comp, comp.xYConstructionPlane, PCB_Z - 0.1))
        holes_sk.name = 'EasyEDA PCB NPTH holes, translated to case datum'
        for x, y, d in PCB_HOLES:
            holes_sk.sketchCurves.sketchCircles.addByCenterRadius(p(x, y), d / (2 * MM))
        for i in range(holes_sk.profiles.count):
            extrude_profile(comp, holes_sk.profiles.item(i), PCB_T + 0.2,
                            adsk.fusion.FeatureOperations.CutFeatureOperation, pcb)

        mount_centers = [(16.0,16.0),(213.55,16.0),(16.0,116.0),(213.55,114.61)]

        # Bank envelope centered in the clear space below the PCB.
        bank_x = (232.0 - BANK_SIZE[0]) / 2.0
        bank_y = (132.0 - BANK_SIZE[1]) / 2.0
        bank_sk = comp.sketches.add(offset_plane(comp, comp.xYConstructionPlane, BANK_Z))
        bank_sk.name = 'INIU BI-B5 power bank 134x71 mm footprint'
        make_rect(bank_sk, bank_x, bank_y, bank_x + BANK_SIZE[0], bank_y + BANK_SIZE[1])
        bank_ex = extrude_profile(comp, bank_sk.profiles.item(0), BANK_SIZE[2],
                                  adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        bank = bank_ex.bodies.item(0)
        bank.name = 'INIU BI-B5 power bank fit-check'
        made.append(bank)

        # Openings in the front wall. Five 10 x 6.5 mm slots accept SMA bulkhead
        # adapters/coax pigtails for 2x nRF24, ALFA, RTL-SDR, and ESP32 antennas.
        # The coax mapping is intentionally flexible because the RF parts are not
        # placed on the carrier at fixed connector coordinates.
        antenna_centers = [30.0, 72.0, 114.0, 156.0, 198.0]
        for n, x in enumerate(antenna_centers, 1):
            s = comp.sketches.add(offset_plane(comp, comp.xZConstructionPlane, -4.0))
            s.name = 'Antenna bulkhead clearance slot {} 10x6.5'.format(n)
            make_rounded_slot(s, x, 38.0, 10.0, 6.5)
            extrude_profile(comp, s.profiles.item(0), 8.0,
                            adsk.fusion.FeatureOperations.CutFeatureOperation, case)

        # Power-bank USB-C access from front wall (broad service slot).
        s = comp.sketches.add(offset_plane(comp, comp.xZConstructionPlane, -4.0))
        s.name = 'Power-bank USB-C service opening 14x7 mm'
        make_rect(s, 109.0, 8.0, 123.0, 15.0)
        extrude_profile(comp, s.profiles.item(0), 8.0,
                        adsk.fusion.FeatureOperations.CutFeatureOperation, case)

        # LILYGO USB-C access on the right case wall; nominal location is based on
        # the board's EasyEDA placement. It needs a short flexible pigtail if its
        # exact revision's port is not on this edge.
        right_sk = comp.sketches.add(offset_plane(comp, comp.yZConstructionPlane, 228.0))
        right_sk.name = 'LILYGO programming USB-C access slot 11x6 mm'
        # YZ local X maps to -world Z, local Y to world Y.
        make_rect(right_sk, -37.0, 76.0, -31.0, 87.0)
        extrude_profile(comp, right_sk.profiles.item(0), 8.0,
                        adsk.fusion.FeatureOperations.CutFeatureOperation, case)

        # IR ports on left side wall: wall openings are sized for 5 mm THT optical
        # components and a short printed light-pipe; board items are at x~15 mm,
        # so a light-pipe/reflector is required for direct optical alignment.
        ir_sk = comp.sketches.add(offset_plane(comp, comp.yZConstructionPlane, 4.0))
        ir_sk.name = 'IR LED and receiver side light-pipe ports Ø5.5 mm'
        for y in (31.7, 40.8):
            ir_sk.sketchCurves.sketchCircles.addByCenterRadius(
                p(-38.5, y), 5.5 / (2 * MM))
        for i in range(ir_sk.profiles.count):
            extrude_profile(comp, ir_sk.profiles.item(i), 8.0,
                            adsk.fusion.FeatureOperations.CutFeatureOperation, case)

        # Visibility: keep the model as a legible assembly instead of hiding real case parts.
        for body in made:
            body.isVisible = True
        app.activeViewport.fit()

        # Record verified coordinates plus explicit assumptions/fit cautions.
        def body_bounds(body):
            b = body.boundingBox
            return [round(b.minPoint.x*MM,3), round(b.minPoint.y*MM,3), round(b.minPoint.z*MM,3),
                    round(b.maxPoint.x*MM,3), round(b.maxPoint.y*MM,3), round(b.maxPoint.z*MM,3)]
        audit = {
            'document': doc.name, 'units': 'mm', 'status': 'fit-check geometry added to live Fusion case',
            'pcbSource': 'EasyEDA/PCB_cyberdeck-completed_2026-11-18.json; 226 x 126 mm board outline and NPTH pattern',
            'pcbBoundsMm': body_bounds(pcb), 'pcbThicknessMm': PCB_T,
            'pcbOutlinePlacement': {'caseXmm': 3, 'caseYmm': 3, 'clearancePerSideMm': 1},
            'pcbHoles': {'count': len(PCB_HOLES), 'caseScrewHolesMm': 6.299,
                         'CardKBAndChameleonHolesMm': 5.415, 'mountCentersMm': mount_centers},
            'caseClearanceReliefMm': {'from': [2,2], 'to': [230,130], 'perSideIncrease': 1,
                                      'outerCaseUnchanged': True},
            'powerBank': {'model': 'INIU BI-B5 20000 mAh', 'nominalSizeMm': list(BANK_SIZE),
                          'boundsMm': body_bounds(bank), 'source': 'https://manuals.plus/asin/B09XZZKKSW',
                          'placement': 'centered on enclosure floor below PCB; service port oriented toward front wall'},
            'existingSupports': {'keptInPlace': True, 'mountCentersMm': mount_centers,
                                 'note': 'The existing case already has support geometry; this update does not add overlapping posts.'},
            'caseOpenings': {
                'antennaSlots': {'count': 5, 'sizeMm': [10,6.5], 'centersXmm': antenna_centers,
                                 'centerZmm': 38, 'wall': 'front',
                                 'intendedFor': ['nRF24 #1', 'nRF24 #2', 'ALFA AWUS036ACS', 'RTL-SDR V4L', 'ESP32/LILYGO'],
                                 'routing': 'Use short coax pigtails/SMA bulkheads; exact dongle and radio connector positions are not fixed by the carrier PCB.'},
                'powerBankUsbC': {'boundsX_Z_mm': [109,8,123,15], 'wall': 'front'},
                'lilygoUsbC': {'boundsY_Z_mm': [76,31,87,37], 'wall': 'right', 'nominalOnly': True},
                'ir': {'diameterMm': 5.5, 'wall': 'left', 'centerYmm': [31.7,40.8],
                       'centerZmm': 38.5, 'lightPipeRequired': True}},
            'mechanicalCautions': [
                'The PCB is an unpopulated 1.6 mm fit-check silhouette; component heights, USB/HDMI cable bends, and connector orientations are not represented.',
                'The INIU BI-B5 size is a nominal external envelope (about 134 x 71 x 25.5 mm); case the actual unit before printing.',
                'Battery overlaps the PCB in plan view by design and is vertically separated by 7.0 mm. Check bottom-side solder leads and component protrusions; if they exceed this clearance, increase base height or route the bank beside the PCB.',
                'The IR apertures require short light pipes because the on-board vertical components sit inward from the left case wall.',
                'Antenna connector placements are flexible wall slots with coax leads, not direct fixed alignment to the radio modules.',
                'Confirm the LILYGO USB-C connector is on the modeled right edge before printing; the cutout is a fit-check access slot.'
            ]
        }
        with open(AUDIT, 'w') as f:
            json.dump(audit, f, indent=2)
        doc.save('Added scaled PCB and INIU bank fit-check, 1 mm clearance, antenna/IR/USB-C ports')
        ui.messageBox('Added a scale PCB outline and mounting holes, centered INIU BI-B5 power-bank envelope, four 33 mm support rings, 1 mm per-side interior relief, five antenna slots, two IR light-pipe holes, and USB-C access slots. The existing outer case/lid dimensions and screen placement were left unchanged. Review the assembly and fit-check notes before printing.')
    except:
        if ui:
            ui.messageBox('Case fit-check and port update stopped. Inspect the Fusion timeline for any partial features; no intentional move was made to the lid or display bodies.\n\n' + traceback.format_exc())


def stop(context):
    pass
