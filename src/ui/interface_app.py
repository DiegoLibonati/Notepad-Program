from tkinter import Tk

from src.configs.default_config import DefaultConfig
from src.constants.messages import MESSAGE_NOT_VALID_FIELD_NUM, MESSAGE_NOT_VALID_FIELDS
from src.constants.paths import PATH_ICON
from src.services.file_service import FileService
from src.ui.styles import Styles
from src.ui.views.font_config_view import FontConfigView
from src.ui.views.main_view import MainView
from src.utils.dialogs import ValidationDialogError


class InterfaceApp:
    def __init__(self, root: Tk, config: DefaultConfig, styles: Styles = Styles()) -> None:
        self._styles = styles
        self._config = config
        self._root = root
        self._root.title("Notepad APP")
        self._root.geometry("800x800")
        self._root.resizable(False, False)
        self._root.iconbitmap(PATH_ICON)

        self._main_view = MainView(
            root=self._root,
            styles=self._styles,
            on_open=self._get_txt_from_file,
            on_save=self._save_file,
            on_delete=self._delete_txt,
            on_change_font=self._open_win_config_font,
        )
        self._main_view.grid(row=0, column=0, sticky="nsew")
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

    def _get_txt_from_file(self) -> None:
        file_content = FileService.open_file()
        if file_content:
            self._main_view.set_text(file_content)

    def _save_file(self) -> None:
        text_content = self._main_view.get_text()
        FileService.save_file(text_content)

    def _delete_txt(self) -> None:
        self._main_view.clear_text()

    def _open_win_config_font(self) -> None:
        FontConfigView(
            root=self._root,
            styles=self._styles,
            on_save=self._save_config_font,
        )

    def _save_config_font(self, new_font: str, new_size: str) -> None:
        if not new_font or not new_size:
            ValidationDialogError(message=MESSAGE_NOT_VALID_FIELDS).dialog()
            return

        try:
            new_size = int(new_size)
        except Exception:
            ValidationDialogError(message=MESSAGE_NOT_VALID_FIELD_NUM).dialog()
            return

        self._main_view.set_font(new_font, new_size)
