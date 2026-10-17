# NEONRED unmatched parts and external purchase BOM

Updated: 2026-10-15

This file is a gap-filling BOM for the live LCSC list `BOM_neonred_PCB_neonred_2026-10-15` plus off-board items LCSC/EasyEDA cannot assemble. It is **not an order release**. The companion CSV now gives every row a sourcing link and either a checked price, owned/N/A status, or an explicit TBD where an exact safe part is not identified. Owned modules are called out so they are not re-purchased. See the companion CSV for all 41 row-level entries.

## Live LCSC result

The active LCSC page now reports **72 rows: 48 exact, 4 partial, 20 no match**. I corrected the catalog links for the four-position Hirose connector (row 59, C598157) and 2x10 shrouded header (row 60, C9039). The row 61 1x6 header still shows a fuse suggestion; C37208 is the likely 1x6, 2.54 mm header candidate, but I could not apply it through the available row editor. Row 62's Panasonic EVQQ1D06M remains on hold because the manufacturer marks it discontinued and its footprint still needs a land-pattern check.

The remaining partial rows 9 and 11 are false device matches: a bare nRF24L01 QFN IC was suggested for a complete radio module, and a Pi Zero W was suggested for the owned Pi Zero 2 W. Neither should be ordered as an LCSC replacement. The no-match items are retained in the CSV with the footprint/value information available from the current list; merged or generic rows need schematic-level identification before selecting MPNs.

The LCSC page still flags duplicate source rows **2, 3, 5, 7, 8, 10, 60, 61, and 72**. Current checkout state is **0 selected, $0.00**, with nothing added to cart or ordered.

## Power, USB, and owned external parts

The project notes identify a Miady 10,000 mAh USB power-bank two-pack as owned, with a stated 5 V / 2.4 A output per bank. That rating is below Raspberry Pi’s 5 V / 2.5 A recommended supply for Zero models, even before attached USB loads. Keep the battery outside the carrier PCB and do not parallel USB outputs. For a final build, choose a supply plan with a Pi branch meeting the Pi rating plus a separately protected peripheral branch sized from measured loads. A 4–5 A total 5 V capacity is only a planning target for the full system, not a tested draw.

Waveshare lists the USB HUB HAT package with a Micro-USB connector and cable; check the owned package before purchasing a replacement. Their instructions connect the Pi Zero’s USB OTG port to the hub’s USB HUB port. The Pi’s separate POWER IN still needs a qualified 5 V supply and low-drop cable. A USB-C data cable is needed for programming the LILYGO if one is not already on hand. Cables for the Chameleon or Mini-B Proxmark connection are conditional on the selected connection and device revision; the imported Proxmark USB circuit is not validated.

The CSV marks the Pi, HAT, LILYGO, CardKB, and nRF modules as owned/verify so they are excluded from repurchase. Chameleon and ALFA ownership must be checked against inventory before buying. RTL-SDR V4 remains a planned external module only if still in scope; it is not part of EasyEDA assembly.

## PCB order status

The live EasyEDA Design Manager currently shows **DRC Errors (0)** and **Nets (198/198)**. The current source export has four active copper layers (top, bottom, Inner1, Inner2), 643 tracks, and GND copper areas. This is a CAD connectivity/DRC result, not electrical or manufacturing sign-off. The Design Manager also shows **Components (0/0)** despite visible PCB objects, so the component-count/BOM linkage needs attention. The LCSC BOM still has 20 unmatched rows, 4 partials, and 9 duplicate-row alerts.

**Do not order the board or PCBA yet.** Remaining blockers include:

1. Resolve the 20 unmatched groups and the 4 partials, and remove or consolidate duplicate BOM entries without dropping real designators.
2. Verify the 4-layer stack with the selected board house and generate a fresh Gerber/drill/placement package from the same live PCB revision; inspect the large open area/cutout and board outline in the fabrication preview.
3. Validate the complete imported Proxmark circuit against a specific hardware revision, including the Mini-B USB path, MCU/FPGA part variant, all analog devices and antenna-coil/tuning networks. A populated symbol/footprint does not establish a working Proxmark.
4. Fix and verify IR emitter Q1/D1 footprints, pad mapping, drive current and LED current limiting; the existing D1 pitch/drill mismatch and Q1 pin-order concern remain documented in the PCB audit.
5. Complete power-tree, USB VBUS/backfeed, regulator, protection, thermal and branch-current checks. The carrier does not yet document a proven power path for the Pi/HAT and peripherals.
6. Resolve mechanical checks against physical devices: board edge, mounting holes, antenna keepouts, case screws, HAT clearance, and cable bend/access. Run the board house DFM and bench test before release.

## References

- [Raspberry Pi power guidance](https://www.raspberrypi.com/documentation/computers/getting-started.html): Pi Zero models use a recommended 5 V / 2.5 A supply.
- [Waveshare 4-Port USB HUB HAT](https://www.waveshare.com/product/usb-hub-hat.htm): four USB 2.0 ports, 5 V input, 65 × 30 mm board, and included micro-USB cable/connector.
- [Waveshare USB HUB HAT instructions](https://www.waveshare.com/wiki/USB_HUB_HAT): connect the Pi Zero USB port to the HAT USB HUB port.
- [LCSC C598157](https://www.lcsc.com/pt/product-detail/C598157.html), Hirose MQ172X-4PA(31), and [Hirose MQ172 series](https://www.hirose.com/en/product/series/MQ172).
- [LCSC C9039](https://www.lcsc.com/product-detail/C9039.html), BOOMELE 2.54-2*10P shrouded header.
- [LCSC C37208](https://www.lcsc.com/product-detail/Pin-Header-Female-Header_BOOMELE-Boom-Precision-Elec-2-54mm-1x6-Header_C37208.html), BOOMELE 1x6 header candidate.
- [Panasonic EVQQ1D06M](https://industry.panasonic.com/ap/en/products/control/switch/light-touch/number/evqq1d06m): lifecycle/footprint hold.

## Prices and sourcing links added (checked 2026-10-15)

The companion CSV now has a sourcing link and an explicit cost/status for every one of its 41 rows. Prices are USD before tax, shipping, and any import fees. `Owned; $0 incremental` means no planned repurchase, not that the item has no value. `TBD` and `N/A` are intentional where the source BOM does not identify a safe exact purchase part, the row is a DNP placeholder, or the item is on lifecycle/fit hold. Search links are discovery links, not approved substitutes.

Currently priced candidates include the LCSC HRS MQ172X-4PA(31) ($2.42), BOOMELE 2x10 header ($1.09), and BOOMELE 1x6 male header ($0.0419 each, but LCSC minimum order 10); the latter remains conditional on confirming that the PCB actually needs a male header. The cost and link are in the corresponding CSV rows.

External references priced in the CSV include the Chameleon Ultra SE3 ($39.99), ALFA AWUS036ACS ($29.99 listing), RTL-SDR Blog V4L Lite dongle ($37.95), a short USB-A-to-USB-C data cable ($3.95), and a short USB-A-to-Mini-B cable ($0.95). These are retail snapshots, not guaranteed checkout totals. The original RTL-SDR Blog V4 is end-of-life; the link is for the V4L Lite replacement. The Miady bank is recorded as owned and its observed listing price is reference-only; it still does not meet the documented power target. A replacement battery/power plan remains unpriced until simultaneous-output ratings and protection are established.

Other source pages used for these list prices: [MTools Tec Chameleon SE3](https://shop.mtoolstec.com/product/chameleon-ultra-se3/), [Best Buy ALFA AWUS036ACS](https://www.bestbuy.com/product/alfa-awus036acs-dual-band-ac600-usb-wi-fi-adapter-w-antenna-win-mac-kali-supported-black/C3F72LK6H4), [RTL-SDR Blog V4L listing](https://www.rtl-sdr.com/shop/page/2/?product-page=2), [Adafruit USB-A-to-C cable](https://www.adafruit.com/product/4473), [ProtoSupplies Mini-B cable](https://protosupplies.com/product/usb-2-0-type-a-to-mini-b-cable-1-ft/), and [LCSC BOOMELE header listings](https://www.lcsc.com/product-detail/C37208.html).
