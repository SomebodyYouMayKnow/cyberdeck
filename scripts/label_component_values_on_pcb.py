"""Add readable top-silkscreen function/value labels to the two-layer PCB candidate."""
import copy
import importlib.util
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'PCB/PCB_cyberdeck-completed-two-layer-case-mounts-2026-10-17.json'
OUTPUT = ROOT / 'PCB/PCB_cyberdeck-completed-labeled-2026-10-17.json'
REPORT = ROOT / 'PCB/component-label-audit-2026-10-17.json'
SCALE = 0.254  # EasyEDA coordinate units in mm
ORIGIN = (4047.559, 3047.847)


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'work' / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


fingerprint = module('label_glyph_source', 'build-fingerprint.py')
labels = fingerprint.labels
glyphs = fingerprint.all_glyphs()
pcb = json.loads(INPUT.read_text(encoding='utf-8-sig'))
original = copy.deepcopy(pcb)


def text_bbox(text):
    probe = labels.make_text(text, 0, 0, 'ggeTextProbe', 1.0, 0.15, 3, glyphs).split('~')
    nums = list(map(float, re.findall(r'[-+]?(?:\d*\.\d+|\d+\.?\d*)', probe[11])))
    return (min(nums[::2]), min(nums[1::2]), max(nums[::2]), max(nums[1::2]))


def put_center(text, xraw, ytopraw, identity, height=1.0, stroke=0.15):
    bx0, by0, bx1, by1 = text_bbox(text)
    width_mm = (bx1 - bx0) * SCALE * height
    x_mm = (xraw - ORIGIN[0]) * SCALE - width_mm / 2
    y_mm = (ytopraw - ORIGIN[1]) * SCALE
    record = labels.make_text(text, x_mm, y_mm, identity, height, stroke, 3, glyphs)
    pcb['shape'].append(record)
    fields = record.split('~')
    vals = list(map(float, re.findall(r'[-+]?(?:\d*\.\d+|\d+\.?\d*)', fields[11])))
    bbox = (min(vals[::2]), min(vals[1::2]), max(vals[::2]), max(vals[1::2]))
    return {'text': text, 'id': identity, 'bbox_mm_from_outline': [round((bbox[0] - ORIGIN[0]) * SCALE, 2), round((bbox[1] - ORIGIN[1]) * SCALE, 2), round((bbox[2] - ORIGIN[0]) * SCALE, 2), round((bbox[3] - ORIGIN[1]) * SCALE, 2)]}


def put_sign(kind, xraw, yraw, identity, size_mm=0.75, stroke_mm=0.15):
    # Native EasyEDA top-silk strokes; signs sit next to, not on, the electrical pad.
    half = size_mm / SCALE / 2
    width = stroke_mm / SCALE
    cx, cy = xraw, yraw
    lines = [[(cx-half, cy), (cx+half, cy)]]
    if kind == '+':
        lines.append([(cx, cy-half), (cx, cy+half)])
    elif kind != '-':
        raise ValueError(kind)
    out = []
    for i, (a, b) in enumerate(lines):
        out.append(f'TRACK~{width:.6f}~3~~{a[0]:.6f} {a[1]:.6f} {b[0]:.6f} {b[1]:.6f}~{identity}_{i+1}~0')
    pcb['shape'].extend(out)
    return {'symbol': kind, 'id': identity, 'center_mm_from_outline': [round((cx - ORIGIN[0]) * SCALE, 2), round((cy - ORIGIN[1]) * SCALE, 2)], 'size_mm': size_mm}


# Center labels on the component rows; locations are derived from the saved footprint centers.
text_plan = [
    ('BACK', 4610.55, 3335.0, 'silk_BACK', 1.0),
    ('UP', 4657.794, 3335.0, 'silk_UP', 1.0),
    ('MENU', 4610.55, 3374.0, 'silk_MENU', 1.0),
    # Place SELECT below the encoder push switch. Above it is too close to the
    # switch's two signal pads, so keep the text clear of copper and solder mask.
    ('SELECT', 4657.794, 3420.0, 'silk_SELECT', 1.0),
    ('DOWN', 4708.975, 3355.0, 'silk_DOWN', 1.0),
    ('ENTER', 4669.605, 3315.0, 'silk_ENTER', 1.0),
    ('1K', 4287.5, 3215.0, 'silk_R5_1K', 1.0),
    ('100R', 4243.0, 3190.0, 'silk_R6_100R', 1.0),
    ('2N2222', 4287.5, 3173.0, 'silk_Q1_2N2222', 1.0),
    ('IR LED', 4065.0, 3384.0, 'silk_D1_IR_LED', 1.0),
    ('100NF X4', 4514.5, 3184.0, 'silk_ceramic_100NF_x4', 1.0),
    ('100NF', 4242.5, 3197.0, 'silk_C9_100NF', 0.9),
    ('10K', 4414.0, 3158.083, 'silk_R7_10K', 0.8),
    ('10K', 4414.0, 3173.831, 'silk_R8_10K', 0.8),
    ('10K', 4414.0, 3189.579, 'silk_R10_10K', 0.8),
    ('10K', 4414.0, 3205.327, 'silk_R9_10K', 0.8),
]
for cx, ref in zip([4116, 4146, 4176, 4206], ['C12', 'C13', 'C15', 'C17']):
    text_plan.append(('10UF', cx, 3183.0, f'silk_{ref}_10UF', 0.8))

added_text = [put_center(*item) for item in text_plan]

# Mark polarity from the saved netlist: D1 pin 1 is IR_LED_A (+), pin 2 is IR_LED_K (-);
# C12/C13/C15/C17 pin 1 goes to a positive rail and pin 2 to GND.
polarity = []
for xplus, xminus, y, ref in [
    (4112.063, 4119.937, 3202.0, 'C12'),
    (4142.063, 4149.937, 3202.0, 'C13'),
    (4172.063, 4179.937, 3202.0, 'C15'),
    (4202.063, 4209.937, 3202.0, 'C17'),
    (4060.0, 4070.0, 3405.0, 'D1'),
]:
    polarity.append(put_sign('+', xplus, y, f'silk_{ref}_plus'))
    polarity.append(put_sign('-', xminus, y, f'silk_{ref}_minus'))

# Pad-collision screen for all added glyphs using native text paths and the actual pad records.
pads = []
for shape in original['shape']:
    if not shape.startswith('LIB~'):
        continue
    for child in shape.split('#@$'):
        if child.startswith('PAD~'):
            f = child.split('~')
            pads.append({'x': float(f[2]), 'y': float(f[3]), 'w': float(f[4]), 'h': float(f[5]), 'net': f[7], 'pin': f[8]})
text_errors = []
for label in added_text:
    r = next(s for s in pcb['shape'] if s.startswith('TEXT~L~') and label['id'] in s)
    f = r.split('~'); vals = list(map(float, re.findall(r'[-+]?(?:\d*\.\d+|\d+\.?\d*)', f[11])))
    bb = [min(vals[::2]) - float(f[4])/2, min(vals[1::2]) - float(f[4])/2, max(vals[::2]) + float(f[4])/2, max(vals[1::2]) + float(f[4])/2]
    for pad in pads:
        pb = [pad['x'] - pad['w']/2, pad['y'] - pad['h']/2, pad['x'] + pad['w']/2, pad['y'] + pad['h']/2]
        if bb[0] < pb[2] and bb[2] > pb[0] and bb[1] < pb[3] and bb[3] > pb[1]:
            text_errors.append({'label': label['text'], 'label_id': label['id'], 'pad_net': pad['net'], 'pad_pin': pad['pin']})
if text_errors:
    raise RuntimeError('Silkscreen text overlaps pads: ' + json.dumps(text_errors))

assert len([s for s in pcb['shape'] if s.startswith('LIB~')]) == len([s for s in original['shape'] if s.startswith('LIB~')])
assert len([s for s in pcb['shape'] if s.startswith('HOLE~')]) == len([s for s in original['shape'] if s.startswith('HOLE~')])
assert all(a == b for a, b in zip(pcb['shape'][:len(original['shape'])], original['shape']))
OUTPUT.write_text(json.dumps(pcb, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
report = {
    'status': 'PASS_STATIC_LABEL_AND_PAD_CHECK',
    'input': str(INPUT.relative_to(ROOT)),
    'output': str(OUTPUT.relative_to(ROOT)),
    'text_labels': added_text,
    'polarity_marks': polarity,
    'pad_overlaps': text_errors,
    'components_positions_tracks_nets_and_holes_unchanged': True,
    'note': 'Labels and signs are top-silkscreen geometry on a candidate export. Confirm readability and silk-to-mask clearances in EasyEDA DRC/preview before manufacturing.'
}
REPORT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': report['status'], 'label_count': len(added_text), 'polarity_mark_count': len(polarity), 'output': report['output']}, indent=2))
