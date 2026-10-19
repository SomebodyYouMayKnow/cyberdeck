"""Append readable top-silkscreen function/value labels to a fresh EasyEDA export."""
import copy
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'outputs/PCB_PCB_cyberdeck-completed_2026-10-17.json'
OUTPUT = ROOT / 'outputs/PCB_cyberdeck-completed-labeled-2026-10-17.json'
REPORT = ROOT / 'outputs/PCB_cyberdeck-completed-label-audit-2026-10-17.json'
SCALE = 0.254
ORIGIN = (4047.559, 3047.847)

spec = importlib.util.spec_from_file_location('label_glyph_source', ROOT / 'work/build-fingerprint.py')
glyph_source = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = glyph_source
spec.loader.exec_module(glyph_source)
labels, glyphs = glyph_source.labels, glyph_source.all_glyphs()
pcb = json.loads(INPUT.read_text(encoding='utf-8-sig'))
original = copy.deepcopy(pcb)


def bbox_for(text):
    f = labels.make_text(text, 0, 0, 'probe', 1.0, 0.15, 3, glyphs).split('~')
    n = list(map(float, re.findall(r'[-+]?(?:\d*\.\d+|\d+\.?\d*)', f[11])))
    return min(n[::2]), min(n[1::2]), max(n[::2]), max(n[1::2])


def add_text(text, x_raw, y_raw, identity, height=1.0):
    x0, y0, x1, y1 = bbox_for(text)
    width_mm = (x1 - x0) * SCALE * height
    x_mm = (x_raw - ORIGIN[0]) * SCALE - width_mm / 2
    y_mm = (y_raw - ORIGIN[1]) * SCALE
    rec = labels.make_text(text, x_mm, y_mm, identity, height, 0.15, 3, glyphs)
    pcb['shape'].append(rec)
    f = rec.split('~')
    n = list(map(float, re.findall(r'[-+]?(?:\d*\.\d+|\d+\.?\d*)', f[11])))
    return {'text': text, 'id': identity, 'bbox': [min(n[::2])-float(f[4])/2, min(n[1::2])-float(f[4])/2,
                                                   max(n[::2])+float(f[4])/2, max(n[1::2])+float(f[4])/2]}


def add_sign(kind, x, y, identity, size_mm=0.75, stroke_mm=0.15):
    half, width = size_mm / SCALE / 2, stroke_mm / SCALE
    lines = [[(x-half, y), (x+half, y)]]
    if kind == '+':
        lines.append([(x, y-half), (x, y+half)])
    for i, (a, b) in enumerate(lines):
        pcb['shape'].append(f'TRACK~{width:.6f}~3~~{a[0]:.6f} {a[1]:.6f} {b[0]:.6f} {b[1]:.6f}~{identity}_{i+1}~0')


# Remove the crowded default value/reference silkscreen from the five tactile
# buttons. Their function legends below replace it, leaving one readable name
# per key. The user reports DOWN and SELECT were visually swapped, so print
# those two labels at the opposite button locations; electrical nets stay as-is.
button_centers = {
    (4610.552, 3350.9955),
    (4610.552, 3390.3655),
    (4657.792, 3350.9955),
    (4708.972, 3370.6855),
    (4657.792, 3390.3655),
}
for i, shape in enumerate(pcb['shape']):
    if not shape.startswith('LIB~'):
        continue
    fields = shape.split('~', 3)
    center = (round(float(fields[1]), 3), round(float(fields[2]), 3))
    if center in {(round(x, 3), round(y, 3)) for x, y in button_centers}:
        pieces = shape.split('#@$')
        pcb['shape'][i] = '#@$'.join([pieces[0]] + [p for p in pieces[1:] if not p.startswith(('TEXT~N~', 'TEXT~P~'))])

# One function label per tactile button. These positions are above, outside the
# 6x6 mm switch body, with DOWN and SELECT intentionally exchanged as requested.
plan = [
    ('BACK',   4610.552, 3370.0, 'silk_BACK', 0.9),
    ('UP',     4657.792, 3370.0, 'silk_UP', 0.9),
    ('MENU',   4610.552, 3414.0, 'silk_MENU', 0.9),
    ('DOWN',   4657.792, 3414.0, 'silk_DOWN', 0.9),
    ('SELECT', 4708.972, 3394.0, 'silk_SELECT', 0.9),
    ('ENTER',  4669.605, 3257.0, 'silk_ENTER', 0.9),
    # Group/value legends are placed in clear gaps; the individual footprints
    # retain their reference designators, so no long duplicate value strings
    # are added over pad rows.
    ('10K X8', 4280.0, 3069.5, 'silk_R_array_10Kx8', 0.75),
    ('100NF X4', 4220.0, 3130.0, 'silk_C_array_100NFx4', 0.75),
    ('100NF', 4225.0, 3228.0, 'silk_C9_100NF', 0.75),
    ('100R', 4250.0, 3160.0, 'silk_R6_100R', 0.75),
    ('1K', 4305.0, 3207.0, 'silk_R5_1K', 0.75),
    ('2N2222', 4287.5, 3158.0, 'silk_Q1_2N2222', 0.75),
]
text_records = [add_text(*row) for row in plan]

sign_records = []
for xplus, xminus, y, ref in [
    (4112.063,4119.937,3202,'C12'), (4142.063,4149.937,3202,'C13'),
    (4172.063,4179.937,3202,'C15'), (4202.063,4209.937,3202,'C17'),
    (4060,4070,3405,'D1')]:
    add_sign('+',xplus,y,f'silk_{ref}_plus'); add_sign('-',xminus,y,f'silk_{ref}_minus')
    sign_records.extend([{'ref':ref,'symbol':'+','x':xplus,'y':y},{'ref':ref,'symbol':'-','x':xminus,'y':y}])

pad_boxes=[]
for shape in original['shape']:
    if not shape.startswith('LIB~'): continue
    for child in shape.split('#@$'):
        if child.startswith('PAD~'):
            f=child.split('~'); pad_boxes.append([(float(f[2])-float(f[4])/2)*SCALE,(float(f[3])-float(f[5])/2)*SCALE,
                (float(f[2])+float(f[4])/2)*SCALE,(float(f[3])+float(f[5])/2)*SCALE])
overlaps=[]
for rec in text_records:
    b=rec['bbox']
    for p in pad_boxes:
        if b[0]<p[2] and b[2]>p[0] and b[1]<p[3] and b[3]>p[1]: overlaps.append(rec['id'])
if overlaps: raise RuntimeError('Text/pad overlap: '+json.dumps(overlaps))
text_overlaps=[]
for a in range(len(text_records)):
    for b in range(a+1, len(text_records)):
        aa, bb = text_records[a]['bbox'], text_records[b]['bbox']
        if aa[0] < bb[2] and aa[2] > bb[0] and aa[1] < bb[3] and aa[3] > bb[1]:
            text_overlaps.append([text_records[a]['text'], text_records[b]['text']])
if text_overlaps: raise RuntimeError('Label-to-label overlap: '+json.dumps(text_overlaps))

def path_bbox(rec, scale):
    f = rec.split('~')
    if len(f) < 12 or f[7] != '3' or not f[11].strip():
        return None
    nums = list(map(float, re.findall(r'[-+]?(?:\d*\.\d+|\d+\.?\d*)', f[11])))
    if len(nums) < 4:
        return None
    xs, ys = nums[::2], nums[1::2]
    return [min(xs)*scale, min(ys)*scale, max(xs)*scale, max(ys)*scale]

existing_text_boxes = []
for shape in original['shape']:
    if shape.startswith('LIB~'):
        fields = shape.split('~', 3)
        center = (round(float(fields[1]), 3), round(float(fields[2]), 3))
        for child in shape.split('#@$')[1:]:
            if center in {(round(x, 3), round(y, 3)) for x, y in button_centers} and child.startswith(('TEXT~N~', 'TEXT~P~')):
                continue
            box = path_bbox(child, SCALE)
            if box: existing_text_boxes.append(box)
    elif shape.startswith('TEXT~'):
        box = path_bbox(shape, 1.0)
        if box: existing_text_boxes.append(box)
existing_text_overlaps = []
for label in text_records:
    a = label['bbox']
    for b in existing_text_boxes:
        if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
            existing_text_overlaps.append(label['text'])
if existing_text_overlaps:
    raise RuntimeError('New control legend overlaps existing silk text: '+json.dumps(existing_text_overlaps))
def pads_by_component(document):
    result = {}
    for item in document['shape']:
        if item.startswith('LIB~'):
            key = tuple(item.split('~', 3)[:3])
            result[key] = sorted(child for child in item.split('#@$') if child.startswith('PAD~'))
    return result
assert pads_by_component(pcb) == pads_by_component(original)
assert sum(s.startswith('LIB~') for s in pcb['shape']) == 36
OUTPUT.write_text(json.dumps(pcb,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
REPORT.write_text(json.dumps({'status':'PASS_STATIC_PAD_CHECK','source':str(INPUT.relative_to(ROOT)),
    'output':str(OUTPUT.relative_to(ROOT)),'components':36,'labels':text_records,'polarity':sign_records,
    'pad_overlaps':overlaps,'original_objects_unchanged':True,
    'button_default_value_and_ref_text_removed':True,'button_text_overlaps':text_overlaps,
    'existing_silkscreen_text_overlaps':existing_text_overlaps,
    'note':'This is a fresh-export-derived PCB with crowded button default text removed; DOWN and SELECT legends are swapped per user request. Electrical wiring is unchanged.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS_STATIC_PAD_CHECK','component_count':36,'labels':len(text_records),
    'signs':len(sign_records),'output':str(OUTPUT.relative_to(ROOT))},indent=2))
