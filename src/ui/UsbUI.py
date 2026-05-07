# UsbController.py
# Chains UsbTest with prompts into a full USB port test flow.
# Loops through each port one at a time.

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
    def __init__(self, port_num: int, port_total: int, callback=None):
        self.port_num = port_num
        self.port_total = port_total
        super().__init__(title=USB_TITLE, geometry="420x240", callback=callback)

    def build_content(self, parent):
        tk.Label(parent,
                 text=f"Port {self.port_num} of {self.port_total}",
                 font=FONT_SMALL, bg=BG, fg=MUTED).pack(pady=(20, 0))

        tk.Label(parent, text=USB_PLUG_MSG,
                 font=FONT_TITLE, bg=BG, fg=TEXT,
                 wraplength=360).pack(pady=(8, 8))

        tk.Label(parent, text=PROMPT_HINT,
                 font=FONT_SMALL, bg=BG, fg=MUTED).pack()

        btn_frame = tk.Frame(parent, bg=BG)
        btn_frame.pack(pady=16)

        tk.Button(btn_frame, text="Start", font=FONT_LABEL,
                  bg=ACCENT, fg=BG, relief="flat", padx=16, pady=8,
                  command=lambda: self.respond(True)).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Skip", font=FONT_LABEL,
                  bg=MUTED, fg=TEXT, relief="flat", padx=16, pady=8,
                  command=lambda: self.respond(None)).pack(side="left", padx=10)

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
    Loops through each USB port one at a time:
      1. Prompt user to plug into port N
      2. Wait for device to appear (30s timeout)
      3. Prompt user to unplug it
      4. Confirm it disappears
      5. Move to next port
      6. Return all results via callback
    """

    def __init__(self, root: tk.Tk, callback=None):
        self.root = root
        self.callback = callback
        self._results = []
        self._port_total = 0
        self._current = 0
        self._test = None
        self._status_win = None
        self._device = None

    def run(self):
        self._port_total = get_port_count()
        if self._port_total == 0:
            self._finish_all()
            return
        self._current = 1
        self._next_port()

    def _next_port(self):
        if self._current > self._port_total:
            self._finish_all()
            return

        self._device = None
        UsbPlugPrompt(
            port_num=self._current,
            port_total=self._port_total,
            callback=self._on_start,
        ).run()

    def _on_start(self, confirmed):
        if confirmed is False:
            self._finish_all()
            return

        if confirmed is None:
            self._results.append({
                "port": self._current,
                "passed": None,
                "device": None,
                "note": "skipped",
            })
            self._current += 1
            self._next_port()
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
        self.root.after(0, lambda: self._status_win.update(f"{USB_DETECTED}\n{device}"))
        threading.Timer(2.0, self._prompt_unplug).start()

    def _prompt_unplug(self):
        self.root.after(0, lambda: self._status_win.update(USB_UNPLUG_MSG))

    def _on_disconnected(self, device):
        self.root.after(0, self._after_disconnect)

    def _after_disconnect(self):
        if self._status_win:
            self._status_win.close()
        self._record(True)

    def _on_timeout(self):
        self.root.after(0, self._after_timeout)

    def _after_timeout(self):
        if self._status_win:
            self._status_win.close()
        self._record(False)

    def _record(self, passed: bool):
        self._results.append({
            "port": self._current,
            "passed": passed,
            "device": self._device,
        })
        self._current += 1
        self._next_port()

    def _finish_all(self):
        if self.callback:
            self.callback({
                "test": "usb",
                "port_count": self._port_total,
                "results": self._results,
                "passed": all(r["passed"] for r in self._results if r["passed"] is not None),
            })


if __name__ == "__main__":
    def on_result(result):
        print(f"USB Test Result: {result}")


    root = tk.Tk()
    root.withdraw()
    UsbController(root=root, callback=on_result).run()
    root.mainloop()
