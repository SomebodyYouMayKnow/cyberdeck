# NEONRED PCB and Proxmark readiness audit

**Date:** 2026-10-11  
**Result:** Not ready for fabrication or a power-on claim.

## Evidence checked

- Fresh EasyEDA export captured on 2026-10-11 after the safe DRC cleanup: `PCB/neonred-live-PCB_2026-10-11-fixed.json` (EasyEDA Standard 6.5.51). The prior export is retained for comparison.
- The fresh board has 170 component footprints and 642 tracks. It includes the Proxmark reference designators (`PROXIC1`, `PROXIC2`, `PROXSV1`, etc.), an onboard `USB-MINIB` connector (`PROXSV1`), and separate outlines for the main board and the imported Proxmark area.
- The main rectangular board outline is about 90 × 180 mm. The inner Proxmark-area rectangle is about 81.3 × 51.3 mm. Four separate holes sit near the left/right edges in the upper/middle region, not at the board corners. They may be the intended case fasteners, but their purpose and fit to the enclosure still need verification. The Pi footprint also has its own four module-hole locations.
- The Raspberry Pi Zero 2 W footprint has 40 GPIO pads plus four mechanical holes, but all GPIO pads retain isolated names (`PI1_1` through `PI1_40`) and have no routed tracks. Thus the carrier PCB does not currently take power from the Pi header or connect Pi GPIO to other circuits. Pi USB can still host the Proxmark through a USB cable; power and any other signals need their own explicit connection path.
- The single 940 nm IR LED (`D1`) and TSOP38238 receiver (`U3`) are at the top edge of the carrier, about 3.5 mm in from the board edge, and about 15 mm apart. They are not at the left side in this layout. Both footprint metadata entries say `DRAFT - VERIFY BEFORE FAB`; confirm lens orientation and the case openings before release.
- The Proxmark USB D+ and D− nets terminate at its Mini-B connector and local USB protection/resistors. That is the correct sort of device-side interface, but it does not by itself establish a connection to the Pi: the Mini-B port must be reachable and connected by a data cable to a downstream host port on the Pi's USB hub, or a separately engineered USB link must be added. Do not connect these signals to GPIO. No Proxmark-to-ESP32 link is required.
- The layout contains the four-pin Proxmark antenna connector (`PROXSV2`), but no LF/HF antenna coils are part of this board export. The antennas must be supplied, connected, tuned, and validated for the selected hardware revision; the connector alone does not provide RFID capability.
- The imported Proxmark circuit is predominantly SMD (including 0603 passives and fine-pitch ICs). This conflicts with the project's through-hole preference and requires either professional assembly or a deliberate redesign/assembly plan; it is not a hand-soldered through-hole-only board.
- Initial DRC reported 526 findings: 522 track-width warnings, 3 silk/text-clearance warnings, and 1 incomplete GND connection. I removed the stray `route15` text object (`gge23615`), which was colliding with three Proxmark header pads/a via; after saving and rerunning DRC, the count fell to 523 and all three text-clearance warnings disappeared. The GND track-to-via warning remains.
- The 522 remaining DRC findings are existing 0.203 mm (8 mil) routed traces that are below the board's 0.254 mm default minimum. I left both the traces and 0.254 mm rule unchanged because many flagged nets include Proxmark analog, supply, and antenna-drive paths. A general rule change would only hide the mismatch and would not verify current capacity. Assess those nets against the selected fab, copper weight, actual peak currents, temperature rise, and voltage drop; widen/re-route only where justified.
- The current EasyEDA Proxmark pages are a reference-based schematic draft. `reference/proxmark3/NEONRED-integration-notes.md` records 620 preserved reference pin-to-net memberships, but explicitly says that this does not verify conversion, footprints, electrical correctness, or physical operation.
- The Proxmark reference schematic still needs exact orderable parts, crystal values, population options, USB and regulator current checks, antenna tuning, and complete ERC/DRC/layout review.
- The JSON export is a snapshot of the live PCB after the Proxmark placement. It confirms the geometry and object/net labels in that snapshot, but cannot prove electrical performance, source power capacity, antenna tuning, or physical fit.

## Interconnect recommendation

- Run Proxmark client software on the Raspberry Pi and connect the Proxmark USB device interface to one downstream USB-A port on the Waveshare USB HUB HAT. Use the appropriate intact data cable for the exact Proxmark connector.
- Do not connect the Proxmark to Raspberry Pi GPIO. USB D+/D−, ground, and the intended USB 5 V supply path are the host interface; do not parallel independent 5 V sources. The Pi header is not currently wired to this carrier, so the Pi cannot power carrier circuits through that header as drawn.
- No direct Proxmark-to-ESP32 wiring is needed. Any optional Pi/ESP32 control link should be a separately designed interface and is not required for Proxmark operation.
- Keep Proxmark LF/HF antenna circuits and coils as their own tuned RF subsystem; preserve the reference keepouts and do not place them against metal or the other radios without RF validation.

## Power status

- Raspberry Pi's product brief specifies a 5 V, 2.5 A input supply recommendation. This is not proof that 2.5 A is available to USB peripherals after the Pi and HAT loads.
- Waveshare's page for the user's 4 Port USB HUB HAT states 5 V operating voltage and identifies four USB ports plus an onboard USB-to-UART converter. The published product summary does not state a guaranteed combined downstream current budget. Do not assume the HAT can power all peripherals at their peak current.
- The exact Miady battery-bank model/output label, HAT revision and source capability, Proxmark variant/current, ALFA adapter load, and simultaneous peak loads are not specified in the files checked. Therefore an aggregate current budget and voltage-drop/thermal check cannot be completed.
- Do not connect the carrier's battery-bank output directly to Proxmark or other rails, and do not join separate USB VBUS outputs. Establish a documented source/load budget and measure the assembled peak load before approving the power system.

## Required before calling the board ready

1. Resolve the remaining unrouted GND track-to-via connection; the three silk-clearance errors are now fixed. Rerun DRC after reconnecting/rebuilding the intended GND copper.
2. Review all 522 0.203 mm track-width findings across 127 nets. Verify the intended board house's minimum widths, copper weight, clearance, and current capacity; widen or re-route power/coil paths where required. Do not simply change the rule to 0.203 mm.
3. Verify whether the Proxmark is intended to be a custom clone or an assembled removable USB instrument. The current import is a complex SMD circuit, not a validated manufacturing release; reconcile the schematic, exact BOM, footprints, antenna network/coils, and test points against the selected Proxmark hardware revision.
4. Make the `PROXSV1` Mini-B connector accessible in the enclosure and route a USB data cable from it to a downstream USB-A host port on the Pi hub. If instead routing USB directly on the carrier, design and verify the full USB interface and controlled-impedance differential pair; do not route USB D+/D− to GPIO.
5. Confirm case-mount hole locations and Proxmark/module mounting against the actual enclosure and physical parts; the current four holes are not perimeter case mounts.
6. Complete the total 5 V source budget from each module's peak/current-at-startup specification. Include cable/connector losses, hub consumption, Pi load, ALFA, RTL-SDR, Proxmark, ESP32, and any other powered accessory. Then verify with a current-limited bench supply and measurement at the farthest load.
7. Run EasyEDA ERC and DRC on the saved current schematic/PCB, inspect all unrouted nets and USB routing, and physically measure the modules and clearances.

**Readiness conclusion:** The live PCB now has zero text-clearance findings, but still has one unrouted GND connection and 522 minimum-width DRC findings. Proxmark can be controlled by the Pi through USB; no ESP32 interconnect is necessary. The total power budget, antenna behavior, and physical mounting/connector access remain unverified. The board is not yet ready to order or power.

## References

- [Raspberry Pi Zero 2 W product brief](https://pip-assets.raspberrypi.com/categories/584-raspberry-pi-zero-2-w/documents/RP-008359-DS/raspberry-pi-zero-2-w-product-brief.pdf)
- [Waveshare 4 Port USB HUB HAT product page](https://www.waveshare.com/product/iot-communication/wired-comm-converter/usb-hub-hat.htm)
- [Proxmark3 hardware description](https://github.com/Proxmark/proxmark3/wiki/Hardware-Description)
