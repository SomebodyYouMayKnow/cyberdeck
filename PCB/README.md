# PCB sources

The current project goal is documented in [NEONRED_FINAL_VERSION_2026-10-09.md](../docs/NEONRED_FINAL_VERSION_2026-10-09.md): **no separate HDMI display**, with proposed Proxmark3, RTL-SDR, ESP32 firmware modes and a conditional external ESP32 antenna. On 2026-10-09, the live EasyEDA Standard project `neonred` was opened and its current `Sheet_1` and `PCB_neonred` exported below. These are baseline snapshots only: the proposed Proxmark3/RTL-SDR/antenna expansion has not been laid out, and this is not a fabrication release. Older simple-power and port-revision sources are design history, not approval to fabricate.

- `neonred-live-schematic_2026-10-09.json` and `neonred-live-PCB_2026-10-09.json` — source exports from the live EasyEDA Standard project.
- `screenshots/easyeda-neonred-schematic-2026-10-09.png` and `screenshots/easyeda-neonred-pcb-2026-10-09.png` — matching visual exports.

- `pcb-simple-power-native.json` — saved EasyEDA PCB source
- `schematic-simple-power-native.json` — saved EasyEDA schematic source
- `wiring-map-simple-power.*` — connector and pin-assignment record
- `simple-power-native-drc.json` — saved DRC record; the corresponding EasyEDA screenshot shows 0 displayed DRC errors for that point-in-time revision
- `simple-power-mounting-template.pdf` — 1:1 mechanical-fit print template
- `screenshots/` — live project image exports plus earlier design-stage views and mounting-template preview

The source and screenshots document the design stage; they do not prove physical fit, assembly, or electrical operation. There is no final Gerber archive. Before fabrication, measure the real hardware, complete final DRC/ERC in the PCB tool, and add `production/gerbers.zip`.
