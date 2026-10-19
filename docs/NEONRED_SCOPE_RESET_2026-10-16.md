# NEONRED scope reset and PCB rollback

**Date:** 2026-10-16

The project has returned to the simpler Chameleon Ultra SE3 version. The preserved EasyEDA `savecopy` was left untouched. I cloned that native PCB document in the `neonred` project and renamed the clone `PCB_neonred`, making it the current PCB.

## Verification

EasyEDA Design Manager on the new canonical `PCB_neonred` showed **Components (20), Nets (70 / 70), and DRC Errors (0)** after cloning. This confirms the restored document retained its component and net objects. It is a CAD/DRC result only; it does not establish that the electrical design, power budget, footprints, RF behavior, physical fit, or fabrication outputs are validated.

The exact native source exported from the preserved savecopy is [PCB_savecopy_2026-10-16.json](../PCB/PCB_savecopy_2026-10-16.json). The active PCB should be exported again after any further edits. The `savecopy` document itself was not edited.

## Live board update — 2026-10-16

The active non-savecopy EasyEDA board retains the LILYGO T-Display-S3 AMOLED, Pi Zero 2 W header/mechanical reference, controls, dual nRF24 modules, and integrated IR receiver/emitter circuit. The Chameleon Ultra SE3 and ALFA AWUS036ACS are external modules, not solderable footprints. Their new reference boxes are on the non-copper `Document` layer outside the board outline: Chameleon 40 x 24 mm is explicitly provisional and unverified; ALFA 55 x 25 mm represents the adapter body only, without antenna or USB-cable clearance. These boxes are case-layout guides, not verified mechanical fit or fabrication features. The Chameleon itself must be measured before designing its retainer.

The current carrier BOM is [BOM.csv](../BOM.csv). It lists the Chameleon and ALFA as external modules. A new native PCB export should be generated after the final cleanup of the live editor document.

## Current scope

- Keep the Chameleon Ultra SE3 as the removable RFID/NFC device.
- Keep the Pi Zero 2 W, LILYGO T-Display-S3 AMOLED, CardKB, controls, IR hardware, two nRF24L01+ modules, and USB Hub HAT as described in the current goal and [BOM.csv](../BOM.csv).
- RTL-SDR/radar detector, downconverters, Marauder/Flock You experiments, and external ESP32 antenna are out of current scope.
- A separate `ARCHIVE_incomplete-copy_DO_NOT_USE_2026-10-16` document remains from an unsuccessful copy attempt. It is not the canonical PCB; use only `PCB_neonred`.

## Next checks

1. Verify the restored PCB's schematic-to-board synchronization, exact component revisions, power/current paths, IR orientation and current limiting, and board outline/mounting against physical parts.
2. Generate fresh fabrication outputs from the canonical `PCB_neonred` only after those checks. Do not treat the 0-error DRC as fabrication or power-on approval.
