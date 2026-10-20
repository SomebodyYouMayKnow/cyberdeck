# Mechanical design and validation

This is an editable enclosure and printed-retainer concept for the current NEONRED PCB export. It is not a verified physical fit. The model is `Cyberdeck_Enclosure.scad`; all dimensions are millimetres.

## Current PCB reference

| Feature | Current model | Source/status |
| --- | --- | --- |
| PCB outside envelope | 226 × 126 × 1.6 mm, including eight mounting lips | Current EasyEDA source export in `EasyEDA/NEONRED_PCB_2026-10-19.json`; digital envelope only |
| Main PCB area | 210 × 110 mm, offset 8 mm from the envelope origin | Reconstructed from the saved board outline |
| Board through-holes | 24 total in current live Gerber: 12 case mounts (four field + eight lips), 4 Pi mounting holes, 8 CardKB/Chameleon support holes | The eight support holes were imported into the live EasyEDA board; native EasyEDA DRC reported 0 errors |
| Enclosure outside | 242 × 142 mm | CAD allowance of 8 mm nominal around the PCB; hinge and port clearances remain provisional |
| CardKB reserve/body | 88 × 54 mm reserve; 88 × 54 × 5 mm product size | M5Stack product listing; the PCB document also labels an 84 × 54 mm body. Measure the owned unit and connector before finalizing the recess |
| Chameleon reserve | 60 × 30 mm | Outline in the live PCB document; the enclosure holder uses a centered 40 × 24 × 8 mm provisional device envelope |
| ALFA AWUS036ACS | 55 × 25 × 12 mm placeholder | Not outlined or located in the current PCB; measure the owned adapter, USB plug and RP-SMA connector before placing its cradle |

## Printed supports and new PCB holes

- `keyboard_frame` is a recessed support/retainer around the CardKB reserve. Its four 2.8 mm printed holes align with four 2.751 mm NPTHs in the live carrier PCB and service-tray bosses. The CardKB itself is not drilled.
- `chameleon_retainer` fits inside the PCB's 60 × 30 mm document reserve and captures a centered 40 × 24 mm device with side rails. Its four 2.8 mm printed holes align with four 2.751 mm live PCB NPTHs and service-tray bosses. The lower pair is shifted 2 mm inward to clear a routed trace.
- `alfa_cradle` is an independent, selectable printed cradle with four mounting holes. It remains unplaced: the current PCB has no ALFA outline or agreed location, and the placeholder body dimensions omit confirmed connector/cable keep-outs. No ALFA holes were added to the PCB.
- The tray posts follow 12 case mounting holes and eight component-support holes. Use insulating washers and keep metal fasteners clear of copper.

Export individual parts by changing the `part` selector in the SCAD file. The `assembly` view is only a visual concept. The loose ALFA cradle is not shown in that view because its position is not established.

## Required physical checks before printing the final enclosure

1. Print the 1:1 PCB template and confirm its calibration, lip locations, all 12 case holes, and eight support-hole centers against the fabricated/owned PCB.
2. Measure the actual CardKB body, key/connector protrusions and cable direction. Check that the 88 × 54 mm frame does not cover keys or the connector, and transfer the four printed-frame screw axes to case bosses. Do not drill the CardKB itself based on this model.
3. Measure the Chameleon body including buttons, USB connector and cable bend. Confirm it fits the 60 × 30 mm reserve with retainer rails and that the intended RFID face is unobstructed.
4. Measure the ALFA adapter including its RP-SMA connector, antenna bulkhead and USB plug. Select a PCB/case location with cable and antenna clearance, then revise `alfa_xy` and the cradle before printing.
5. Confirm Pi, USB HAT, micro-USB cable, keyboard and lid clear one another through the full close/open motion.
6. Test the lid, hinges, service tray, screw-head access, cable exits and strain relief with real parts. Confirm no screw or support contacts exposed PCB copper.

## Source references and limits

- CardKB dimensions/reference drawing: [M5Stack CardKB v1.1 product page](https://shop.m5stack.com/products/cardkb-mini-keyboard-programmable-unit-v1-1-mega8a) and [CardKB v1.1 PDF](https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/static/pdf/static/en/unit/cardkb_1.1.pdf). The case/frame still needs a measurement of the actual unit and connector.
- Chameleon dimensions used as a placeholder: [Chameleon Ultra hardware wiki](https://github.com/ChameleonUltra/ChameleonUltra/wiki/hardware). Treat 40 × 24 × 8 mm as provisional until measured.
- ALFA model identity: [ALFA AWUS036ACS product page](https://www.alfa.com.tw/products/awus036acs_1). The 55 × 25 mm cradle envelope in this file is a placeholder, not a dimension verified from that page.

The live PCB adds eight non-plated mechanical holes; electrical shapes, tracks, component placements, and outline remain unchanged. EasyEDA reported 36 components, 29/29 nets, 0 DRC errors and generated a fresh Gerber archive. The STEP export is for the PCB plate only. The SCAD still needs a full render and physical fit check before printing the enclosure.
