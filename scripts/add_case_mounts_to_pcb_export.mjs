import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const sourcePath = path.join(root, 'PCB', 'PCB_cyberdeck-completed-after-JP5-2026-10-16.json');
const outputPath = path.join(root, 'PCB', 'PCB_cyberdeck-completed-two-layer-case-mounts-2026-10-17.json');
const reportPath = path.join(root, 'PCB', 'case-mount-hole-audit-2026-10-17.json');
const pcb = JSON.parse(fs.readFileSync(sourcePath, 'utf8'));

const outline = pcb.shape.find((s) => s.startsWith('TRACK~1~10~'));
if (!outline) throw new Error('Board outline track on layer 10 not found');
const outlineCoords = outline.split('~')[4].trim().split(/\s+/).map(Number);
const xs = outlineCoords.filter((_, i) => i % 2 === 0);
const ys = outlineCoords.filter((_, i) => i % 2 === 1);
const bounds = { minX: Math.min(...xs), maxX: Math.max(...xs), minY: Math.min(...ys), maxY: Math.max(...ys) };
const unitsPerMm = 3.937007874;
const toMm = (v) => v / unitsPerMm;
const widthMm = toMm(bounds.maxX - bounds.minX);
const heightMm = toMm(bounds.maxY - bounds.minY);

const copperLayers = pcb.layers
  .map((s) => s.split('~'))
  .filter((a) => ['TopLayer', 'BottomLayer', 'Inner1', 'Inner2', 'Inner3', 'Inner4'].includes(a[1]) && a[3] === 'true')
  .map((a) => a[1]);
if (widthMm < 200 || widthMm > 220 || heightMm < 100 || heightMm > 120) {
  throw new Error(`Unexpected outline size ${widthMm.toFixed(2)} x ${heightMm.toFixed(2)} mm`);
}
if (copperLayers.length !== 2 || !copperLayers.includes('TopLayer') || !copperLayers.includes('BottomLayer')) {
  throw new Error(`Expected a two-layer stack; active copper layers: ${copperLayers.join(', ')}`);
}

const tracks = [];
const pads = [];
const holes = [];
for (const shape of pcb.shape) {
  if (shape.startsWith('TRACK~')) {
    const a = shape.split('~');
    // Only layers 1 and 2 are copper here; layer 10 is the board outline.
    if (!['1', '2'].includes(a[2])) continue;
    const points = a[4].trim().split(/\s+/).map(Number);
    for (let i = 0; i + 3 < points.length; i += 2) {
      tracks.push({ x1: points[i], y1: points[i + 1], x2: points[i + 2], y2: points[i + 3], width: Number(a[1]), layer: a[2] });
    }
  } else if (shape.startsWith('LIB~')) {
    for (const item of shape.split('#@$')) {
      if (!item.startsWith('PAD~')) continue;
      const a = item.split('~');
      pads.push({ x: Number(a[2]), y: Number(a[3]), w: Number(a[4]), h: Number(a[5]) });
    }
  } else if (shape.startsWith('HOLE~')) {
    const a = shape.split('~');
    holes.push({ x: Number(a[1]), y: Number(a[2]), diameter: Number(a[3]), id: a[4] });
  }
}

const distanceToSegment = (x, y, x1, y1, x2, y2) => {
  const dx = x2 - x1;
  const dy = y2 - y1;
  const lengthSq = dx * dx + dy * dy;
  const t = lengthSq ? Math.max(0, Math.min(1, ((x - x1) * dx + (y - y1) * dy) / lengthSq)) : 0;
  return Math.hypot(x - (x1 + t * dx), y - (y1 + t * dy));
};

// Six distributed case holes, intentionally placed on the existing 5 mm inset perimeter band.
// The component placements and all existing copper/objects are retained unchanged.
const candidateMm = [
  { ref: 'CASE1', x: 51.4, y: 5.0 },
  { ref: 'CASE2', x: 153.0, y: 5.0 },
  { ref: 'CASE3', x: 35.0, y: 105.0 },
  { ref: 'CASE4', x: 115.0, y: 105.0 },
  { ref: 'CASE5', x: 205.0, y: 85.0 },
  { ref: 'CASE6', x: 205.0, y: 105.0 },
];
const holeDiameterMm = 2.7; // M2.5 clearance estimate; confirm screw/standoff choice before fab.
const holeRadius = holeDiameterMm * unitsPerMm / 2;
const checks = [];
const add = [];
for (const c of candidateMm) {
  const x = bounds.minX + c.x * unitsPerMm;
  const y = bounds.minY + c.y * unitsPerMm;
  const edgeInsetMm = Math.min(x - bounds.minX, bounds.maxX - x, y - bounds.minY, bounds.maxY - y) / unitsPerMm;
  const trackClearanceMm = Math.min(...tracks.map((t) => distanceToSegment(x, y, t.x1, t.y1, t.x2, t.y2) - t.width / 2 - holeRadius)) / unitsPerMm;
  const padClearanceMm = Math.min(...pads.map((p) => Math.hypot(x - p.x, y - p.y) - Math.max(p.w, p.h) / 2 - holeRadius)) / unitsPerMm;
  const existingHoleClearanceMm = Math.min(...holes.map((h) => Math.hypot(x - h.x, y - h.y) - h.diameter / 2 - holeRadius)) / unitsPerMm;
  const newHoleClearanceMm = Math.min(...add.map((h) => Math.hypot(x - h.x, y - h.y) - 2 * holeRadius)) / unitsPerMm;
  // At least 3 mm from board edge to drill center; >=0.5 mm from track/pad edges;
  // >=1.0 mm between adjacent hole edges. These are conservative screening checks, not CAD DRC.
  const ok = edgeInsetMm >= 3 && trackClearanceMm >= 0.5 && padClearanceMm >= 0.5 && existingHoleClearanceMm >= 1 && newHoleClearanceMm >= 1;
  checks.push({ ...c, x: Number(toMm(x - bounds.minX).toFixed(3)), y: Number(toMm(y - bounds.minY).toFixed(3)), holeDiameterMm, edgeInsetMm: Number(edgeInsetMm.toFixed(2)), nearestCopperClearanceMm: Number(trackClearanceMm.toFixed(2)), nearestPadClearanceMm: Number(padClearanceMm.toFixed(2)), nearestExistingHoleEdgeMm: Number(existingHoleClearanceMm.toFixed(2)), nearestNewHoleEdgeMm: Number.isFinite(newHoleClearanceMm) ? Number(newHoleClearanceMm.toFixed(2)) : null, passesGeometryScreen: ok });
  if (!ok) throw new Error(`${c.ref} failed preliminary clearance screen: ${JSON.stringify(checks.at(-1))}`);
  add.push({ ...c, x, y });
}

let idSuffix = 1;
const ids = new Set(pcb.shape.flatMap((s) => [...s.matchAll(/gge[\w-]+/g)].map((m) => m[0])));
const nextId = (tag) => {
  let id;
  do { id = `ggeNRcase${tag}${String(idSuffix++).padStart(4, '0')}`; } while (ids.has(id));
  ids.add(id);
  return id;
};
for (const h of add) {
  const x = Number(h.x.toFixed(3));
  const y = Number(h.y.toFixed(3));
  const n = h.ref;
  pcb.shape.push(`HOLE~${x}~${y}~${(holeDiameterMm * unitsPerMm).toFixed(4)}~${nextId(n)}~0`);
  pcb.shape.push(`CIRCLE~${x}~${y}~15.748~0.5~12~${nextId(`${n}keepout`)}~0~~`);
}

fs.writeFileSync(outputPath, JSON.stringify(pcb, null, 2) + '\n');
const report = {
  status: 'PRELIMINARY_OFFLINE_EXPORT_ONLY',
  source: path.relative(root, sourcePath),
  output: path.relative(root, outputPath),
  sourceRevisionDate: '2026-10-16',
  note: 'This uses the newest saved cyberdeck-completed PCB source in the workspace. It is not an export from the live EasyEDA document; re-export/sync live PCB before fabrication.',
  boardOutlineMm: { width: Number(widthMm.toFixed(2)), height: Number(heightMm.toFixed(2)) },
  copperLayers,
  sourceShapeCount: JSON.parse(fs.readFileSync(sourcePath, 'utf8')).shape.length,
  outputShapeCount: pcb.shape.length,
  componentFootprintsPreserved: true,
  existingHolesPreserved: holes.length,
  addedCaseHoles: checks,
  checksPassed: checks.every((x) => x.passesGeometryScreen),
  requiredFinalChecks: ['Import the export into the active EasyEDA cyberdeck-completed PCB and compare against its current canvas.', 'Run EasyEDA DRC after import; inspect hole-to-copper and hole-to-component clearances.', 'Check case screw/standoff diameter and actual enclosure attachment points.', 'Generate and visually inspect Gerber and drill files; perform physical fit and combined-load tests before powering the assembly.'],
};
fs.writeFileSync(reportPath, JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report, null, 2));
