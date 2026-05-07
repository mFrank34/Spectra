import tkinter as tk

from src.theme.Theme import *
from src.theme.Label import *

class Spectra(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spectra")
        self.geometry("800x600")
        self.minsize(800, 600)
        self.configure(bg=BG)
        self.resizable(width=False, height=False)

        self._build_header()

    def _build_header(self):
        hdr = tk.Frame(self, bg=BG_PANEL, height=52)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        logo = tk.Frame(hdr, bg=BG_PANEL, highlightthickness=0)
        logo.pack(side="left", padx=20)

        tk.Label(logo, text=APP_TITLE, font=FONT_TITLE,
                 bg=BG_PANEL, fg=ACCENT).pack(side="left")

        tk.Label(logo, text=APP_SUBTITLE, font=FONT_SMALL,
                 bg=BG_PANEL, fg=MUTED).pack(side="left", pady=(6, 0))

        # Right: version tag
        tk.Label(hdr, text=APP_VERSION, font=FONT_SMALL,
                 bg=BG_PANEL, fg=MUTED).pack(side="right", padx=20)

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

    def _build_body(self):
        body = tk.Frame(self, bg=BG_PANEL, highlightthickness=0)
        body.pack(fill="both", expand=True)

        self._build_sidebar(body)
        tk.Frame(body, bg=BORDER, width=1).pack(side="left", fill="y")
        self._build_content(body)

    def _build_sidebar(self, body):
        pass

    def _build_content(self, body):
        pass
