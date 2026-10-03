# Fusion 360 import guide

Fusion cannot directly convert an OpenSCAD `.scad` source into its editable native `.f3d` format. This project includes:

- `Cyberdeck_Enclosure.scad`: editable parametric 3D source and the dimensional authority.
- `Cyberdeck_Fusion_Layout.dxf`: millimetre DXF placement sketch for Fusion.
- `Cyberdeck_layout.svg`: visual reference usable as an inserted Fusion sketch.
- `MECHANICAL_VALIDATION.md`: fit assumptions and physical checks.

## Use the DXF in Fusion

1. Create a new Fusion design and set document units to **mm**.
2. Create a sketch on the XY plane.
3. Choose **Insert → Insert DXF**, select `Cyberdeck_Fusion_Layout.dxf`, and keep scale at **1.0**.
4. Confirm the outer carrier-board outline is **190 × 110 mm**.
5. Use its layers as construction references: `PCB_OUTLINE`, `MOUNT_HOLES`, `MODULE_ENVELOPES`, `CUTOUTS`, and `CONTROLS`.
6. Create native Fusion components for the enclosure and supports, then save an editable `.f3d`.
7. Export the complete electronics-inclusive assembly as `.step` for Stardance.

The DXF is a placement reference, not a verified manufacturing drawing. Complete the physical tests in `MECHANICAL_VALIDATION.md` before finalizing holes or printing.

