import adsk.core
import adsk.fusion
import json
import traceback


MM = 10.0  # Fusion's internal length unit is centimeters.
HOLE_DIA_MM = 3.2  # M3 clearance through-hole.

# Tab centers measured from Sketch1 line geometry in the active case:
# top and bottom tab outlines, plus the four side tab outlines.
TAB_CENTERS_MM = [
    (63.35, 125.245, 'top-left'),
    (168.38, 125.245, 'top-right'),
    (63.45, 6.955, 'bottom-left'),
    (163.125, 6.955, 'bottom-right'),
    (7.125, 93.415, 'left-upper'),
    (7.125, 38.40, 'left-lower'),
    (224.875, 93.415, 'right-upper'),
    (224.875, 38.405, 'right-lower'),
]

OUT_JSON = (r'C:\Users\matth\Documents\Codex\2026-09-29\cyberdeck-electrical-engineering'
            r'\cad\case_hole_final_audit.json')


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError('No active Fusion design.')
        root = design.rootComponent
        sketch = next((root.sketches.item(i) for i in range(root.sketches.count)
                       if root.sketches.item(i).name == 'Sketch1'), None)
        if not sketch:
            raise RuntimeError('Root Sketch1 was not found.')

        circles = sketch.sketchCurves.sketchCircles
        if circles.count != 8:
            raise RuntimeError('Expected the 8 corrected case-tab holes before widening the left tabs; found {}. No geometry changed.'.format(circles.count))

        # Guard against deleting circles that are not in the lip/tab regions.
        intended = [(x, y) for x, y, _ in TAB_CENTERS_MM]
        old_data = []
        for i in range(circles.count):
            circle = circles.item(i)
            center = circle.geometry.center
            x, y = center.x * MM, center.y * MM
            old_left = ((9.0, 93.415), (9.0, 38.40))
            if not any(abs(x - tx) <= 4.5 and abs(y - ty) <= 4.5 for tx, ty in intended + list(old_left)):
                raise RuntimeError('Found a circle outside the measured case-tab regions at ({:.3f}, {:.3f}) mm. No geometry changed.'.format(x, y))
            old_data.append({'x': round(x, 6), 'y': round(y, 6),
                             'diameterMm': round(circle.geometry.radius * 2 * MM, 6)})

        sketch.isComputeDeferred = True
        created = []
        if circles.count == 8:
            # Preserve all six unaffected holes. Move only the two left holes
            # outward by the difference between the 4 mm and 7.75 mm tabs.
            old_left_centers = ((9.0, 93.415), (9.0, 38.40))
            expected = list(TAB_CENTERS_MM)
            for i in range(circles.count - 1, -1, -1):
                c = circles.item(i)
                p = c.geometry.center
                x_mm, y_mm = p.x * MM, p.y * MM
                if abs(c.geometry.radius * 2 * MM - HOLE_DIA_MM) > 0.001:
                    raise RuntimeError('A case-tab hole is not Ø3.2 mm.')
                if any(abs(x_mm - ox) < 0.001 and abs(y_mm - oy) < 0.001 for ox, oy in old_left_centers):
                    c.deleteMe()
            circles = sketch.sketchCurves.sketchCircles
            for x_mm, y_mm, label in TAB_CENTERS_MM:
                matching = [circles.item(i) for i in range(circles.count)
                            if abs(circles.item(i).geometry.center.x * MM - x_mm) < 0.001
                            and abs(circles.item(i).geometry.center.y * MM - y_mm) < 0.001]
                if not matching:
                    center = adsk.core.Point3D.create(x_mm / MM, y_mm / MM, 0)
                    circle = circles.addByCenterRadius(center, (HOLE_DIA_MM / 2) / MM)
                    if not circle:
                        raise RuntimeError('Fusion could not place the {} hole.'.format(label))
                    c = circle
                else:
                    c = matching[0]
                p = c.geometry.center
                x_actual, y_actual = p.x * MM, p.y * MM
                if abs(x_actual - x_mm) > 0.001 or abs(y_actual - y_mm) > 0.001:
                    raise RuntimeError('Hole coordinate check failed for {}.'.format(label))
                created.append({'label': label, 'xMm': round(x_actual, 6),
                                'yMm': round(y_actual, 6),
                                'xFromPcbOriginMm': round(x_actual - 11.0, 6),
                                'yFromPcbOriginMm': round(y_actual - 11.0, 6),
                                'diameterMm': round(c.geometry.radius * 2 * MM, 6)})
        else:
            # Replace only the nine old mounting circles or one partial retry
            # circle. Board outline and other sketch lines are preserved.
            for i in range(circles.count - 1, -1, -1):
                if not circles.item(i).deleteMe():
                    raise RuntimeError('Fusion could not delete an old mounting circle.')
            for x_mm, y_mm, label in TAB_CENTERS_MM:
                center = adsk.core.Point3D.create(x_mm / MM, y_mm / MM, 0)
                circle = circles.addByCenterRadius(center, (HOLE_DIA_MM / 2) / MM)
                if not circle:
                    raise RuntimeError('Fusion could not create the {} hole.'.format(label))
                actual = circle.geometry
                created.append({'label': label, 'xMm': round(actual.center.x * MM, 6),
                                'yMm': round(actual.center.y * MM, 6),
                                'xFromPcbOriginMm': round(actual.center.x * MM - 11.0, 6),
                                'yFromPcbOriginMm': round(actual.center.y * MM - 11.0, 6),
                                'diameterMm': round(actual.radius * 2 * MM, 6)})

        # Widen each left tab from 4.00 mm to 7.75 mm, matching the right tabs.
        # Replace only its three outline segments; preserve all other sketch
        # lines and the main board outline.
        left_tab_y = [(98.42, 88.41), (43.40, 33.40)]
        tab_segments = []
        lines = sketch.sketchCurves.sketchLines
        for i in range(lines.count):
            line = lines.item(i)
            a, b = line.geometry.startPoint, line.geometry.endPoint
            p1, p2 = (a.x * MM, a.y * MM), (b.x * MM, b.y * MM)
            for y_top, y_bottom in left_tab_y:
                segment = [p1, p2]
                if (any(abs(p[0] - 11.0) < 0.01 and abs(p[1] - y_top) < 0.01 for p in segment)
                    and any(abs(p[0] - 7.0) < 0.01 and abs(p[1] - y_top) < 0.01 for p in segment)) or \
                   (all(abs(p[0] - 7.0) < 0.01 for p in segment)
                    and {round(p[1], 2) for p in segment} == {round(y_top, 2), round(y_bottom, 2)}) or \
                   (any(abs(p[0] - 7.0) < 0.01 and abs(p[1] - y_bottom) < 0.01 for p in segment)
                    and any(abs(p[0] - 11.0) < 0.01 and abs(p[1] - y_bottom) < 0.01 for p in segment)):
                    tab_segments.append(line)
                    break
        if len(tab_segments) != 6:
            raise RuntimeError('Expected 6 left-tab outline segments to widen; found {}.'.format(len(tab_segments)))
        for line in tab_segments:
            line.deleteMe()
        lines = sketch.sketchCurves.sketchLines
        for y_top, y_bottom in left_tab_y:
            p11t = adsk.core.Point3D.create(11.0 / MM, y_top / MM, 0)
            p3t = adsk.core.Point3D.create(3.25 / MM, y_top / MM, 0)
            p3b = adsk.core.Point3D.create(3.25 / MM, y_bottom / MM, 0)
            p11b = adsk.core.Point3D.create(11.0 / MM, y_bottom / MM, 0)
            lines.addByTwoPoints(p11t, p3t)
            lines.addByTwoPoints(p3t, p3b)
            lines.addByTwoPoints(p3b, p11b)
        widened_left_tabs = True

        # Remove the isolated almost-overlapping segment that created the
        # visible stray point just below the bottom-left tab.
        removed_stray_segment = False
        lines = sketch.sketchCurves.sketchLines
        for i in range(lines.count - 1, -1, -1):
            line = lines.item(i)
            a, b = line.geometry.startPoint, line.geometry.endPoint
            ends = [(a.x * MM, a.y * MM), (b.x * MM, b.y * MM)]
            target = [(58.35, 11.0), (58.35, 3.04)]
            if all(any(abs(p[0] - q[0]) < 0.01 and abs(p[1] - q[1]) < 0.01 for q in target) for p in ends):
                if not line.deleteMe():
                    raise RuntimeError('Fusion could not remove the stray bottom-left segment.')
                removed_stray_segment = True

        sketch.isComputeDeferred = False
        if len(created) != 8 or any(abs(h['diameterMm'] - HOLE_DIA_MM) > 0.001 for h in created):
            raise RuntimeError('Post-edit check failed: wrong count or diameter.')

        audit = {
            'document': design.parentDocument.name,
            'sketch': sketch.name,
            'units': 'mm',
            'boardOuterSizeMm': [232, 132],
            'pcbBaseSizeMm': [210, 110],
            'pcbBaseBottomLeftInSketchMm': [11, 11],
            'holeSpecification': '8 x Ø3.2 mm, M3 clearance, centered on each case tab',
            'leftTabProjectionMm': 7.75,
            'leftTabHoleOffsetFromPcbEdgeMm': 3.875,
            'geometry': 'Created at exact coordinates and radius; left unconstrained to avoid overconstraining existing sketch geometry.',
            'circlesAtStart': len(old_data),
            'holes': created,
            'removedStrayBottomLeftSegment': removed_stray_segment,
            'leftTabsWidened': widened_left_tabs,
            'lineGeometryModified': bool(removed_stray_segment or widened_left_tabs),
            'boardOutlineModified': False,
            'deviceOutlinesModified': False,
        }
        with open(OUT_JSON, 'w') as f:
            json.dump(audit, f, indent=2)
        ui.messageBox('Case-tab holes corrected and checked.\n\n8 holes: Ø3.2 mm M3 clearance\nAll centered on measured tab centers.\nBoard outline and other sketch geometry were left unchanged.\n\nAudit: ' + OUT_JSON)
    except:
        if ui:
            ui.messageBox('Case tab hole correction failed:\n' + traceback.format_exc())
    finally:
        try:
            if 'sketch' in locals() and sketch:
                sketch.isComputeDeferred = False
        except:
            pass


def stop(context):
    pass
