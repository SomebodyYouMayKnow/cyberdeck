# PCB sources

This folder contains the current **simple-power** revision of the NEONRED carrier PCB.

- `pcb-simple-power-native.json` — saved EasyEDA PCB source
- `schematic-simple-power-native.json` — saved EasyEDA schematic source
- `wiring-map-simple-power.*` — connector and pin-assignment record
- `simple-power-native-drc.json` — saved DRC record; the corresponding EasyEDA screenshot shows 0 displayed DRC errors for that point-in-time revision
- `simple-power-mounting-template.pdf` — 1:1 mechanical-fit print template
- `screenshots/` — current EasyEDA visual evidence: 3D assembly view, routed board / DRC view, and mounting-template preview

The source and screenshots document the design stage; they do not prove physical fit, assembly, or electrical operation. There is no final Gerber archive. Before fabrication, measure the real hardware, complete final DRC/ERC in the PCB tool, and add `production/gerbers.zip`.
