import adsk.core
import adsk.fusion
import json
import traceback

MM = 10.0  # Fusion API internal units are cm.
SKETCH_NAME = 'Sketch1'
RING_SKETCH_NAME = 'PCB Case HoldDown References'
DX_MM = 5.375
DY_MM = -1.39
HOLE_DIA_MM = 3.2
RING_OUTER_DIA_MM = 6.5
OUT_JSON = r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering\cad\fusion_mount_correction_audit.json'


def near(a, b, tol=0.01):
    return abs(a-b) <= tol


def line_ends_mm(line):
    g = line.geometry
    return [(g.startPoint.x*MM, g.startPoint.y*MM), (g.endPoint.x*MM, g.endPoint.y*MM)]


def is_segment(line, a, b, tol=0.01):
    ends = line_ends_mm(line)
    return ((near(ends[0][0], a[0], tol) and near(ends[0][1], a[1], tol) and near(ends[1][0], b[0], tol) and near(ends[1][1], b[1], tol)) or
            (near(ends[1][0], a[0], tol) and near(ends[1][1], a[1], tol) and near(ends[0][0], b[0], tol) and near(ends[0][1], b[1], tol)))


def find_lines(lines, a, b):
    return [lines.item(i) for i in range(lines.count) if is_segment(lines.item(i), a, b)]


def circle_at(circles, x, y, diameter=None):
    found = []
    for i in range(circles.count):
        c = circles.item(i)
        p = c.geometry.center
        xx, yy, dd = p.x*MM, p.y*MM, c.geometry.radius*2*MM
        if near(xx, x, 0.001) and near(yy, y, 0.001) and (diameter is None or near(dd, diameter, 0.001)):
            found.append(c)
    return found


def add_line(lines, a, b):
    p1 = adsk.core.Point3D.create(a[0]/MM, a[1]/MM, 0)
    p2 = adsk.core.Point3D.create(b[0]/MM, b[1]/MM, 0)
    if not lines.addByTwoPoints(p1, p2):
        raise RuntimeError('Fusion failed to add line {} -> {}'.format(a, b))


def add_circle(circles, x, y, d):
    center = adsk.core.Point3D.create(x/MM, y/MM, 0)
    c = circles.addByCenterRadius(center, d/(2*MM))
    if not c:
        raise RuntimeError('Fusion failed to add circle at ({}, {}).'.format(x, y))
    return c


def run(context):
    ui = None
    sketch = None
    ring_sketch = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError('No active Fusion design.')
        root = design.rootComponent
        sketch = next((root.sketches.item(i) for i in range(root.sketches.count) if root.sketches.item(i).name == SKETCH_NAME), None)
        ring_sketch = next((root.sketches.item(i) for i in range(root.sketches.count) if root.sketches.item(i).name == RING_SKETCH_NAME), None)
        if not sketch or not ring_sketch:
            raise RuntimeError('Expected Sketch1 and PCB Case HoldDown References in the active document.')

        # Confirm the exact current bottom-right tab and hole, then shift the full tab +5.375 mm.
        old_x1, old_x2 = 157.9512, 168.2952
        new_x1, new_x2 = old_x1 + DX_MM, old_x2 + DX_MM
        y0, y1, ymid = 2.9099, 11.0, 5.0
        hole_x_old, hole_y = 163.125, 6.955
        hole_x_new = hole_x_old + DX_MM
        circles = sketch.sketchCurves.sketchCircles
        old_hole = circle_at(circles, hole_x_old, hole_y, HOLE_DIA_MM)
        if len(old_hole) != 1:
            raise RuntimeError('Expected exactly one bottom-right Ø3.2 hole at ({:.3f},{:.3f}); found {}. No edits applied.'.format(hole_x_old, hole_y, len(old_hole)))

        lines = sketch.sketchCurves.sketchLines
        expected_segments = [
            ((old_x1, 11.0), (old_x2, 11.0)),
            ((old_x2, 11.0), (old_x2, y0)),
            ((old_x2, y0), (old_x1, y0)),
            ((old_x1, y0), (old_x1, 11.0)),
            ((227.0, ymid), (old_x2, ymid)),
            ((old_x1, ymid), (68.5499, ymid)),
        ]
        matches = [find_lines(lines, a, b) for a, b in expected_segments]
        if any(len(m) != 1 for m in matches):
            raise RuntimeError('Bottom-right tab guard failed: expected one match for each of six exact outline segments, got {}. No edits applied.'.format([len(m) for m in matches]))

        # Ensure no geometry is already at the destination to avoid duplicates on reruns.
        if circle_at(circles, hole_x_new, hole_y, HOLE_DIA_MM):
            raise RuntimeError('Destination bottom-right hole already exists; no edits applied.')
        dest_segments = [
            ((new_x1, 11.0), (new_x2, 11.0)),
            ((new_x2, 11.0), (new_x2, y0)),
            ((new_x2, y0), (new_x1, y0)),
            ((new_x1, y0), (new_x1, 11.0)),
            ((227.0, ymid), (new_x2, ymid)),
            ((new_x1, ymid), (68.5499, ymid)),
        ]
        if any(find_lines(lines, a, b) for a, b in dest_segments):
            raise RuntimeError('Some bottom-right destination outline segments already exist; no edits applied.')

        # Validate the two right support-ring pairs before changing either.
        rc = ring_sketch.sketchCurves.sketchCircles
        if rc.count != 8:
            raise RuntimeError('Expected exactly 8 inner-ring circles; found {}. No edits applied.'.format(rc.count))
        right_old = [(213.55, 17.39), (213.55, 116.0)]
        ring_replacements = []
        for x, y in right_old:
            inner = circle_at(rc, x, y, HOLE_DIA_MM)
            outer = circle_at(rc, x, y, RING_OUTER_DIA_MM)
            if len(inner) != 1 or len(outer) != 1:
                raise RuntimeError('Expected one Ø3.2 and one Ø6.5 circle at ({},{}); got inner {}, outer {}. No edits applied.'.format(x, y, len(inner), len(outer)))
            ring_replacements.append((inner[0], outer[0], x, y, y + DY_MM))
        if circle_at(rc, 213.55, 16.0, HOLE_DIA_MM) or circle_at(rc, 213.55, 114.61, HOLE_DIA_MM):
            raise RuntimeError('Right support-ring destination already contains a hole; no edits applied.')

        # Apply the guarded changes. Keep all diameters and the other six lip holes unchanged.
        sketch.isComputeDeferred = True
        ring_sketch.isComputeDeferred = True
        for m in matches:
            if not m[0].deleteMe():
                raise RuntimeError('Fusion could not remove one of the six old tab outline segments.')
        for a, b in dest_segments:
            add_line(sketch.sketchCurves.sketchLines, a, b)
        if not old_hole[0].deleteMe():
            raise RuntimeError('Fusion could not replace the old bottom-right hole.')
        add_circle(sketch.sketchCurves.sketchCircles, hole_x_new, hole_y, HOLE_DIA_MM)

        for inner, outer, x, old_y, new_y in ring_replacements:
            if not inner.deleteMe() or not outer.deleteMe():
                raise RuntimeError('Fusion could not move right-side support pair at x={}, y={}.'.format(x, old_y))
            add_circle(ring_sketch.sketchCurves.sketchCircles, x, new_y, HOLE_DIA_MM)
            add_circle(ring_sketch.sketchCurves.sketchCircles, x, new_y, RING_OUTER_DIA_MM)

        sketch.isComputeDeferred = False
        ring_sketch.isComputeDeferred = False

        # Verify exact positions, circle diameters, sketch counts, and tab edges.
        v_circles = sketch.sketchCurves.sketchCircles
        if len(circle_at(v_circles, hole_x_new, hole_y, HOLE_DIA_MM)) != 1 or v_circles.count != 8:
            raise RuntimeError('Post-edit case-tab hole verification failed.')
        if any(find_lines(sketch.sketchCurves.sketchLines, a, b).__len__() != 1 for a, b in dest_segments):
            raise RuntimeError('Post-edit case-tab outline verification failed.')
        vr = ring_sketch.sketchCurves.sketchCircles
        for x, y in [(213.55, 16.0), (213.55, 114.61)]:
            if len(circle_at(vr, x, y, HOLE_DIA_MM)) != 1 or len(circle_at(vr, x, y, RING_OUTER_DIA_MM)) != 1:
                raise RuntimeError('Post-edit inner support-ring verification failed at ({},{})'.format(x, y))
        if vr.count != 8:
            raise RuntimeError('Inner support-ring count changed unexpectedly to {}.'.format(vr.count))

        audit = {
            'fusionDocument': design.parentDocument.name,
            'result': 'corrected and verified',
            'caseSketch': SKETCH_NAME,
            'bottomRightLipHole': {
                'oldCenterMm': [hole_x_old, hole_y],
                'newCenterMm': [hole_x_new, hole_y],
                'diameterMm': HOLE_DIA_MM,
                'shiftMm': [DX_MM, 0.0],
                'tabShiftedMm': [DX_MM, 0.0],
                'tabBoundsMm': {'xMin': new_x1, 'xMax': new_x2, 'yMin': y0, 'yMax': 11.0},
                'outlineSegmentsReplaced': 6
            },
            'rightInnerSupportRings': [
                {'name': 'CASE_TR', 'oldCenterMm': [213.55, 17.39], 'newCenterMm': [213.55, 16.0], 'innerDiameterMm': HOLE_DIA_MM, 'outerDiameterMm': RING_OUTER_DIA_MM},
                {'name': 'CASE_BR', 'oldCenterMm': [213.55, 116.0], 'newCenterMm': [213.55, 114.61], 'innerDiameterMm': HOLE_DIA_MM, 'outerDiameterMm': RING_OUTER_DIA_MM}
            ],
            'leftInnerSupportRingsChanged': False,
            'otherCaseLipHolesChanged': False,
            'sketchCounts': {'caseCircles': v_circles.count, 'caseLines': sketch.sketchCurves.sketchLines.count, 'mountCircles': vr.count}
        }
        with open(OUT_JSON, 'w') as f:
            json.dump(audit, f, indent=2)
        ui.messageBox('Fusion mount locations corrected and verified.\n\nBottom-right lip and its hole shifted +5.375 mm.\nRight inner support-ring pairs shifted -1.390 mm in Y.\nHole and ring diameters preserved.\n\nAudit: ' + OUT_JSON)
    except:
        if ui:
            ui.messageBox('Mount-location correction failed:\n' + traceback.format_exc())
    finally:
        try:
            if sketch:
                sketch.isComputeDeferred = False
            if ring_sketch:
                ring_sketch.isComputeDeferred = False
        except:
            pass


def stop(context):
    pass
