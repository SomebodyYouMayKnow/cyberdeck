"""Patch only the NPTH Excellon member in an EasyEDA-generated Gerber ZIP."""
import sys
import zipfile
from pathlib import Path

source = Path(sys.argv[1])
target = Path(sys.argv[2])
rows = sys.argv[3:]
with zipfile.ZipFile(source, "r") as src:
    entries = {info.filename: src.read(info.filename) for info in src.infolist()}
name = "Drill_NPTH_Through.DRL"
text = entries[name].decode("ascii")
if text.count("T01\n") != 1 or "\nT02\n" not in text:
    raise SystemExit("Unexpected EasyEDA NPTH Excellon structure")
before, after = text.split("\nT02\n", 1)
before = before.replace(
    ";EasyEDA v6.5.51, 2026-10-19 10:07:01",
    ";Derived from EasyEDA v6.5.51 export 2026-10-19; 8 support NPTHs added 2026-10-19",
)
entries[name] = (before + "\n" + "\n".join(rows) + "\nT02\n" + after).encode("ascii")
with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as dst:
    for filename, data in entries.items():
        dst.writestr(filename, data)
with zipfile.ZipFile(target, "r") as check:
    verify = check.read(name).decode("ascii")
    if not all(row in verify for row in rows):
        raise SystemExit("Updated NPTH rows did not verify")
    if len(check.namelist()) != len(entries):
        raise SystemExit("Gerber archive member count changed unexpectedly")
print(f"Updated {name} with {len(rows)} new NPTH locations; kept {len(entries) - 1} other Gerber members unchanged.")
