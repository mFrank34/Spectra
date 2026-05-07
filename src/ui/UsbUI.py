# UsbController.py
# Chains UsbTest with prompts into a full USB port test flow.

import threading
import tkinter as tk

from src.devices.Usb import Usb
from src.module.HumanPrompt import HumanPrompt
from src.module.UsbPlatform import get_port_count
from src.theme.Label import (
    USB_TITLE, USB_PLUG_MSG, USB_UNPLUG_MSG,
    USB_DETECTED, PROMPT_HINT,
)
from src.theme.Theme import (
    BG, TEXT, MUTED, ACCENT, DANGER,
    FONT_TITLE, FONT_LABEL, FONT_SMALL,
)


class UsbPlugPrompt(HumanPrompt):
    def __init__(self, callback=None):
        super().__init__(title=USB_TITLE, geometry="420x240", callback=callback)

    def build_content(self, parent):
        port_count = get_port_count()
        port_label = f"USB ports detected on this device: {port_count}"

        tk.Label(parent, text=USB_PLUG_MSG,
                 font=FONT_TITLE, bg=BG, fg=TEXT,
                 wraplength=360).pack(pady=(30, 8))

        tk.Label(parent, text=port_label,
                 font=FONT_SMALL, bg=BG, fg=ACCENT).pack(pady=(0, 8))

        tk.Label(parent, text=PROMPT_HINT,
                 font=FONT_SMALL, bg=BG, fg=MUTED).pack()

        btn_frame = tk.Frame(parent, bg=BG)
        btn_frame.pack(pady=16)

        tk.Button(btn_frame, text="Start", font=FONT_LABEL,
                  bg=ACCENT, fg=BG, relief="flat", padx=16, pady=8,
                  command=lambda: self.respond(True)).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Cancel", font=FONT_LABEL,
                  bg=DANGER, fg=TEXT, relief="flat", padx=16, pady=8,
                  command=lambda: self.respond(False)).pack(side="left", padx=10)


class UsbStatusWindow:
    def __init__(self, message: str):
        self.root = tk.Toplevel()
        self.root.title(USB_TITLE)
        self.root.geometry("420x160")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self._var = tk.StringVar(value=message)
        tk.Label(self.root, textvariable=self._var,
                 font=FONT_TITLE, bg=BG, fg=TEXT,
                 wraplength=380).pack(pady=(40, 8))
        tk.Label(self.root, text="Please wait…",
                 font=FONT_SMALL, bg=BG, fg=MUTED).pack()

    def update(self, message: str):
        self._var.set(message)

    def close(self):
        self.root.destroy()


class UsbController:
    """
    Full USB port test flow:
      1. Show port count and prompt user to plug in a USB device
      2. Wait for device to appear (30s timeout)
      3. Prompt user to unplug it
      4. Confirm it disappears
      5. Return result via callback
    """

    def __init__(self, callback=None):
        self.callback = callback
        self._test = None
        self._status_win = None
        self._device = None

    def run(self):
        UsbPlugPrompt(callback=self._on_start).run()

    def _on_start(self, confirmed):
        if not confirmed:
            self._finish(None)
            return

        self._status_win = UsbStatusWindow(USB_PLUG_MSG)

        self._test = Usb(
            on_connected=self._on_connected,
            on_disconnected=self._on_disconnected,
            on_timeout=self._on_timeout,
            timeout=30,
        )
        self._test.start()

    def _on_connected(self, device):
        self._device = device
        if self._status_win:
            self._status_win.update(f"{USB_DETECTED}\n{device}")
        threading.Timer(2.0, self._prompt_unplug).start()

    def _prompt_unplug(self):
        if self._status_win:
            self._status_win.update(USB_UNPLUG_MSG)

    def _on_disconnected(self, device):
        if self._status_win:
            self._status_win.close()
        self._finish(True)

    def _on_timeout(self):
        if self._status_win:
            self._status_win.close()
        self._finish(False)

    def _finish(self, passed):
        if self.callback:
            self.callback({
                "test": "usb",
                "passed": passed,
                "device": self._device,
                "port_count": get_port_count(),
            })


if __name__ == "__main__":
    def on_result(result):
        print(f"USB Test Result: {result}")


    root = tk.Tk()
    root.withdraw()
    UsbController(callback=on_result).run()
    root.mainloop()
