# NEONRED scope reset and PCB rollback

**Date:** 2026-10-16

The project has returned to the simpler Chameleon Ultra SE3 version. The preserved EasyEDA `savecopy` was left untouched. I cloned that native PCB document in the `neonred` project and renamed the clone `PCB_neonred`, making it the current PCB. The previous Proxmark-expanded PCB is preserved as `PCB_neonred_proxmark_archive_2026-10-16` rather than deleted.

## Verification

EasyEDA Design Manager on the new canonical `PCB_neonred` showed **Components (20), Nets (70 / 70), and DRC Errors (0)** after cloning. This confirms the restored document retained its component and net objects. It is a CAD/DRC result only; it does not establish that the electrical design, power budget, footprints, RF behavior, physical fit, or fabrication outputs are validated.

The exact native source exported from the preserved savecopy is [PCB_savecopy_2026-10-16.json](../PCB/PCB_savecopy_2026-10-16.json). The active PCB should be exported again after any further edits. The `savecopy` document itself was not edited.

## Current scope

- Keep the Chameleon Ultra SE3 as the removable RFID/NFC device.
- Keep the Pi Zero 2 W, LILYGO T-Display-S3 AMOLED, CardKB, controls, IR hardware, two nRF24L01+ modules, and USB Hub HAT as described in the current goal and [BOM.csv](../BOM.csv).
- The Proxmark3, RTL-SDR/radar detector, downconverters, Marauder/Flock You experiments, and external ESP32 antenna are out of current scope. Dated notes about them are historical.
- At the user's direction on 2026-10-16, the five `PM3_*` schematic pages were deleted from the live `neonred` EasyEDA project. The separate `neonred-schematic-backup-2026-10-11` project and the archived Proxmark PCB remain preserved.
- A separate `ARCHIVE_incomplete-copy_DO_NOT_USE_2026-10-16` document remains from an unsuccessful copy attempt. It is not the canonical PCB; use only `PCB_neonred`.

## Next checks

1. Keep the separate `neonred-schematic-backup-2026-10-11` project and all local Proxmark history as archive; do not copy the PM3 design back into the active project without a new scope decision.
2. Verify the restored PCB's schematic-to-board synchronization, exact component revisions, power/current paths, IR orientation and current limiting, and board outline/mounting against physical parts.
3. Generate fresh fabrication outputs from the canonical `PCB_neonred` only after those checks. Do not treat the 0-error DRC as fabrication or power-on approval.
