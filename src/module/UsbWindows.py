# UsbWindows.py
# Windows USB backend using wmi.

try:
    import wmi
    HAS_WMI = True
except ImportError:
    HAS_WMI = False

import time


def get_devices() -> set:
    """Returns a set of connected USB device identifiers."""
    devices = set()
    if not HAS_WMI:
        return devices
    try:
        c = wmi.WMI()
        for usb in c.Win32_USBControllerDevice():
            try:
                dependent = usb.Dependent
                label = getattr(dependent, "Caption", None) or \
                        getattr(dependent, "Description", None) or \
                        getattr(dependent, "DeviceID", "Unknown")
                devices.add(label)
            except Exception:
                pass
    except Exception:
        pass
    return devices


def get_port_count() -> int:
    """Returns the number of USB controllers on the device."""
    if not HAS_WMI:
        return 0
    try:
        c = wmi.WMI()
        return len(c.Win32_USBController())
    except Exception:
        return 0


def watch(on_connect=None, on_disconnect=None, interval: float = 1.0):
    """
    Polls for USB connect/disconnect by comparing device snapshots.
    Calls on_connect(device) or on_disconnect(device) when detected.
    Runs in the calling thread — call from a background thread.
    """
    if not HAS_WMI:
        raise RuntimeError("wmi not installed. Run: pip install wmi")

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
