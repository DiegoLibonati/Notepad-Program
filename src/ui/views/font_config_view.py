from tkinter import Button, StringVar, Tk, Toplevel, font

from src.constants.paths import PATH_ICON
from src.ui.components.font_config_form import FontConfigForm
from src.ui.styles import Styles


class FontConfigView(Toplevel):
    def __init__(self, root: Tk, styles: Styles, on_save: callable) -> None:
        super().__init__(root)
        self._styles = styles
        self._on_save = on_save

        self.iconbitmap(PATH_ICON)
        self.title("Change font")
        self.geometry("400x200")
        self.resizable(False, False)

        self._entry_number = StringVar()

        self._create_widgets()

    def _create_widgets(self) -> None:
        self.columnconfigure(0, weight=1)

        self._font_config_form = FontConfigForm(
            parent=self,
            styles=self._styles,
            font_families=list(font.families()),
            entry_number=self._entry_number,
        )
        self._font_config_form.grid(row=0, column=0, sticky="ew", padx=5, pady=10)

        Button(
            self,
            text="Save",
            command=self._handle_save,
        ).grid(row=1, column=0, pady=(10, 0))

    def _handle_save(self) -> None:
        new_font = self._font_config_form.get_font()
        new_size = self._entry_number.get()
        self._on_save(new_font, new_size)
        self.destroy()
