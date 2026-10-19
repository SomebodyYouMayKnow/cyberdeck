# CAD sources

These files are copied from the active design folder for publication:

- `Cyberdeck_Enclosure.scad` is the editable parametric enclosure and printed-support concept for the 226 × 126 mm PCB with eight outside lips.
- `Cyberdeck_Fusion_Layout.dxf` is the updated millimetre placement sketch, including the PCB lips, 12 case holes, and eight 2.751 mm CardKB/Chameleon support holes.
- `Cyberdeck_layout.svg` previews the board position and current module reserves.
- `MECHANICAL_VALIDATION.md` records dimensions, assumptions and physical checks still required.

`NEONRED_PCB_component-mounts_2026-10-19.step` is the Fusion-exported STEP solid for the 1.6 mm carrier PCB. `Export_Neonred_PCB_STEP.py` regenerates it in Fusion 360. PrusaSlicer exports mesh formats such as STL/3MF, not STEP. The CardKB and Chameleon support holes now pass through the live EasyEDA PCB and align to service-tray bosses. EasyEDA reports 0 DRC errors and the native Gerber is saved in `outputs/NEONRED_live_component_mounts_2026-10-19.zip`. The ALFA cradle is separate and unplaced, with no board holes, because its location and exact adapter envelope are not established. These sources are not a fit-tested enclosure.

