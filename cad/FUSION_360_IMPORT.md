# Fusion 360 import guide

Fusion cannot directly convert an OpenSCAD `.scad` source into its editable native `.f3d` format. This project includes:

- `Cyberdeck_Enclosure.scad`: editable parametric enclosure source for the 226 × 126 mm PCB, including its eight mounting lips and separate printed retainers.
- `Cyberdeck_Fusion_Layout.dxf`: millimetre placement sketch showing the lips, PCB mounting holes, module reserves and printed-support hole patterns.
- `Cyberdeck_layout.svg`: visual reference usable as an inserted Fusion sketch.
- `MECHANICAL_VALIDATION.md`: fit assumptions and physical checks.

## Export a PCB STEP solid

PrusaSlicer works with mesh files, but it does not export STEP. In Fusion's Design workspace, run `Export_Neonred_PCB_STEP.py` from **Utilities → Scripts and Add-Ins**. The script creates `NEONRED_PCB_component-mounts_2026-10-19.step` beside itself. This STEP is the carrier board only (226 × 126 mm lip outline, 1.6 mm thickness, and 24 NPTHs: 12 case, 4 Pi mounting, and 8 support holes); it is not the full enclosure or an electronics assembly.

## Use the DXF in Fusion

1. Create a new Fusion design and set document units to **mm**.
2. Create a sketch on the XY plane.
3. Choose **Insert → Insert DXF**, select `Cyberdeck_Fusion_Layout.dxf`, and keep scale at **1.0**.
4. Confirm the outer PCB envelope is **226 × 126 mm** including its eight lips; the inner routed area is **210 × 110 mm**.
5. Use its layers as construction references: `PCB_OUTLINE`, `MOUNT_HOLES`, `MODULE_ENVELOPES`, `SUPPORT_HOLES`, `CUTOUTS`, and `CONTROLS`. `MOUNT_HOLES` includes the new CardKB and Chameleon through-holes; `SUPPORT_HOLES` shows their matching support locations.
6. Create native Fusion components for the enclosure and supports, then save an editable `.f3d`.
7. Export the complete electronics-inclusive assembly as `.step` for Stardance.

The DXF and SCAD are placement references, not fit-verified enclosure drawings. The eight support holes were imported into the live EasyEDA PCB; the saved audit reported zero DRC errors, and the latest native EasyEDA Gerber is [`PCB/NEONRED_Gerbers_current_2026-10-19.zip`](../PCB/NEONRED_Gerbers_current_2026-10-19.zip). The STEP file is the carrier board only, not a verified full enclosure. The ALFA cradle is separate and unplaced because the current PCB has no ALFA reserve. Complete physical checks in `MECHANICAL_VALIDATION.md` before printing.

