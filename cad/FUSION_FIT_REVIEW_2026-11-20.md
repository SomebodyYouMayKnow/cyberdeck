# Fusion fit review, 2026-11-20

## Updated STEP

`NEONRED_Cyberdeck_Case_FitCheck_2026-11-20.step` is exported from the current live Fusion document `cad case cyberdeck`. It is a mechanical fit-check assembly, not a fabrication-ready enclosure. The open-lid STEP includes the case, hinge/lid, 7-inch display fit-check geometry, PCB envelope/supports, power-bank envelope, Pi/USB-HAT underside envelope, CardKB, Chameleon Ultra SE3, LILYGO board envelope, controls, and antenna/port openings modeled in the document.

## Checked placements and geometry

- The live EasyEDA board `cyberdeck-completed / PCB_cyberdeck-completed` showed A2 (`ESP32-S3-AMOLED-1.91`) at X=185.547 mm, Y=29.083 mm, rotation 0°.
- The Fusion board-to-case datum is +4 mm X and +52 mm Y. Applying that transform to the A2 EasyEDA footprint outline gives a portrait fit envelope of X=189.547..215.047 mm, Y=27.267..81.083 mm. The old landscape fit block was removed; the Fusion envelope now uses those outline dimensions and position. Its 10 mm height is an estimate.
- The corrected LILYGO envelope has 11.917 mm Y separation from the Chameleon envelope and 11.547 mm X separation from the encoder envelope. These boxes do not clash in the current fit model.
- PCB fit envelope: 226 x 126 x 1.6 mm at X=3..229, Y=3..129, Z=33..34.6 mm. The case cavity relief provides nominal 1 mm perimeter clearance while retaining the modeled PCB hole centers.
- Four support rings and washers are centered on the modeled PCB fasteners. Each ring is OD10/ID3.2 x 33 mm; each washer is OD10/ID3.2 x 1 mm. They support the PCB underside at Z=33 mm and are intended to keep the board plane level. The 6.299 mm PCB clearance holes are larger than the 3.2 mm M3 screw passages by design; the rings and washers bridge the clearance-hole annulus.
- The Pi/USB-HAT underside keepout and battery boxes do not intersect in the current model, but their nearest Y-edge clearance is only 1.5 mm while their Z ranges overlap. This depends on an estimated 14 mm underside stack and must be checked against the exact HAT revision and bank before printing.

## Items still not confirmed

- **The closed assembly is not verified to clear.** The modeled lid inner face is at Z=42 mm; the PCB top is Z=34.6 mm, leaving about 7.4 mm. The modeled CardKB is 6.5 mm high, Chameleon is 8 mm, LILYGO is estimated at 10 mm, and the encoder envelope is estimated at 14 mm. Chameleon, LILYGO, and the encoder exceed that nominal headroom. The open-lid STEP cannot prove that the lid closes. The lid needs added depth or properly aligned local relief, followed by a closed-position check.
- **The LILYGO lid aperture is currently misaligned.** It remains at X=170.25..193.25 mm, Y=54.5..101.5 mm from the old landscape fit. The corrected A2 board envelope is X=189.547..215.047 mm, Y=27.267..81.083 mm. The old opening only partly overlaps that envelope. The opening was not moved in Fusion because the closed-lid transform and the exact panel active-area offset were not verified. Reposition it in the lid's closed coordinate system and compare it with the exact LILYGO DWG before printing.
- Module height, connectors, cables, antenna pigtails, battery port placement, hinge tolerances, and fastener lengths are not fully represented by manufacturer-accurate CAD. Several are envelope estimates. Confirm the exact purchased revisions and measure their protrusions.
- The fit-check bodies for the seven-inch display and external modules are simplified. They are not supplier CAD and do not validate display cable bend radius or the USB-C pass-through fit.
- The enclosure fit audit is not an electrical review of the PCB or a guarantee that the assembled cyberdeck works.

## Conclusion

The LILYGO CAD orientation and placement now match the live EasyEDA A2 footprint outline. The visible layout is corrected, but the enclosure is **not ready to print as a closed, finished assembly** until lid clearance and the screen aperture are resolved and the estimated connector/module clearances are checked against actual hardware. The STEP is useful for reviewing the current open-lid fit arrangement.
