from tkinter import Frame, Menu, Scrollbar, Text, Tk

from src.ui.styles import Styles


class MainView(Frame):
    def __init__(
        self,
        root: Tk,
        styles: Styles,
        on_open: callable,
        on_save: callable,
        on_delete: callable,
        on_change_font: callable,
    ) -> None:
        super().__init__(root)
        self._styles = styles
        self._on_open = on_open
        self._on_save = on_save
        self._on_delete = on_delete
        self._on_change_font = on_change_font

        self._create_widgets()
        self._create_menu()

    def _create_widgets(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._scrollbar_vertical = Scrollbar(master=self)
        self._scrollbar_vertical.grid(row=0, column=1, sticky="ns")

        self._scrollbar_horizontal = Scrollbar(master=self, orient=self._styles.ORIENT_HORIZONTAL)
        self._scrollbar_horizontal.grid(row=1, column=0, sticky="ew")

        self._text_entry = Text(
            master=self,
            font=self._styles.FONT_ARIAL_10,
            wrap=self._styles.WRAP_NONE,
            padx=5,
            pady=5,
            yscrollcommand=self._scrollbar_vertical.set,
            xscrollcommand=self._scrollbar_horizontal.set,
        )
        self._text_entry.grid(row=0, column=0, sticky="nsew")

        self._scrollbar_vertical.config(command=self._text_entry.yview)
        self._scrollbar_horizontal.config(command=self._text_entry.xview)

    def _create_menu(self) -> None:
        menu_bar = Menu(master=self.master)
        self.master.config(menu=menu_bar)

        file_drop_down = Menu(master=menu_bar, tearoff=0)
        config_drop_down = Menu(master=menu_bar, tearoff=0)

        menu_bar.add_cascade(label="File", menu=file_drop_down)
        menu_bar.add_cascade(label="Configuration", menu=config_drop_down)

        file_drop_down.add_command(label="Open", command=self._on_open)
        file_drop_down.add_command(label="Save", command=self._on_save)
        file_drop_down.add_command(label="Delete all text", command=self._on_delete)
        file_drop_down.add_separator()
        file_drop_down.add_command(label="Exit", command=lambda: exit())

        config_drop_down.add_command(label="Change font", command=self._on_change_font)

    def get_text(self) -> str:
        return self._text_entry.get(1.0, self._styles.POSITION_END)

    def set_text(self, content: str) -> None:
        self._text_entry.delete(1.0, self._styles.POSITION_END)
        self._text_entry.insert(self._styles.POSITION_END, content)

    def clear_text(self) -> None:
        self._text_entry.delete(1.0, self._styles.POSITION_END)

    def set_font(self, new_font: str, new_size: int) -> None:
        self._text_entry["font"] = (f"{new_font}", f"{new_size}")
