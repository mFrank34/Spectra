# ScreenTestController.py

import tkinter as tk

from src.devices.Screen import Screen
from src.module.HumanPrompt import HumanPrompt
from src.theme.Label import PROMPT_QUESTION, PROMPT_HINT, PROMPT_YES, PROMPT_NO
from src.theme.Theme import BG, TEXT, MUTED, ACCENT2, DANGER, FONT_TITLE, FONT_LABEL, FONT_SMALL


class ScreenResultPrompt(HumanPrompt):
    def __init__(self, callback=None):
        super().__init__(title="Screen Test Result", geometry="400x200", callback=callback)

    def build_content(self, parent):
        tk.Label(parent, text=PROMPT_QUESTION, font=FONT_TITLE,
                 bg=BG, fg=TEXT).pack(pady=(40, 16))
        tk.Label(parent, text=PROMPT_HINT, font=FONT_SMALL,
                 bg=BG, fg=MUTED).pack()

        btn_frame = tk.Frame(parent, bg=BG)
        btn_frame.pack(pady=16)

        tk.Button(btn_frame, text=PROMPT_YES, font=FONT_LABEL,
                  bg=ACCENT2, fg=BG, relief="flat", padx=16, pady=8,
                  command=lambda: self.respond(True)).pack(side="left", padx=10)

        tk.Button(btn_frame, text=PROMPT_NO, font=FONT_LABEL,
                  bg=DANGER, fg=TEXT, relief="flat", padx=16, pady=8,
                  command=lambda: self.respond(False)).pack(side="left", padx=10)


class ScreenController:
    """
    Runs ScreenTest then launches ScreenResultPrompt.
    Result passed back via callback(result).
    """

    def __init__(self, callback=None):
        self.callback = callback

    def run(self):
        test = Screen(on_complete=self._on_test_done)
        test.run()

    def _on_test_done(self):
        ScreenResultPrompt(callback=self.callback).run()


if __name__ == "__main__":
    def on_result(result):
        print(result)


    ScreenController(callback=on_result).run()
