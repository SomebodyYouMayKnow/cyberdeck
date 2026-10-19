# NEONRED external power plan — prototype wiring, not yet bench-approved

This plan keeps Pi/HAT current off the carrier PCB. The latest saved PCB export has no onboard power converter, fuse, reverse-polarity protection, or high-current Pi path. JP4 is only an auxiliary rail input.

## Intended branches

1. Connect the power source to Raspberry Pi Zero 2 W `PWR IN` with an intact, correctly rated USB cable. Connect the Waveshare hub upstream to the Pi OTG/data port. Never open the sealed power bank or splice its cable onto the PCB.
2. Use one owned Miady bank only for the auxiliary branch, after reading its output label. Run its regulated 5 V positive to JP4 pin 1 (`+5V_EXT`) and ground to pin 2. Use the same auxiliary 5 V/GND source as the Pololu regulator input; never connect the Pi bank's positive output to this branch.
3. Feed an off-board Pololu D24V10F3 from that regulated auxiliary 5 V/GND source. Return its 3.3 V output to JP4 pin 3 (`3V3_AUX`) and ground to pin 4. Use the current-limited USB output and the regulator's short-circuit/over-current protection; the regulator has no reverse-voltage protection. Check polarity and voltage with a meter before connecting it. It is a 1 A-class regulator with thermal limits, not a whole-system power supply.
4. Keep grounds common where SPI, I²C and IR signal lines cross between the ESP32 and peripherals. Keep the Chameleon Ultra SE3 on its own USB/BLE power arrangement.

## Candidate battery status

The BOM lists the INIU BI-B5 20,000 mAh bank for the Pi branch only. INIU specifies 5 V/3 A from a single output and a 5 V/3 A (15 W) limit when multiple outputs are active ([manufacturer specifications](https://iniushop.com/collections/portable-fast-charging-series/products/iniu-megapower-20000mah-portable-charger)). Raspberry Pi recommends a 5 V/2.5 A supply for Zero models. The single-output rating is enough to meet that recommendation on paper, but does not prove the four-port hub plus all USB devices fit within the remaining current. **Do not assume this bank can power the whole deck by itself.**

Use a current-limited bench supply for initial tests. The proposed two-bank arrangement keeps Pi/HAT and JP4 positive outputs separate, with shared ground only as required for signal reference. Before field use, measure Pi/HAT and auxiliary branch peaks independently and together, then decide whether the existing banks have enough margin. A five-hour runtime is not established.

## Wiring and protection decision still required

- Confirm each power bank's regulated 5 V output and built-in current/short-circuit protection from its exact model label/manual. Add an appropriately rated inline fuse to any exposed/cut-wire auxiliary harness after checking the harness wire gauge and measured load; do not guess a fuse rating.
- JP4 has both 5 V and 3.3 V rail pins. Use the keyed 4-pin mapping above; do not land a two-wire battery lead across an unidentified pair. The Adafruit USB-A plug breakout in the BOM is a 5 V/GND power-only harness at red/black; insulate the data wires and meter-check before connecting.
- Do not feed the Pi through JP4 or from the ESP32/LILYGO 5 V pins. The Pi must receive its own regulated supply through `PWR IN`.
- Do not inject a second 5 V source into the USB hub's upstream VBUS; that can backfeed the Pi or cause supplies to contend.
- The `SCH_cyberdeck-completed-power-option2-2026-10-18.json` file is a saved candidate, not proof that the live EasyEDA schematic and PCB are synchronized. The actual board has to be re-exported and reviewed after any approved wiring changes.
