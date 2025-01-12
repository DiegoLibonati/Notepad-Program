# coding: utf8
from tkinter import Tk
from tkinter import Menu
from tkinter import Text
from tkinter import Scrollbar
from tkinter import Button
from tkinter import Label
from tkinter import Entry
from tkinter import StringVar
from tkinter import filedialog
from tkinter import Toplevel
from tkinter import font
from tkinter.ttk import Combobox

from src.utils.paths import APP_ICON
from src.utils.constants import FONT_ARIAL_10
from src.utils.constants import FONT_ROBOTO_10
from src.utils.constants import WRAP_NONE
from src.utils.constants import FILL_BOTH
from src.utils.constants import SIDE_RIGHT
from src.utils.constants import SIDE_BOTTOM
from src.utils.constants import FILL_X
from src.utils.constants import FILL_Y
from src.utils.constants import ORIENT_HORIZONTAL
from src.utils.constants import POSITION_END
from src.utils.constants import ANCHOR_CENTER


class InterfaceApp:
    def __init__(self, root: Tk) -> None:
        # APP Config
        self._root = root
        self._root.title("Notepad APP")
        self._root.geometry("800x800")
        self._root.resizable(False, False)
        self._root.iconbitmap(APP_ICON)

        # Create widges
        self._create_widgets()
        self._create_menu()

    def _create_widgets(self) -> None:
        # Scroll bar
        self._scrollbar_vertical = Scrollbar(master=self._root)
        self._scrollbar_vertical.pack(side=SIDE_RIGHT, fill=FILL_Y)
        self._scrollbar_horizontal = Scrollbar(master=self._root, orient=ORIENT_HORIZONTAL)
        self._scrollbar_horizontal.pack(side=SIDE_BOTTOM, fill=FILL_X)

        # Entry Text
        self._text_entry = Text(master=self._root, font=FONT_ARIAL_10, wrap=WRAP_NONE, padx=5, pady=5, yscrollcommand=self._scrollbar_vertical.set, xscrollcommand=self._scrollbar_horizontal.set)
        self._text_entry.pack(expand=True, fill=FILL_BOTH)

        # Scroll bar final config
        self._scrollbar_vertical.config(command=self._text_entry.yview)
        self._scrollbar_horizontal.config(command=self._text_entry.xview)

    def _create_menu(self) -> None:
        menu_bar = Menu(master=self._root)

        self._root.config(menu=menu_bar)

        file_drop_down = Menu(master=menu_bar, tearoff=0)
        config_drop_down = Menu(master=menu_bar, tearoff=0)

        menu_bar.add_cascade(label="File", menu=file_drop_down)
        menu_bar.add_cascade(label="Configuration", menu=config_drop_down)

        file_drop_down.add_command(label="Open", command=lambda:self._get_txt_from_file())
        file_drop_down.add_command(label="Save", command=lambda:self._save_file())
        file_drop_down.add_command(label="Delete all text", command=lambda:self._delete_txt())
        file_drop_down.add_separator()
        file_drop_down.add_command(label="Exit", command=lambda:exit())

        config_drop_down.add_command(label="Change font", command=lambda:self._open_win_config_font()) 

    @staticmethod
    def browser_file() -> str:
        filename = filedialog.askopenfilename(
            initialdir = "/",
            title = "Select a File",
            filetypes = (
                ("Text files", "*.txt*"),
                ("All files", "*.*")
            )
        )
        
        return filename
    
    def _get_txt_from_file(self) -> None:
        file_path = self.browser_file()

        file = open(file_path, "r")
        file_content = file.read()

        self._text_entry.delete(1.0, POSITION_END)
        self._text_entry.insert(POSITION_END, str(file_content))

        file.close()

    def _save_file(self) -> None:
        files = [
            ('Text Document', '*.txt')
        ]

        file = filedialog.asksaveasfile(
            mode="w",
            filetypes = files, 
            defaultextension = files
        )

        file.write(str(self._text_entry.get(1.0, POSITION_END)))

        file.close()

    def _delete_txt(self) -> None:
        self._text_entry.delete(1.0, POSITION_END)

    def _open_win_config_font(self) -> None:
        self._win_config_font = Toplevel(master=self._root)
        self._win_config_font.iconbitmap(APP_ICON)
        self._win_config_font.title("Change font")
        self._win_config_font.geometry("400x200")
        self._win_config_font.resizable(False, False)
        
        self._entry_number = StringVar()

        Label(master=self._win_config_font, text="Change the font type: ", font=FONT_ROBOTO_10).place(x=5, y=10)

        self._combo_fonts = Combobox(master=self._win_config_font, values=font.families(), font=FONT_ROBOTO_10)
        self._combo_fonts.place(x=170, y=10)

        Label(master=self._win_config_font, text="Change the font size: ", font=FONT_ROBOTO_10).place(x=5, y=40)
        Entry(master=self._win_config_font, font=FONT_ROBOTO_10, width=5, textvariable=self._entry_number).place(x=200, y=40)

        Button(master=self._win_config_font, text="Save", command=lambda:self._save_config_font()).place(x=200, y=180, anchor=ANCHOR_CENTER)

    def _save_config_font(self) -> None:
        new_font = self._combo_fonts.get()
        new_size = self._entry_number.get()

        if not new_font or not new_size:
            self._win_config_font.destroy()
            raise ValueError("You must enter valid fields.")
        
        try:
            new_size = int(new_size)
        except:
            raise ValueError("You must enter a valid number in the font size.")

        self._text_entry["font"] = (f"{new_font}", f"{new_size}")

        self._win_config_font.destroy()
      