# NEONRED — current project goal

**Updated:** 2026-10-16. This is the current scope after restoring the EasyEDA PCB from the preserved `savecopy`. It supersedes older descriptions of an integrated Proxmark, radar detector, and other radio expansions.

## Final version description

NEONRED is a compact portable cyberdeck centered on a Raspberry Pi Zero 2 W and a LILYGO T-Display-S3 AMOLED. The Pi runs Linux; the LILYGO ESP32-S3 provides a small onboard interface. A CardKB keyboard, rotary encoder, navigation buttons, IR receiver/transmitter, and two nRF24L01+ modules support the planned user controls and electronics experiments. The Waveshare four-port USB Hub HAT mounts next to the Pi and connects over USB. The Chameleon Ultra SE3 is the external RFID/NFC device for this version; it is not integrated as a bare IC or custom reader circuit.

The current design has no HDMI display, integrated Proxmark, RTL-SDR/radar-detector subsystem, or ESP32 external antenna. Proxmark3, RTL-SDR/downconverters, Marauder/Flock You firmware, and antenna-feed expansion are out of current scope. Earlier notes about these are historical only.

## Intended uses

- Portable Linux development, coding, and diagnostics on the Pi.
- ESP32-S3 interface experiments using its screen, buttons, encoder, and CardKB.
- IR learning and control with the user's own devices.
- NFC/RFID experiments with owned or explicitly authorized tags using the Chameleon Ultra SE3.
- nRF24 experiments in a controlled lab with owned equipment.
- Learning PCB design, firmware, wiring, enclosure CAD, fabrication, and assembly.

## Current hardware boundaries

- Keep the Chameleon Ultra SE3 a removable external module; allow its USB/Bluetooth connection and physical access.
- Keep the Raspberry Pi and USB Hub HAT as separate serviceable modules. Do not assume the HAT and Pi share a mounting footprint or may be powered through an unverified path.
- Keep the LILYGO board on the carrier as represented by the restored saved copy. The saved PCB is a design snapshot, not proof that power, pin mapping, or physical fit is correct.
- The current source export is [PCB_savecopy_2026-10-16.json](../PCB/PCB_savecopy_2026-10-16.json), exported from the untouched EasyEDA `savecopy`. The active EasyEDA PCB was cloned from that source and named `PCB_neonred`.
- The five `PM3_*` pages were removed from the live EasyEDA project on 2026-10-16 at the user's direction. The separate dated schematic backup and archived Proxmark PCB remain preserved; PM3 is outside the active design scope.

## Power and release status

Treat power as unresolved. Keep the Pi, LILYGO, and external modules on their intended USB/power connections until the exact bank ratings, hub power path, and combined loads are verified. Do not route USB VBUS outputs together or assume the Pi GPIO/header can power all peripherals. Bench-measure current and voltage under combined operation before approving a power plan.

The restored PCB has not been certified for fabrication or power-on. Run a fresh DRC and electrical review on this restored copy, confirm all board outlines/holes and device fit, and inspect the fabrication outputs before ordering.

## Historical material

Older dated Proxmark and SDR BOM/audit files are retained as project history. They do not describe the current NEONRED build. Use [the scope reset note](NEONRED_SCOPE_RESET_2026-10-16.md) and [BOM.csv](../BOM.csv) for current scope.
