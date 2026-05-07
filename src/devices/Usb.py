# UsbTest.py
# Tests a USB port by detecting plug and unplug events.

import threading
import time

from src.module.UsbPlatform import get_devices


class Usb:
    """
    Tests a USB port by:
    1. Taking a baseline snapshot of connected devices
    2. Watching for a new device to appear (connect test)
    3. Watching for it to disappear (disconnect test)

    Callbacks:
        on_connected(device)    — new device detected
        on_disconnected(device) — device removed
        on_timeout()            — no device detected in time
    """

    def __init__(self,
                 on_connected=None,
                 on_disconnected=None,
                 on_timeout=None,
                 timeout: int = 30):

        self.on_connected = on_connected
        self.on_disconnected = on_disconnected
        self.on_timeout = on_timeout
        self.timeout = timeout

        self._baseline = set()
        self._found = None
        self._running = False
        self._thread = None

    def start(self):
        """Take baseline snapshot and start watching for new devices."""
        self._baseline = get_devices()
        self._running = True
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def _watch_loop(self):
        start = time.time()

        while self._running:
            if time.time() - start > self.timeout:
                self._running = False
                if self.on_timeout:
                    self.on_timeout()
                return

            current = get_devices()

            # New device plugged in
            new = current - self._baseline
            if new and self._found is None:
                self._found = next(iter(new))
                if self.on_connected:
                    self.on_connected(self._found)

            # Device unplugged
            if self._found and self._found not in current:
                self._running = False
                if self.on_disconnected:
                    self.on_disconnected(self._found)
                return

            time.sleep(1.0)
