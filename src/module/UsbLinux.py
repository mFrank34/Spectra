# UsbLinux.py
# Linux USB backend using lsusb.

import subprocess
import time


def get_devices() -> set:
    """Returns a set of connected USB device identifiers."""
    devices = set()
    try:
        out = subprocess.check_output(
            "lsusb", shell=True,
            stderr=subprocess.DEVNULL,
            timeout=5
        ).decode(errors="ignore")
        for line in out.strip().split("\n"):
            if line.strip():
                devices.add(line.strip())
    except Exception:
        pass
    return devices


def get_port_count() -> int:
    """Returns the number of USB buses/controllers on the device."""
    try:
        out = subprocess.check_output(
            "lsusb -t", shell=True,
            stderr=subprocess.DEVNULL,
            timeout=5
        ).decode(errors="ignore")
        return sum(1 for line in out.split("\n") if "/:  Bus" in line)
    except Exception:
        return 0


def watch(on_connect=None, on_disconnect=None, interval: float = 1.0):
    """
    Polls for USB connect/disconnect by comparing lsusb snapshots.
    Calls on_connect(device) or on_disconnect(device) when detected.
    Runs in the calling thread — call from a background thread.
    """
    previous = get_devices()

    while True:
        time.sleep(interval)
        current = get_devices()

        for device in current - previous:
            if on_connect:
                on_connect(device)

        for device in previous - current:
            if on_disconnect:
                on_disconnect(device)

        previous = current
