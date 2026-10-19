# NEONRED order readiness — 2026-10-18

## Decision

**Ready to order a bare-board prototype from the current Gerber. Not yet confirmed as a working assembled system or ready for component assembly.** The active EasyEDA `cyberdeck-completed` PCB was saved, exported, and checked in the desktop app during this pass. The manufacturing package was generated after running DRC from that same live PCB.

## Completed from the live design

- [x] EasyEDA Design Manager shows **29/29 nets**.
- [x] EasyEDA DRC shows **0 errors**. The Gerber generation dialog offered to run DRC; the check completed and proceeded to fabrication export.
- [x] Exported a fresh EasyEDA PCB JSON: [PCB_cyberdeck-completed-order-candidate-2026-10-18.json](../PCB/PCB_cyberdeck-completed-order-candidate-2026-10-18.json).
- [x] Generated [NEONRED_Gerber_order-candidate_2026-10-18.zip](../PCB/NEONRED_Gerber_order-candidate_2026-10-18.zip) from the live board after DRC, then created [NEONRED_Gerber_bare-board-order_2026-10-18.zip](../PCB/NEONRED_Gerber_bare-board-order_2026-10-18.zip) with only fabrication layers and the order note.
- [x] Gerber setup reports **2 copper layers** and **210 × 110 mm** board dimensions. It showed a JLCPCB preview of **$14.88 for five green boards** (shipping/tax excluded).
- [x] Verified that the upload archive opens and contains top/bottom copper, top/bottom solder mask, top silkscreen, top paste, outline, plated/non-plated/via drill files, and the fabrication order note. The descriptive DocumentLayer was omitted from the upload copy. `Gerber_BoardOutlineLayer.GKO` carries the board outline.
- [x] Updated [the purchase BOM](../BOM.csv) with the prototype-board quote and distinct Pi and auxiliary power-source roles.

These checks cover EasyEDA's configured geometry rules and exported file structure. They do **not** prove all component connections are electrically correct, that the chosen wire/regulator can carry every peak, or that the assembled device boots and works.

## Power and assembly are still prototype tasks

- `JP4` pinout in the project notes: pin 1 `+5V_EXT`, pin 2 GND, pin 3 `3V3_AUX`, pin 4 GND. The rails are inputs. The carrier PCB does not generate or protect them.
- The Raspberry Pi Zero 2 W must receive regulated 5 V through its own intact micro-USB `PWR IN` cable. Raspberry Pi recommends a 5 V / 2.5 A supply for Zero models ([official guidance](https://www.raspberrypi.com/documentation/computers/getting-started.html)). Do not feed the Pi or USB hub through the carrier's small traces, and do not splice another 5 V source into the Pi-to-HAT upstream USB cable.
- The BOM lists the INIU 20 Ah bank for the Pi branch only. Its shared multi-port maximum is 5 V / 3 A (15 W); use one output only and verify the exact label/model. It is not evidence that the Pi plus all HAT peripherals can run simultaneously without a load test.
- The BOM lists one owned Miady bank for an auxiliary branch, but its exact label/current rating still needs checking. A Pololu D24V10F3 external regulator can provide `3V3_AUX` from regulated 5 V and is rated up to 1 A subject to thermal limits; manufacturer notes it has overcurrent/short-circuit protection but **no reverse-voltage protection** ([specifications](https://www.pololu.com/product/2830)). Confirm wiring polarity with a meter before connecting it.
- Treat the bank outputs as separate positive rails. Do not tie their +5 V outputs together. A shared ground may be needed as the signal reference when the attached interfaces connect; measure and verify the chosen wiring before connecting modules.
- The power estimate for the complete deck is still only a planning estimate, not a measured load. USB peripherals share the Pi/HAT branch; HAT port current and the combined current under Wi-Fi, SDR, RFID, radio, display, and IR operation have not been measured. Five-hour runtime is not confirmed.
- Mechanical clearances, exact owned-module revisions, and bench tests remain open by design. No parts were energized or tested in this pass. Do not interpret bare-PCB readiness as permission to power up an unchecked assembly.

## Purchase scope

The Gerber is ready to submit to JLCPCB for **five bare two-layer prototype boards** at the displayed preview price. It is not a PCBA/one-click-assembly order: the board includes external development modules and through-hole parts. Order this fabrication package as a bare PCB only; assemble components after checking the physical footprints and power wiring. The full BOM includes separate purchase links and prices where currently known; verify prices, stock, and exact item revisions at checkout.
