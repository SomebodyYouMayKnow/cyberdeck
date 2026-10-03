#!/usr/bin/env python3
"""Discover a Chameleon Ultra SE3 over Bluetooth Low Energy.

This does not write to the device. The Chameleon command UUIDs and command
format must be verified from the exact SE3 firmware before control features are
added. Discovery is a safe first hardware test.
"""

import argparse
import asyncio

from bleak import BleakScanner


async def discover(timeout: float) -> int:
    devices = await BleakScanner.discover(timeout=timeout, return_adv=True)
    found = 0
    for address, (device, advertisement) in devices.items():
        name = device.name or advertisement.local_name or ""
        if "chameleon" in name.lower():
            found += 1
            print(f"Found: name={name!r} address={address} rssi={advertisement.rssi}")
    if found == 0:
        print("No Chameleon-named BLE advertisement found. Confirm it is powered and advertising.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Find a Chameleon Ultra SE3 BLE advertisement")
    parser.add_argument("--seconds", type=float, default=8.0)
    return asyncio.run(discover(parser.parse_args().seconds))


if __name__ == "__main__":
    raise SystemExit(main())
