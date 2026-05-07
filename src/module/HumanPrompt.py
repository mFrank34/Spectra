# HumanPrompt.py
# Base class for any test step that requires human input.
# Subclass it and override build_content() to add your own UI.

import tkinter as tk
from abc import ABC, abstractmethod

from src.theme.Label import (
    PROMPT_QUESTION, PROMPT_YES, PROMPT_NO,
)
from src.theme.Theme import (
    BG, TEXT, MUTED, ACCENT2,
    FONT_TITLE, FONT_LABEL, FONT_SMALL, DANGER
)


class HumanPrompt(ABC):
    """
    Base class for human interaction prompts.
    Subclass and override build_content() to build your UI.
    Result is passed back via callback(result).

    Keyboard: Y = True (yes), N = False (no), ESC = cancel
    """

    def __init__(self, title: str, geometry: str = "400x200", callback=None):
        self.title = title
        self.callback = callback

        self.root = tk.Toplevel() if self._has_root() else tk.Tk()
        self.root.title(self.title)
        self.root.geometry(geometry)
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.build_content(self.root)

        # Keyboard bindings
        self.root.bind("y", lambda e: self.respond(True))
        self.root.bind("n", lambda e: self.respond(False))
        self.root.bind("<Escape>", lambda e: self.respond(None))

    def _has_root(self):
        try:
            return bool(tk._default_root)
        except Exception:
            return False

    @abstractmethod
    def build_content(self, parent):
        """Override this in subclasses to build your UI."""
        pass

    def respond(self, result):
        """Call this to return a result and close the window."""
        if self.callback:
            self.callback(result)
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    class TestPrompt(HumanPrompt):
        def __init__(self, callback=None):
            super().__init__(title="Test Prompt", geometry="400x200", callback=callback)

        def build_content(self, parent):
            tk.Label(parent,
                     text=PROMPT_QUESTION,
                     font=FONT_TITLE,
                     bg=BG, fg=TEXT).pack(pady=(40, 16))

            tk.Label(parent,
                     text=PROMPT_QUESTION,
                     font=FONT_SMALL,
                     bg=BG, fg=MUTED).pack()

            btn_frame = tk.Frame(parent, bg=BG)
            btn_frame.pack(pady=16)

            tk.Button(btn_frame,
                      text=PROMPT_YES, font=FONT_LABEL,
                      bg=ACCENT2, fg=BG, relief="flat",
                      padx=16, pady=8,
                      command=lambda: self.respond(True)).pack(side="left", padx=10)

            tk.Button(btn_frame,
                      text=PROMPT_NO, font=FONT_LABEL,
                      bg=DANGER, fg=TEXT, relief="flat",
                      padx=16, pady=8,
                      command=lambda: self.respond(False)).pack(side="left", padx=10)


    def on_result(result):
        print(f"Result: {result}")


    TestPrompt(callback=on_result).run()
