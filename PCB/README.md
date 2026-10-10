# PCB sources

The current project goal is documented in [NEONRED_FINAL_VERSION_2026-10-09.md](../docs/NEONRED_FINAL_VERSION_2026-10-09.md): **no separate HDMI display**, and the proposed Proxmark3, RTL-SDR, ESP32 firmware modes and conditional ESP32 external antenna. The EasyEDA files and screenshots currently saved here predate that expansion and are not a current fabrication layout. The EasyEDA live project was not available to the computer session for a new screenshot or edit. Older simple-power and port-revision sources are design history, not approval to fabricate.

- `pcb-simple-power-native.json` — saved EasyEDA PCB source
- `schematic-simple-power-native.json` — saved EasyEDA schematic source
- `wiring-map-simple-power.*` — connector and pin-assignment record
- `simple-power-native-drc.json` — saved DRC record; the corresponding EasyEDA screenshot shows 0 displayed DRC errors for that point-in-time revision
- `simple-power-mounting-template.pdf` — 1:1 mechanical-fit print template
- `screenshots/` — current EasyEDA visual evidence: 3D assembly view, routed board / DRC view, and mounting-template preview

The source and screenshots document the design stage; they do not prove physical fit, assembly, or electrical operation. There is no final Gerber archive. Before fabrication, measure the real hardware, complete final DRC/ERC in the PCB tool, and add `production/gerbers.zip`.
