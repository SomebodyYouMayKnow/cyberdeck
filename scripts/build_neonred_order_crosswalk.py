"""Annotate the live EasyEDA BOM with sourcing status; never guess LCSC codes."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "PCB" / "NEONRED-live-PCB-BOM-2026-10-12.csv"
OUTPUT = ROOT / "PCB" / "NEONRED-order-parts-crosswalk-2026-10-12.csv"

# These are candidates only. The footprint and pinout still need a physical
# datasheet check before assigning a code inside EasyEDA or placing an order.
CANDIDATES = {
    "C1,C2": ("C507069", "https://www.lcsc.com/product-detail/C507069.html", "100 nF X7R, 5.08 mm pitch; verify body/drill"),
    "C5": ("C507069", "https://www.lcsc.com/product-detail/C507069.html", "100 nF X7R, 5.08 mm pitch; verify body/drill"),
    "C3,C4": ("C1579616", "https://www.lcsc.com/product-detail/C1579616.html", "Panasonic EEA-GA1V100 10 uF; verify polarity/body"),
    "D1": ("C55528", "https://www.lcsc.com/product-detail/C55528.html", "Vishay TSAL6200 IR LED; verify polarity and optical direction"),
    "U3": ("C141632", "https://www.lcsc.com/product-detail/C141632.html", "Vishay TSOP38238; verify lead order and case opening"),
    "SW1": ("C143789", "https://www.lcsc.com/product-detail/C143789.html", "Existing code; Bourns PEC11R-4015F-S0024"),
}

with SOURCE.open(encoding="utf-16", newline="") as fh:
    rows = list(csv.DictReader(fh, delimiter="\t"))

for row in rows:
    designators = row["Designator"]
    candidate = CANDIDATES.get(designators)
    if candidate:
        row["Candidate LCSC code"] = candidate[0]
        row["Candidate URL"] = candidate[1]
        row["Review note"] = candidate[2]
        row["Order status"] = "Candidate; not assigned/validated in live PCB"
    elif designators.startswith("PROX"):
        row["Candidate LCSC code"] = ""
        row["Candidate URL"] = ""
        row["Review note"] = "Imported Proxmark reference circuit; exact revision, values and RF coil design are unverified"
        row["Order status"] = "Design hold"
    elif designators in {"A1", "PI1", "IC1,IC2"}:
        row["Candidate LCSC code"] = ""
        row["Candidate URL"] = ""
        row["Review note"] = "Complete module or external board; purchase separately after revision/fit check"
        row["Order status"] = "External module"
    else:
        row["Candidate LCSC code"] = ""
        row["Candidate URL"] = ""
        row["Review note"] = "Exact part, footprint and pinout not yet matched to an LCSC listing"
        row["Order status"] = "Unassigned"

with OUTPUT.open("w", encoding="utf-8-sig", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=[*rows[0].keys()])
    writer.writeheader()
    writer.writerows(rows)

print(f"{OUTPUT}: {len(rows)} grouped rows")
from collections import Counter
print(dict(Counter(row["Order status"] for row in rows)))
