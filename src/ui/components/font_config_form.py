from tkinter import Entry, Frame, Label, Misc, StringVar
from tkinter.ttk import Combobox
from typing import Any

from src.ui.styles import Styles


class FontConfigForm(Frame):
    def __init__(
        self,
        parent: Misc,
        styles: Styles,
        font_families: list[tuple[str, Any]],
        entry_number: StringVar,
    ) -> None:
        super().__init__(parent)
        self._styles = styles
        self._font_families = font_families
        self._entry_number = entry_number

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        Label(
            self,
            text="Change the font type: ",
            font=self._styles.FONT_ROBOTO_10,
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        self._combo_fonts = Combobox(
            self,
            values=self._font_families,
            font=self._styles.FONT_ROBOTO_10,
        )
        self._combo_fonts.grid(row=0, column=1, sticky="ew", pady=(0, 10))

        Label(
            self,
            text="Change the font size: ",
            font=self._styles.FONT_ROBOTO_10,
        ).grid(row=1, column=0, sticky="w")

        Entry(
            self,
            font=self._styles.FONT_ROBOTO_10,
            width=5,
            textvariable=self._entry_number,
        ).grid(row=1, column=1, sticky="w")

    def get_font(self) -> str:
        return self._combo_fonts.get()
