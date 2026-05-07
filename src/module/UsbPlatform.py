# Usb.py
# USB abstraction layer — picks the right backend based on OS.
# Import this everywhere, never import the backends directly.

import platform

_OS = platform.system()

if _OS == "Windows":
    from src.module.UsbWindows import get_devices, watch, get_port_count
elif _OS == "Linux":
    from src.module.UsbLinux import get_devices, watch, get_port_count
else:
    def get_devices() -> set:
        return set()


    def get_port_count() -> int:
        return 0


    def watch(on_connect=None, on_disconnect=None, **kwargs):
        raise RuntimeError(f"USB not supported on {_OS}")
