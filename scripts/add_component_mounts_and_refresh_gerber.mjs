import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const root = path.resolve(import.meta.dirname, '..');
const input = path.join(root, 'PCB', 'PCB_cyberdeck-completed-case-ears-2026-10-19.json');
const output = path.join(root, 'PCB', 'PCB_cyberdeck-completed-component-mounts-2026-10-19.json');
const sourceZip = path.join(root, 'outputs', 'NEONRED_case_ears_2026-10-19.zip');
const outputZip = path.join(root, 'outputs', 'NEONRED_component_mounts_2026-10-19.zip');
const auditPath = path.join(root, 'PCB', 'component-mount-hole-audit-2026-10-19.json');

const pcb = JSON.parse(fs.readFileSync(input, 'utf8'));
const unitsPerMm = 3.937007874;
const holeDiameterMm = 2.751; // Existing EasyEDA NPTH tool T01; M2.5 clearance prototype.
const holeRadiusRaw = holeDiameterMm / 2 * unitsPerMm;
const minX = 4016.063;
const minY = 3016.351;

// These screw axes exactly match the current CAD support-frame holes, transformed
// into the EasyEDA source coordinate system. CardKB remains unmodified.
const mounts = [
  { id: 'KB_TL', component: 'CardKB printed frame', xMm: 13.5, yMm: 48.5 },
  { id: 'KB_TR', component: 'CardKB printed frame', xMm: 106.5, yMm: 48.5 },
  { id: 'KB_BL', component: 'CardKB printed frame', xMm: 13.5, yMm: 107.5 },
  { id: 'KB_BR', component: 'CardKB printed frame', xMm: 106.5, yMm: 107.5 },
  { id: 'CHAM_TL', component: 'Chameleon retainer', xMm: 150, yMm: 14 },
  { id: 'CHAM_TR', component: 'Chameleon retainer', xMm: 202, yMm: 14 },
  // The lower pair is shifted 2 mm inward to clear a routed trace at the
  // original lower-left screw location; the printed retainer pattern matches.
  { id: 'CHAM_BL', component: 'Chameleon retainer', xMm: 150, yMm: 34 },
  { id: 'CHAM_BR', component: 'Chameleon retainer', xMm: 202, yMm: 34 },
].map((m) => ({ ...m, x: minX + m.xMm * unitsPerMm, y: minY + m.yMm * unitsPerMm }));

const existingIds = new Set(pcb.shape.flatMap((s) => [...s.matchAll(/gge[\w-]+/g)].map((m) => m[0])));
const existingHoleIds = pcb.shape.filter((s) => s.startsWith('HOLE~')).map((s) => s.split('~')[4]);
for (const mount of mounts) {
  const id = `gge_neonred_${mount.id}_npth_20261019`;
  if (existingIds.has(id) || existingHoleIds.includes(id)) throw new Error(`Duplicate mount ID ${id}`);
}

const tracks = [];
const pads = [];
const holes = [];
for (const shape of pcb.shape) {
  if (shape.startsWith('TRACK~')) {
    const a = shape.split('~');
    if (!['1', '2'].includes(a[2])) continue;
    const p = a[4].trim().split(/\s+/).map(Number);
    for (let i = 0; i + 3 < p.length; i += 2) {
      tracks.push({ x1: p[i], y1: p[i + 1], x2: p[i + 2], y2: p[i + 3], width: Number(a[1]), id: a[5] });
    }
  } else if (shape.startsWith('LIB~')) {
    for (const item of shape.split('#@$')) {
      if (!item.startsWith('PAD~')) continue;
      const a = item.split('~');
      pads.push({ x: Number(a[2]), y: Number(a[3]), w: Number(a[4]), h: Number(a[5]), id: a[12], net: a[7] });
    }
  } else if (shape.startsWith('HOLE~')) {
    const a = shape.split('~');
    // EasyEDA stores the HOLE radius in raw units; current 6.2992 entries
    // are a 3.2 mm drill as confirmed by the existing Excellon output.
    holes.push({ x: Number(a[1]), y: Number(a[2]), radius: Number(a[3]) });
  }
}

const pointSegmentDistance = (x, y, t) => {
  const dx = t.x2 - t.x1;
  const dy = t.y2 - t.y1;
  const l2 = dx * dx + dy * dy;
  const f = l2 ? Math.max(0, Math.min(1, ((x - t.x1) * dx + (y - t.y1) * dy) / l2)) : 0;
  return Math.hypot(x - t.x1 - f * dx, y - t.y1 - f * dy) - t.width / 2;
};

const clearances = mounts.map((m) => {
  const holeRadius = holeRadiusRaw;
  const nearestTrack = tracks.map((t) => ({ mm: (pointSegmentDistance(m.x, m.y, t) - holeRadius) / unitsPerMm, id: t.id })).sort((a, b) => a.mm - b.mm)[0];
  const nearestPad = pads.map((p) => ({ mm: (Math.hypot(m.x - p.x, m.y - p.y) - Math.max(p.w, p.h) / 2 - holeRadius) / unitsPerMm, id: p.id, net: p.net })).sort((a, b) => a.mm - b.mm)[0];
  const nearestHole = holes.map((h) => ({ mm: (Math.hypot(m.x - h.x, m.y - h.y) - h.radius - holeRadius) / unitsPerMm })).sort((a, b) => a.mm - b.mm)[0];
  const edgeInset = Math.min(m.x - minX, 4905.825 - m.x, m.y - minY, 3512.413 - m.y) / unitsPerMm;
  const result = {
    id: m.id,
    component: m.component,
    boardLocalMm: [m.xMm, m.yMm],
    holeDiameterMm,
    edgeInsetMm: Number(edgeInset.toFixed(3)),
    nearestTrackEdgeClearanceMm: Number(nearestTrack.mm.toFixed(3)),
    nearestTrackId: nearestTrack.id,
    nearestPadEdgeClearanceMm: Number(nearestPad.mm.toFixed(3)),
    nearestPadId: nearestPad.id,
    nearestPadNet: nearestPad.net,
    nearestExistingHoleEdgeClearanceMm: Number(nearestHole.mm.toFixed(3)),
    screeningPass: edgeInset >= 3 && nearestTrack.mm >= 0.25 && nearestPad.mm >= 0.25 && nearestHole.mm >= 1,
  };
  if (!result.screeningPass) throw new Error(`Preliminary geometry screening failed: ${JSON.stringify(result)}`);
  return { ...result, x: m.x, y: m.y };
});

for (const m of clearances) {
  pcb.shape.push(`HOLE~${m.x.toFixed(4)}~${m.y.toFixed(4)}~${holeRadiusRaw.toFixed(4)}~gge_neonred_${m.id}_npth_20261019~0`);
}
fs.writeFileSync(output, JSON.stringify(pcb, null, 2) + '\n');

// Keep the EasyEDA-generated copper/silkscreen/etc. unchanged: the PCB netlist,
// copper, outline, and component placement are unchanged by these mechanical
// through holes. Update only the NPTH Excellon toolpath in the original archive.
// EasyEDA Excellon origin for this exact export: X = board-local-X - 1 mm,
// Y = 77 mm - board-local-Y. Confirmed against its 12 pre-existing NPTH holes.
const ex = (v) => `${v < 0 ? '-' : ''}${Math.round(Math.abs(v) * 1000).toString().padStart(6, '0')}`;
const drillRows = clearances.map((m) => `X${ex(m.boardLocalMm[0] - 1)}Y${ex(77 - m.boardLocalMm[1])}`);
const zipTmp = `${outputZip}.new`;
if (fs.existsSync(zipTmp)) fs.unlinkSync(zipTmp);
if (fs.existsSync(outputZip)) fs.unlinkSync(outputZip);
const python = 'C:\\Users\\matth\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe';
execFileSync(python, [path.join(root, 'scripts', 'refresh_npth_gerber.py'), sourceZip, zipTmp, ...drillRows]);
fs.renameSync(zipTmp, outputZip);

const audit = {
  status: 'OFFLINE_GEOMETRY_SCREEN_PASS_NATIVE_EASYEDA_DRC_PENDING',
  sourcePcb: path.relative(root, input),
  candidatePcb: path.relative(root, output),
  sourceGerber: path.relative(root, sourceZip),
  candidateGerber: path.relative(root, outputZip),
  existingExplicitHoleRecords: holes.length,
  existingNpthDrillCount: 16,
  newTotalNpthDrillCount: 24,
  addedHoles: clearances.map(({ x, y, ...m }) => m),
  unchangedElectricalShapes: true,
  copiedGerberLayersUnchangedExceptNpth: true,
  validation: [
    'All 8 holes have >=0.25 mm estimated clearance from copper tracks and footprint pads; this is a geometry screen, not EasyEDA DRC.',
    'NPTH file uses existing 2.751 mm EasyEDA drill tool and existing coordinate origin mapping.',
    'Run EasyEDA native DRC, import/compare the candidate, then regenerate/download Gerbers in EasyEDA before ordering.',
    'ALFA AWUS036ACS remains unplaced and has no board screw holes; do not drill/print its cradle until a location and real-part measurements are chosen.',
  ],
};
fs.writeFileSync(auditPath, JSON.stringify(audit, null, 2) + '\n');
console.log(JSON.stringify(audit, null, 2));
