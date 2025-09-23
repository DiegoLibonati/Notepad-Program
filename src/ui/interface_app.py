# src/ui/interface_app.py
from tkinter import (
    Button,
    Entry,
    Label,
    Menu,
    Scrollbar,
    StringVar,
    Text,
    Tk,
    Toplevel,
    font,
)
from tkinter.ttk import Combobox

from src.services.file_service import open_file, save_file
from src.utils.constants import (
    ANCHOR_CENTER,
    FILL_BOTH,
    FILL_X,
    FILL_Y,
    FONT_ARIAL_10,
    FONT_ROBOTO_10,
    ORIENT_HORIZONTAL,
    POSITION_END,
    SIDE_BOTTOM,
    SIDE_RIGHT,
    WRAP_NONE,
)
from src.utils.paths import APP_ICON


class InterfaceApp:
    def __init__(self, root: Tk) -> None:
        self._root = root
        self._root.title("Notepad APP")
        self._root.geometry("800x800")
        self._root.resizable(False, False)
        self._root.iconbitmap(APP_ICON)

        self._create_widgets()
        self._create_menu()

    def _create_widgets(self) -> None:
        self._scrollbar_vertical = Scrollbar(master=self._root)
        self._scrollbar_vertical.pack(side=SIDE_RIGHT, fill=FILL_Y)

        self._scrollbar_horizontal = Scrollbar(
            master=self._root, orient=ORIENT_HORIZONTAL
        )
        self._scrollbar_horizontal.pack(side=SIDE_BOTTOM, fill=FILL_X)

        self._text_entry = Text(
            master=self._root,
            font=FONT_ARIAL_10,
            wrap=WRAP_NONE,
            padx=5,
            pady=5,
            yscrollcommand=self._scrollbar_vertical.set,
            xscrollcommand=self._scrollbar_horizontal.set,
        )
        self._text_entry.pack(expand=True, fill=FILL_BOTH)

        self._scrollbar_vertical.config(command=self._text_entry.yview)
        self._scrollbar_horizontal.config(command=self._text_entry.xview)

    def _create_menu(self) -> None:
        menu_bar = Menu(master=self._root)
        self._root.config(menu=menu_bar)

        file_drop_down = Menu(master=menu_bar, tearoff=0)
        config_drop_down = Menu(master=menu_bar, tearoff=0)

        menu_bar.add_cascade(label="File", menu=file_drop_down)
        menu_bar.add_cascade(label="Configuration", menu=config_drop_down)

        file_drop_down.add_command(label="Open", command=self._get_txt_from_file)
        file_drop_down.add_command(label="Save", command=self._save_file)
        file_drop_down.add_command(label="Delete all text", command=self._delete_txt)
        file_drop_down.add_separator()
        file_drop_down.add_command(label="Exit", command=lambda: exit())

        config_drop_down.add_command(
            label="Change font", command=self._open_win_config_font
        )

    def _get_txt_from_file(self) -> None:
        file_content = open_file()
        if file_content:
            self._text_entry.delete(1.0, POSITION_END)
            self._text_entry.insert(POSITION_END, file_content)

    def _save_file(self) -> None:
        text_content = self._text_entry.get(1.0, POSITION_END)
        save_file(text_content)

    def _delete_txt(self) -> None:
        self._text_entry.delete(1.0, POSITION_END)

    def _open_win_config_font(self) -> None:
        self._win_config_font = Toplevel(master=self._root)
        self._win_config_font.iconbitmap(APP_ICON)
        self._win_config_font.title("Change font")
        self._win_config_font.geometry("400x200")
        self._win_config_font.resizable(False, False)

        self._entry_number = StringVar()

        Label(
            master=self._win_config_font,
            text="Change the font type: ",
            font=FONT_ROBOTO_10,
        ).place(x=5, y=10)

        self._combo_fonts = Combobox(
            master=self._win_config_font, values=font.families(), font=FONT_ROBOTO_10
        )
        self._combo_fonts.place(x=170, y=10)

        Label(
            master=self._win_config_font,
            text="Change the font size: ",
            font=FONT_ROBOTO_10,
        ).place(x=5, y=40)

        Entry(
            master=self._win_config_font,
            font=FONT_ROBOTO_10,
            width=5,
            textvariable=self._entry_number,
        ).place(x=200, y=40)

        Button(
            master=self._win_config_font,
            text="Save",
            command=self._save_config_font,
        ).place(x=200, y=180, anchor=ANCHOR_CENTER)

    def _save_config_font(self) -> None:
        new_font = self._combo_fonts.get()
        new_size = self._entry_number.get()

        if not new_font or not new_size:
            self._win_config_font.destroy()
            raise ValueError("You must enter valid fields.")

        try:
            new_size = int(new_size)
        except Exception:
            raise ValueError("You must enter a valid number in the font size.")

        self._text_entry["font"] = (f"{new_font}", f"{new_size}")
        self._win_config_font.destroy()
