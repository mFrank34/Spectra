# Screen.py
# Screen Test - Dead Pixel & Backlight Bleed
# Press SPACE or click to cycle screens, ESC to exit

import tkinter as tk

from src.theme.Label import (
    SCR_RED, SCR_GREEN, SCR_BLUE,
    SCR_WHITE, SCR_BLACK, SCR_BLEED,
    SCR_HINT,
)

SCREENS = [
    (SCR_RED, "#ff0000"),
    (SCR_GREEN, "#00ff00"),
    (SCR_BLUE, "#0000ff"),
    (SCR_WHITE, "#ffffff"),
    (SCR_BLACK, "#000000"),
    (SCR_BLEED, "#000000"),
]

HINT_COLOR = {
    "#ff0000": "#ffffff",
    "#00ff00": "#000000",
    "#0000ff": "#ffffff",
    "#ffffff": "#000000",
    "#000000": "#444444",
}


class Screen:
    def __init__(self, on_complete=None):
        self._index = 0
        self.on_complete = on_complete

        self.root = tk.Toplevel() if self._has_root() else tk.Tk()
        self.root.title("Screen Test")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg=SCREENS[0][1])

        self.canvas = tk.Canvas(self.root, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)

        self.hint = self.canvas.create_text(
            0, 0, text="", font=("Courier New", 11), anchor="sw",
        )

        self.root.bind("<space>", self._next)
        self.root.bind("<Button-1>", self._next)
        self.root.bind("<Escape>", self._exit)

        self._draw(0)
        self.root.after(100, self._set_hint_position)

    def _has_root(self):
        try:
            return bool(tk._default_root)
        except Exception:
            return False

    def _draw(self, index):
        name, color = SCREENS[index]
        hint_fg = HINT_COLOR.get(color, "#888888")

        self.root.configure(bg=color)
        self.canvas.configure(bg=color)

        hint_text = f"  {name}   [{index + 1}/{len(SCREENS)}]   {SCR_HINT}  "
        self.canvas.itemconfig(self.hint, text=hint_text, fill=hint_fg)

    def _set_hint_position(self):
        h = self.root.winfo_height()
        self.canvas.coords(self.hint, 16, h - 16)

    def _next(self, event=None):
        self._index += 1
        if self._index >= len(SCREENS):
            self._exit()
            return
        self._draw(self._index)

    def _exit(self, event=None):
        self.root.destroy()
        if self.on_complete:
            self.on_complete()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Screen().run()
