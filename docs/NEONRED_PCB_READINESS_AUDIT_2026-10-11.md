# Historical: NEONRED PCB readiness and remediation status

> **Superseded 2026-10-16.** The active PCB was restored from the preserved EasyEDA `savecopy`; the Proxmark expansion is now out of scope. Use [the scope reset record](NEONRED_SCOPE_RESET_2026-10-16.md) and [current goal](NEONRED_FINAL_VERSION_2026-10-09.md) for the current project. This dated audit describes an earlier board revision and is retained as history.

**Updated:** 2026-10-11
**Status:** Not cleared for fabrication or power-on. The latest saved EasyEDA PCB has 0 DRC errors after a bottom-layer GND pour was added; power, RF, schematic and mechanical validation remain open. The earlier one-error results below are historical.

## Current evidence

The live EasyEDA board was updated with a top-layer GND copper area over the Proxmark circuit and saved. I removed the inner rectangular BoardOutLine loop that caused the large lower-board cutout. The refreshed 3D view shows continuous PCB material through that section; the large hole is gone. The previous Photo View image was stale and still showed the cutout until its tab was closed.

After the outline edit, the DRC temporarily reported 154 incomplete GND connections because the copper-area fills were stale. Rebuilding all copper areas (Shift+B) reduced the live result to **DRC Errors (1)** and **Nets (195 / 196)**. The saved post-GND-plane export remains `PCB/NEONRED-live-PCB-after-GND-plane-2026-10-11.json`; it predates the latest outline correction and refill, so it is not a fresh export of the current live board. It records 170 footprints, 642 tracks, 334 vias, and four GND copper areas, including overlapping top-layer GND areas that should be reviewed.

The remaining live DRC item is `gge67989 (Via - Track)` on GND. Its details identify BottomLayer track `gge95612`, width 0.254 mm, from (130.937, -182.637) mm to (133.437, -168.137) mm, and GND via `gge38672` at (130.556, -228.092) mm. The endpoints are about 60.0 mm apart. I tried the EasyEDA cloud autorouter with “Skip Routed Nets” enabled; it stayed at 0% for about 15 seconds and was canceled without routing changes. I did not draw an unverified long bridge across the Proxmark circuitry. This one GND connection remains open.

The prior audit reported 522 traces below a 0.254 mm DRC width rule. The active export's default width rule is 0.7992 internal units (about 0.203 mm); changing a minimum rule only affects warnings and does not widen copper or prove current capacity. Confirm the fabricator's limits and review every power, coil-drive, and RF return net against current, copper thickness, voltage drop, and thermal rise. No DRC pass or power sign-off is established.

The carrier is approximately 90 × 180 mm. The Proxmark sub-area is approximately 81.3 × 51.3 mm. There are four mounting holes in the upper/middle region, not confirmed case-corner mounts. The Pi footprint's 40 header-pad nets remain isolated from the carrier traces. The IR LED (D1) and IR receiver (U3) are draft footprints near the top edge, not verified at the intended left-side opening. Proxmark USB Mini-B (PROXSV1) and antenna connector (PROXSV2) are present; LF/HF coils are absent and the Proxmark clone remains an unvalidated reference design.

## Power and interface findings

- The Raspberry Pi Zero 2 W should have a dedicated regulated 5 V input capable of its recommended 2.5 A. Its GPIO header is not routed into this carrier in the current export.
- The Waveshare USB HUB HAT is a four-port, 5 V hub. Its published specifications do not establish enough aggregate downstream current for the ALFA Wi-Fi adapter, RTL-SDR, Proxmark, Chameleon, and other accessories together. The Pi/HAT connection is USB; don't assume the Pi's USB port can power every attached peripheral.
- The project's Miady bank listing/label available in the records says 5 V / 2.4 A, below the Pi's 2.5 A recommendation and below the 4–5 A system planning estimate. That estimate is a conservative target, not a measured load. A replacement bank must have published simultaneous output ratings for the Pi and peripheral branches.
- Do not parallel two USB VBUS outputs or inject another 5 V supply into the bus-powered HAT. Use a hub with a documented, protected external power input or a separately designed power path with VBUS isolation and branch protection. Keep high-current paths out of GPIO and narrow signal traces.
- Proxmark connects to the Pi through its USB device port and a downstream HAT port. It does not need direct GPIO or ESP32 connections. The Proxmark subcircuit still needs exact revision/BOM, antenna coils and tuning, assembly plan, and electrical validation before it can be treated as a manufacturable clone.

## Work needed for a real sign-off

1. Resolve the one remaining GND track-to-via connection after checking its intended return path and RF/coil constraints. Remove the redundant overlapping top GND area if the original zone alone refills and preserves the connection. Refill and rerun DRC.
2. Inspect every DRC item. Keep the 0.203 mm rule only after confirming the chosen fabricator's minimum width/clearance. Review the Proxmark supply and antenna-drive nets against actual peak current, copper weight, voltage drop, and thermal rise; keep system power on separately protected branches.
3. Complete a source/load budget from the exact bank, Pi, HAT revision, ALFA, RTL-SDR (including bias tee if enabled), Proxmark, Chameleon, LILYGO, radio modules, and IR transmitter. Bench-test on a current-limited supply and measure voltage/current at each branch under combined peak operation.
4. Decide between a complete removable Proxmark unit and a custom clone. For a clone, verify exact parts/footprints, USB interface, regulators, antenna network, coils, and test points against the selected Proxmark revision; complete ERC and board review.
5. Measure the Pi/HAT, ALFA without antenna, Chameleon, LILYGO, display, antenna connectors, plugs, and cable bend radii. Check the mounting holes, antenna clearance, service access, and IR lens alignment against the enclosure CAD. Correct the IR location/edge openings if the intended placement is still the left side.
6. Once the native PCB is updated and all checks pass, export a fresh JSON and DRC report, inspect Gerbers, and only then decide whether it is ready to order. Do not power it from the battery bank until branch protection and the load test are complete.

**Conclusion:** The BoardOutLine cutout is removed and the live board is saved; the 3D view confirms the board is continuous where the large hole appeared. Rebuilding copper areas restored the DRC from 154 stale GND errors to one real open GND via-to-track connection. The existing top-layer GND areas overlap, and the narrow-track/current, power-distribution, Proxmark-coil, and mechanical-fit checks remain unresolved. The board is not ready to order or power on. The saved JSON export predates the outline edit and must be refreshed before release.

## References

- [Raspberry Pi Zero 2 W product brief](https://pip-assets.raspberrypi.com/categories/584-raspberry-pi-zero-2-w/documents/RP-008359-DS/raspberry-pi-zero-2-w-product-brief.pdf)
- [Waveshare USB HUB HAT product page](https://www.waveshare.com/product/iot-communication/wired-comm-converter/usb-hub-hat.htm)
- [Proxmark3 hardware description](https://github.com/Proxmark/proxmark3/wiki/Hardware-Description)

## Latest EasyEDA check (2026-10-11)

The active EasyEDA `PCB_neonred` window still reports **DRC Errors (1)** and **Nets (196 / 196)**. The remaining incomplete connection is `gge68790` (Via–Track) on GND, between via `gge38672` and track `gge5612`. This supersedes the older saved-audit track ID `gge95612`; the current live window is the authority. I did not route the connection: EasyEDA reported incoming user input during the selection attempt, so I stopped to avoid colliding with edits in progress. No board change was made in this check. Reinspect the pair in EasyEDA, route GND with clearance, refill copper, and rerun DRC before fabrication.

## Follow-up check and purchase BOM update (2026-10-11)

The live EasyEDA board was reopened and the remaining incomplete item was inspected directly. EasyEDA still reports one incomplete GND connection (`gge68790`, via `gge38672` at 130.556, -228.092 mm to BottomLayer track `gge5612`, from 130.937, -182.637 to 133.437, -168.137 mm). The connection spans approximately 60 mm; a direct path would pass through the Pi module keepout/occupied area and across the Proxmark region. I did not delete the via or force an unreviewed GND route, since either could break the RFID return path or mechanical fit. No live PCB changes were made in this check. The board remains not cleared for fabrication or power-on.

The purchase BOM was refreshed in `BOM_NEONRED_purchase-list_2026-10-11.csv`. It replaces the discontinued RTL-SDR Blog V4 with the currently sold V4L Lite and supplies current single-quantity prices for the encoder, five through-hole switches, capacitors, IR receiver/emitters, and through-hole IR driver parts. The known line-item subtotal is $154.63; including a clearly marked $65 Ka-band chain planning allowance gives $219.63. Prices exclude shipping/tax and may change. Four rows remain deliberately unpriced: Proxmark clone/antennas (the imported schematic is not a validated purchasing BOM), power branch/hub path (needs a safe topology first), PCB fabrication (quote final production files), and enclosure (quote final CAD/material). These are engineering/quote holds rather than unresolved shopping searches.

The Ka-band $65 entry is only a budget placeholder, not a selected part or functional guarantee. The cited project reference estimates a converter and antenna but does not provide a vetted turnkey combination. The integrated Proxmark and power path remain the largest blockers to buying/fabricating safely.

## Latest PCB correction (2026-10-11)

In the active `neonred` project, I rebuilt the copper fills; the two reported track-to-copper clearances disappeared. I then added a **BottomLayer GND copper area** across the center of the board, between the controls and Proxmark section, overlapping the Proxmark GND via and the controls GND return. After another fill and EasyEDA DRC run, the Design Manager reported **DRC Errors (0)** and **Nets (196 / 196)**. The board was saved in EasyEDA and exported to `PCB/NEONRED-live-PCB-DRC0-2026-10-11.json` (2,291,258 bytes, 1,181 shapes, five copper areas, 334 vias). This supersedes the earlier one-open-GND audit. A DRC pass only checks the configured layout rules; it does not validate load current, RF behavior, complete wiring, or physical fit.

The duplicate-prefix warning is separate from PCB DRC. EasyEDA identifies the schematic `savecopy` within `neonred` as duplicating C3, C4, IC2 and other references in `Sheet_1`. The full project was copied to a separate EasyEDA project named `neonred-schematic-backup-2026-10-11` for preservation. The original `savecopy` still remains in `neonred` because an automated approval review rejected removing it under the earlier instruction not to touch savecopies. Do not convert/import the whole active project schematic into the PCB until that duplicate sheet is removed or explicitly excluded, or the resulting netlist could contain duplicate components.
