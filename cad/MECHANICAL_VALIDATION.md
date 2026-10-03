# Mechanical design and validation plan

This is the first editable enclosure design for the current 190 x 110 mm carrier PCB. The matching model is `Cyberdeck_Enclosure.scad`. It produces a removable service tray, base, lid, keyboard frame, ESP32 cradle, Chameleon sled, generic antenna pivot and battery hook. All dimensions are millimetres.

## Confirmed source dimensions

| Item | Design envelope | Evidence | Status |
| --- | --- | --- | --- |
| Carrier PCB | 190 x 110 x 1.6 | Current native PCB and full-size template | Verified digitally |
| Carrier mount holes | 20 holes; 16 carrier plus four Pi holes | Current template audit | Verified digitally |
| HAT | 65 x 30, four 3 mm holes at 58 x 23 | Waveshare USB HUB HAT SKU12694 drawing | Verified from drawing |
| HAT header cutout | 51.8 x 8, R1 | Current PCB/template | Verified digitally; physical header still required |
| CardKB | reserve 88 x 54 x 6.3 | M5Stack drawing/product page conflict | Reserve only |
| Pi Zero 2 | 65 x 30 body, exact carrier holes | Pi drawing/current PCB | Hole pattern verified digitally |
| LILYGO | 60 x 25.5 x 10, active screen 19.8 x 44.22 | LILYGO basic AMOLED documentation | The photo identifies the basic/no-touch type; rev V1 vs V2 still needs a physical check |
| HDMI LCD | 85.01 x 56.41 board | Waveshare SKU12824 drawing | Panel aperture and plug depth need physical check |
| Miady bank | 96 x 64 x 26 maximum envelope | AS-TPB21 manual | Confirm against the bank in hand |
| Chameleon Ultra SE3 | 40 x 24 x 8 adjustable envelope | supplier references, not an official dimensional drawing | Must measure before printing |

## Current fit conclusion

The service tray holds the carrier PCB on 5 mm M2.5 standoffs. The HAT is mounted on the carrier's four dedicated holes with a 1 mm separator and its underside header passes through both the carrier slot and tray clearance. The base reserves 39.6 mm from the tray top to the keyboard-frame plane.

The HAT uses almost the full available plan area underneath the CardKB. The Chameleon cannot be mounted beside the HAT at the same height. The model puts it in a separate under-tray sled with a thin plastic RF window. This arrangement must be range-tested because nearby copper, battery material and the case can reduce RFID performance.

The base remains parametric because the following cannot be established from product drawings: mated HDMI/USB connector depth, USB cable bend radius, actual power-bank dimensions, Chameleon dimensions, antenna pigtail/bulkhead shape and the card keyboard's real screw positions.

## Physical measurement checklist

Print the existing mounting template at actual size first. Confirm its 100 mm calibration line before placing hardware on it.

| Check | Pass criterion | Action if it fails |
| --- | --- | --- |
| PCB, Pi, HAT and carrier mounts | Every hole accepts a screw without forcing | Correct the CAD mount coordinates, never enlarge the PCB holes by drilling blindly |
| HAT underside header | Header clears 51.8 x 8 mm slot with at least 0.5 mm around it | Increase the tray-only cutout first; alter PCB only after a separate electrical/copper audit |
| Pi-HAT cable | Micro-USB plug clears the keyboard and has no sharp bend | Rotate the HAT or change to a short right-angle data cable |
| HAT plus keyboard | Keyboard closes without touching hub plugs, header or standoffs | Increase `base_h` before printing the final base |
| Chameleon sled | Device slides in, buttons/USB remain reachable, and tags work through the RF window | Resize its adjustable rails or move it to a front service bay |
| LCD | Board clips in without force; HDMI and power plugs bend naturally | Change `lcd_xy`, lid cavity depth or cable exit channel |
| LILYGO | USB-C, BOOT and RESET remain reachable; screen aligns to the closed-lid window | Change `lily_xy` and `lily_window` in the model |
| Hinge/lid | Opens to at least 105 degrees, closes without cable pinch | Adjust hinge ears and the rear cable channel |
| Antennas | Folded arms clear the lid, battery and hands | Choose actual RF pigtails and finalise the arm length/clevis geometry |
| Screw heads | No metal fastener touches carrier copper | Use the required insulating washers and recheck clearance |

## Print order

1. Print only the HAT-slot and keyboard/HAT section as a low-infill test slice.
2. Place the HAT, its data cable and keyboard on the test slice. Confirm height before printing the full base.
3. Print the service tray. Test every carrier, Pi and HAT screw location with nylon M2.5 hardware.
4. Print the keyboard frame and ESP32 cradle. Neither assumes a direct mounting hole in the module.
5. Print the lid and check the display and LILYGO window using paper cutouts before installing electronics.
6. Print antenna pivots only after selecting the actual RP-SMA/SMA bulkhead pigtails.

## Operating access designed into the enclosure

- The removable underside service tray gives access to the Pi boot card, USB leads, HAT, Chameleon, level shifter and regulator without disassembling the lid.
- The ESP32 cradle leaves its USB-C and BOOT/RESET end open. Its lid window remains visible when closed.
- The right-front panel provides the encoder hole and peripheral-supply switch opening.
- The left side has a wired IR opening.
- Rear and right cable exits are oversized provisional channels. They need to be finalised using real plugs and strain-relief grommets.
- The lid has a display cavity with edge clips rather than guessed LCD mounting holes.

## Explicit limits

This is a design package, not proof of physical fit. Do not send the PCB, enclosure or final fabrication files for manufacture until the checklist has been completed with the actual parts. In particular, do not use a metal screw head directly against the carrier PCB and do not permanently install the Chameleon before testing its RFID range in the proposed bay.
