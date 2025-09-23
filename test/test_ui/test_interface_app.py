import logging
from test.constants import PATH_TXT, TEXT_TXT
from unittest.mock import MagicMock, patch

import pytest

from src.ui import InterfaceApp

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def test_initial_config_tk_app(interface_app: InterfaceApp) -> None:
    root = interface_app._root
    root.update()

    title = root.title()
    geometry = root.geometry().split("+")[0]
    resizable = root.resizable()

    assert title == "Notepad APP"
    assert geometry == "800x780"
    assert resizable == (False, False)


def test_get_txt_from_file(interface_app: InterfaceApp) -> None:
    path = PATH_TXT

    interface_app._create_widgets()

    with patch("tkinter.filedialog.askopenfilename") as askopenfilename:
        askopenfilename.return_value = path

        interface_app._get_txt_from_file()

        text_entry = interface_app._text_entry.get(1.0, "end-1c")

        assert text_entry == TEXT_TXT
        askopenfilename.assert_called_once_with(
            initialdir="/",
            title="Select a File",
            filetypes=(("Text files", "*.txt*"), ("All files", "*.*")),
        )


def test_save_file(interface_app: InterfaceApp) -> None:
    interface_app._create_widgets()
    interface_app._text_entry.insert(1.0, TEXT_TXT)

    with patch("tkinter.filedialog.asksaveasfile") as asksaveasfile:
        mock_file = MagicMock()
        asksaveasfile.return_value = mock_file

        interface_app._save_file()

        asksaveasfile.assert_called_once_with(
            mode="w",
            filetypes=[("Text Document", "*.txt")],
            defaultextension=[("Text Document", "*.txt")],
        )

        text_entry = interface_app._text_entry.get(1.0, "end")

        mock_file.write.assert_called_once_with(text_entry)

        mock_file.close.assert_called_once()


def test_delete_txt(interface_app: InterfaceApp) -> None:
    interface_app._create_widgets()
    interface_app._text_entry.insert(1.0, TEXT_TXT)

    text_entry = interface_app._text_entry.get(1.0, "end-1c")

    assert text_entry == TEXT_TXT

    interface_app._delete_txt()

    text_entry = interface_app._text_entry.get(1.0, "end-1c")

    assert text_entry == ""


def test_open_win_config_font(interface_app: InterfaceApp) -> None:
    interface_app._open_win_config_font()
    win_font = interface_app._win_config_font

    assert win_font
    assert win_font.title() == "Change font"
    assert win_font.geometry().split("+")[0] == "400x200"
    assert win_font.resizable() == (False, False)

    assert interface_app._entry_number
    assert interface_app._combo_fonts


def test_save_config_font_invalid_fields(interface_app: InterfaceApp) -> None:
    interface_app._open_win_config_font()

    new_size = ""
    new_font = ""

    interface_app._entry_number.set(new_size)
    interface_app._combo_fonts.set(new_font)

    with pytest.raises(ValueError) as exc_info:
        interface_app._save_config_font()

    assert str(exc_info.value) == "You must enter valid fields."


def test_save_config_font_invalid_int(interface_app: InterfaceApp) -> None:
    interface_app._open_win_config_font()

    new_size = "asdas"
    new_font = "Terminal"

    interface_app._entry_number.set(new_size)
    interface_app._combo_fonts.set(new_font)

    with pytest.raises(ValueError) as exc_info:
        interface_app._save_config_font()

    assert str(exc_info.value) == "You must enter a valid number in the font size."


def test_save_config_font(interface_app: InterfaceApp) -> None:
    interface_app._open_win_config_font()

    new_size = "10"
    new_font = "Terminal"

    interface_app._entry_number.set(new_size)
    interface_app._combo_fonts.set(new_font)

    interface_app._save_config_font()

    assert interface_app._text_entry["font"] == f"{new_font} {new_size}"
