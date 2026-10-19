# NEONRED case mounting ears — live validation (2026-10-19)

The case-mounting ears have been imported into the live EasyEDA `cyberdeck-completed` PCB document (`PCB_cyberdeck-completed`) and saved.

## Geometry

- Board outline is one closed polyline with eight chamfered perimeter tabs, two per side.
- Board envelope reported by EasyEDA’s Gerber preview: **226 × 126 mm**, **2 copper layers**.
- Eight new non-plated 3.2 mm mounting holes were added, one per tab. Existing board holes and component placements were preserved.
- The EasyEDA File Source export contains 12 standalone HOLE records: four existing board mounts plus eight new ear mounts.

## Verification and outputs

- Live EasyEDA Design Rule Check: **0 errors**. The Gerber generator’s DRC prompt was accepted before export.
- Gerber archive: `outputs/NEONRED_case_ears_2026-10-19.zip`.
- Live EasyEDA source JSON: `PCB/PCB_cyberdeck-completed-case-ears-2026-10-19.json`.
- The Gerber ZIP contains top/bottom copper, top silkscreen, solder masks, paste mask, board outline, document layer, and plated/non-plated drill files. The NPTH drill file includes the eight new 3.2 mm holes.

This confirms the editor’s DRC and fabrication-file generation for the saved board. It does not establish electrical operation or enclosure fit; verify the case screw placement and clearances against the printed case before assembly.

