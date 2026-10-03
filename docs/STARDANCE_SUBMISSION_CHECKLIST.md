# Stardance submission checklist — Cyberdeck

**Status snapshot:** 2026-10-03

## Completed design work

- [x] Cyberdeck component plan, wiring documentation, and system layout.
- [x] Current carrier-PCB schematic: `outputs/schematic-simple-power-native.json`.
- [x] Current carrier-PCB layout: `outputs/pcb-simple-power-native.json`.
- [x] Current wiring map: `outputs/wiring-map-simple-power.json` and `outputs/wiring-map-simple-power.txt`.
- [x] DRC and verification evidence for the simple-power PCB revision.
- [x] BOM workbook: `outputs/cyberdeck-bom-updated.xlsx`.
- [x] 190 × 110 mm board outline, mounting holes, Pi mounts, HAT mounts, and HAT header slot.
- [x] Printable 1:1 mounting template: `outputs/simple-power-mounting-template.pdf`.
- [x] Parametric enclosure concept: `cad/Cyberdeck_Enclosure.scad`.
- [x] Mechanical layout reference: `cad/Cyberdeck_layout.svg`.
- [x] Mechanical validation plan: `cad/MECHANICAL_VALIDATION.md`.
- [x] Fusion-importable DXF reference: `cad/Cyberdeck_Fusion_Layout.dxf`.
- [x] This checklist and a complete workspace manifest.

## Physical validation

- [ ] Confirm exact revisions of the Pi, LILYGO, CardKB, HDMI display, Chameleon, USB HUB HAT, battery, antennas, and connectors.
- [ ] Print the 1:1 template at 100% and confirm its 100 mm calibration line.
- [ ] Test all real modules and their screw holes against the template.
- [ ] Test the HAT underside header through the 51.8 × 8 mm slot.
- [ ] Test keyboard, HAT, Pi, Chameleon, battery, plugs, and cable-bend height together.
- [ ] Test the Pi-to-HAT micro-USB cable orientation and bend clearance.
- [ ] Confirm display aperture, connector depth, antenna clearance, and Chameleon RFID range.

## CAD and manufacturing

- [ ] Finish the base, lid, hinge, closure, service cover, cable routing, and port cutouts in Fusion.
- [ ] Add final mounts for keyboard, ESP32, Pi/HAT, Chameleon, regulator/level shifter, battery, and antennas.
- [ ] Position accurate models of all electronics in one assembly.
- [ ] Verify opening/closing, antenna movement, cable movement, and screw access.
- [ ] Save the editable Fusion `.f3d` design.
- [ ] Export a complete electronics-inclusive `.STEP` assembly.
- [ ] Export printable case STLs/individual STEP parts.
- [ ] Make any measurement-driven PCB corrections, then run final DRC/ERC.
- [ ] Export final PCB Gerbers and drill files as `production/gerbers.zip`.

## Firmware and public repository

- [ ] Create ESP32 firmware and Raspberry Pi setup software.
- [ ] Add the firmware source, even if initially untested.
- [x] Create a public GitHub repository.
- [x] Organize it into `CAD/`, `PCB/`, `Firmware/`, and `production/`.
- [x] Put a linked `BOM.csv` in the repository root.
- [ ] Write a README in your own words with description, motivation, instructions, CAD render, PCB/schematic/wiring images, and BOM table.
- [x] Add a license and `.gitignore`.
- [ ] Verify repository paths and links from GitHub.

## Stardance submission evidence

- [ ] Log work in Lapse or keep a Markdown build journal.
- [ ] Get and record design feedback from other people.
- [ ] Submit the public repository for hardware funding.
- [ ] After funding: build, test, photograph, and demonstrate the completed cyberdeck.

## Current blockers

1. Physical fit measurements and tests are still needed.
2. No native Fusion `.f3d` or electronics-inclusive `.STEP` assembly exists yet.
3. Firmware, public GitHub repo, root `BOM.csv`, human-written README, production Gerbers, feedback, and work log remain outstanding.

The official Stardance hardware guide requires a complete CAD assembly with electronics in STEP format, PCB source, firmware, a linked root-level BOM CSV, a completed human-written README, and feedback. [Official guide](https://stardance.hackclub.com/resources/shipping-hardware)
