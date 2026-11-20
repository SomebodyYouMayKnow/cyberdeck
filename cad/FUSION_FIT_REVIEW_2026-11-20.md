# Fusion fit review, 2026-11-20

## Export

`NEONRED_Cyberdeck_Case_FitCheck_2026-11-20.step` was exported from the live Fusion 360 document `cad case cyberdeck`. The STEP contains the case, open lid, 7-inch Waveshare display fit-check bodies, 226 x 126 mm PCB envelope, INIU BI-B5 battery envelope, Pi Zero 2 W + Waveshare USB Hub HAT underside envelope, CardKB, Chameleon Ultra SE3, LILYGO T-Display-S3 AMOLED, five button envelopes, rotary encoder, and four PCB support rings plus four washers.

Obsolete hidden 3.5-inch display test bodies, old battery reference, draft hinge bodies, and the two legacy cylinders are not in the STEP export. They remain hidden in the Fusion document so the original timeline/reference geometry is preserved.

## Fit inputs and sources

- Carrier PCB: 226 x 126 x 1.6 mm, positioned at x=3..229, y=3..129, z=33..34.6 mm. The case cavity is modeled with 1 mm clearance on every edge.
- M5Stack CardKB: 84.6 x 54.2 x 6.5 mm, from [M5Stack's specification](https://docs.m5stack.com/en/hat/hat-cardkb).
- Chameleon Ultra SE3: 40 x 24 x 8 mm, from [Chameleon Ultra hardware documentation](https://github.com/ChameleonUltra/docs/blob/main/hardware.md).
- LILYGO T-Display-S3 AMOLED: current fit block is 58 x 25 x 10 mm and is explicitly an estimate. A published manual gives approximate non-touch dimensions of about 60 x 25.5 x 10 mm; verify against the exact touch/non-touch revision and its official CAD before making the enclosure. The current fit block is therefore slightly undersized.
- Waveshare 7-inch HDMI LCD (C): 164.9 x 106.96 x 8 mm, per [Waveshare](https://www.waveshare.com/wiki/7inch_HDMI_LCD_%28C%29).
- Pi Zero 2 W + USB Hub HAT: 65 x 30 mm board outline with a 14 mm under-board stack envelope. The 14 mm projection is a conservative estimate, not a measured connector model.
- Battery: INIU BI-B5 nominal 134 x 71 x 25.5 mm envelope, placed at x=49..183, y=56.5..127.5, z=0.5..26 mm.
- Button and rotary encoder bodies are simple fit envelopes, not manufacturer CAD models.

## Results

### Device envelopes overlap

The existing 58 x 25 mm LILYGO envelope overlaps the Chameleon envelope by 0.5 mm in Y (the X and Z ranges overlap too). The LILYGO envelope also clears the encoder by only 0.2 mm. With the approximate 60 x 25.5 mm LILYGO dimensions, the estimated Chameleon overlap becomes 0.75 mm and the encoder envelope overlaps by about 0.05 mm. These clearances are too small for a reliable physical fit. Move the LILYGO and/or Chameleon placement in the PCB and matching fit model to create at least 1 mm clearance; then recheck the actual board revisions and antenna/connectors. Do not treat the current locations as clash-free.

### Closed-lid height is not clear

The board top is z=34.6 mm and the modeled closed-lid display/inside face is z=42 mm, giving 7.4 mm nominal headroom. CardKB uses 6.5 mm, leaving 0.9 mm. Chameleon is 8 mm tall, exceeding that headroom by 0.6 mm. LILYGO is estimated at 10 mm, exceeding it by 2.6 mm. The encoder envelope is 14 mm, exceeding it by 6.6 mm. The lid therefore cannot be confirmed to close with the current screen and component stack. The case needs a deeper lid/spacer or local relief, with hinge alignment and display mounts rechecked, before printing a closing case.

### Pi/HAT and battery

The HAT underside envelope is x=29.5..94.5, y=25..55, z=19..33 mm. The bank is x=49..183, y=56.5..127.5, z=0.5..26 mm. Their X and Z intervals overlap, but their Y intervals are disjoint by only 1.5 mm. There is no intersection in the current box model; the clearance is tight and depends on the assumed 14 mm HAT/connector projection. Measure the actual through-board connector stack and bank case before printing. The bank also needs its USB-C extension/port orientation checked against the modeled opening.

### PCB mounting and flatness

The carrier has 20 NPTHs in the CAD source: 12 at Ø6.299 mm (four inner board fasteners and eight perimeter lip/case fasteners) and eight at Ø5.415 mm (CardKB/Chameleon clearances). The case screw bores/support-ring IDs are Ø3.2 mm. The larger PCB holes are clearance holes; the fit model bridges them with four concentric OD10/ID3.2 support rings below the board and OD10/ID3.2 washers above it. The support tops are at z=33 mm, the same as the PCB underside; the washers start at z=34.6 mm. This makes the board plane level in the model, with about 1.85 mm radial bearing overlap around each Ø6.299 mm hole. The rings and washers are separate fit-check solids in STEP, not evidence that the actual screws, washer material, or case attachment have been validated. Confirm the screw/washer stack and integrate the standoffs into the printable base if they are intended to be printed with it.

## Decision

This is an updated fit-check STEP, not a manufacturing-ready enclosure. The STEP export itself is valid, but the model identifies a LILYGO/Chameleon clash, almost-zero encoder clearance, insufficient closed-lid height, and an unmeasured 1.5 mm HAT-to-battery gap. Resolve those items and verify exact part revisions before printing the enclosure. Mechanical review does not verify PCB electrical function.

