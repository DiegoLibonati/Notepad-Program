from unittest.mock import MagicMock, patch

import pytest

from src.constants.messages import MESSAGE_NOT_VALID_FIELD_NUM, MESSAGE_NOT_VALID_FIELDS
from src.ui.interface_app import InterfaceApp
from src.ui.styles import Styles
from src.utils.dialogs import ValidationDialogError


@pytest.fixture
def interface_app(mock_root: MagicMock, mock_styles: MagicMock) -> InterfaceApp:
    with patch("src.ui.interface_app.MainView") as mock_main_view_class:
        mock_main_view_class.return_value = MagicMock()
        instance: InterfaceApp = InterfaceApp.__new__(InterfaceApp)
        instance._styles = mock_styles
        instance._config = MagicMock()
        instance._root = mock_root
        instance._main_view = mock_main_view_class.return_value
        return instance


class TestInterfaceAppInit:
    def test_stores_styles(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with patch("src.ui.interface_app.MainView") as mock_main_view_class:
            mock_main_view_class.return_value.grid = MagicMock()
            with patch("src.ui.interface_app.PATH_ICON", "icon.ico"):
                app: InterfaceApp = InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        assert app._styles is mock_styles

    def test_stores_root(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with patch("src.ui.interface_app.MainView") as mock_main_view_class:
            mock_main_view_class.return_value.grid = MagicMock()
            with patch("src.ui.interface_app.PATH_ICON", "icon.ico"):
                app: InterfaceApp = InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        assert app._root is mock_root

    def test_title_is_set(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with patch("src.ui.interface_app.MainView") as mock_main_view_class:
            mock_main_view_class.return_value.grid = MagicMock()
            with patch("src.ui.interface_app.PATH_ICON", "icon.ico"):
                InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        mock_root.title.assert_called_once_with("Notepad APP")

    def test_geometry_is_set(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with patch("src.ui.interface_app.MainView") as mock_main_view_class:
            mock_main_view_class.return_value.grid = MagicMock()
            with patch("src.ui.interface_app.PATH_ICON", "icon.ico"):
                InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        mock_root.geometry.assert_called_once_with("800x800")

    def test_is_not_resizable(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with patch("src.ui.interface_app.MainView") as mock_main_view_class:
            mock_main_view_class.return_value.grid = MagicMock()
            with patch("src.ui.interface_app.PATH_ICON", "icon.ico"):
                InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        mock_root.resizable.assert_called_once_with(False, False)

    def test_iconbitmap_is_set(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with patch("src.ui.interface_app.MainView") as mock_main_view_class:
            mock_main_view_class.return_value.grid = MagicMock()
            with patch("src.ui.interface_app.PATH_ICON", "icon.ico"):
                InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        mock_root.iconbitmap.assert_called_once_with("icon.ico")

    def test_default_styles_is_styles_instance(self, mock_root: MagicMock) -> None:
        with patch("src.ui.interface_app.MainView") as mock_main_view_class:
            mock_main_view_class.return_value.grid = MagicMock()
            with patch("src.ui.interface_app.PATH_ICON", "icon.ico"):
                app: InterfaceApp = InterfaceApp(root=mock_root, config=MagicMock())
        assert isinstance(app._styles, Styles)

    def test_main_view_receives_callbacks(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with patch("src.ui.interface_app.MainView") as mock_main_view_class:
            mock_main_view_class.return_value.grid = MagicMock()
            with patch("src.ui.interface_app.PATH_ICON", "icon.ico"):
                InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        _, kwargs = mock_main_view_class.call_args
        assert callable(kwargs.get("on_open"))
        assert callable(kwargs.get("on_save"))
        assert callable(kwargs.get("on_delete"))
        assert callable(kwargs.get("on_change_font"))

    def test_main_view_grid_called(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with patch("src.ui.interface_app.MainView") as mock_main_view_class:
            mock_main_view: MagicMock = MagicMock()
            mock_main_view_class.return_value = mock_main_view
            with patch("src.ui.interface_app.PATH_ICON", "icon.ico"):
                InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        mock_main_view.grid.assert_called_once_with(row=0, column=0, sticky="nsew")

    def test_columnconfigure_called_on_root(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with patch("src.ui.interface_app.MainView") as mock_main_view_class:
            mock_main_view_class.return_value.grid = MagicMock()
            with patch("src.ui.interface_app.PATH_ICON", "icon.ico"):
                InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        mock_root.columnconfigure.assert_called_once_with(0, weight=1)

    def test_rowconfigure_called_on_root(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with patch("src.ui.interface_app.MainView") as mock_main_view_class:
            mock_main_view_class.return_value.grid = MagicMock()
            with patch("src.ui.interface_app.PATH_ICON", "icon.ico"):
                InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        mock_root.rowconfigure.assert_called_once_with(0, weight=1)


class TestInterfaceAppGetTxtFromFile:
    def test_set_text_called_when_file_content_is_not_empty(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.FileService.open_file", return_value="file content"):
            interface_app._get_txt_from_file()
        interface_app._main_view.set_text.assert_called_once_with("file content")

    def test_set_text_not_called_when_file_content_is_none(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.FileService.open_file", return_value=None):
            interface_app._get_txt_from_file()
        interface_app._main_view.set_text.assert_not_called()

    def test_set_text_not_called_when_file_content_is_empty_string(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.FileService.open_file", return_value=""):
            interface_app._get_txt_from_file()
        interface_app._main_view.set_text.assert_not_called()


class TestInterfaceAppSaveFile:
    def test_save_file_called_with_text_content(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_text.return_value = "some text"
        with patch("src.ui.interface_app.FileService.save_file") as mock_save:
            interface_app._save_file()
        mock_save.assert_called_once_with("some text")

    def test_get_text_called_before_save(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_text.return_value = "content"
        with patch("src.ui.interface_app.FileService.save_file"):
            interface_app._save_file()
        interface_app._main_view.get_text.assert_called_once()


class TestInterfaceAppDeleteTxt:
    def test_clear_text_is_called(self, interface_app: InterfaceApp) -> None:
        interface_app._delete_txt()
        interface_app._main_view.clear_text.assert_called_once()


class TestInterfaceAppOpenWinConfigFont:
    def test_font_config_view_is_created(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.FontConfigView") as mock_font_view:
            interface_app._open_win_config_font()
        mock_font_view.assert_called_once()

    def test_font_config_view_receives_on_save(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.FontConfigView") as mock_font_view:
            interface_app._open_win_config_font()
        _, kwargs = mock_font_view.call_args
        assert callable(kwargs.get("on_save"))

    def test_font_config_view_receives_root(self, interface_app: InterfaceApp, mock_root: MagicMock) -> None:
        with patch("src.ui.interface_app.FontConfigView") as mock_font_view:
            interface_app._open_win_config_font()
        _, kwargs = mock_font_view.call_args
        assert kwargs.get("root") is mock_root


class TestInterfaceAppSaveConfigFont:
    def test_raises_validation_error_when_font_is_empty(self, interface_app: InterfaceApp) -> None:
        with pytest.raises(ValidationDialogError) as exc_info:
            interface_app._save_config_font(new_font="", new_size="12")
        assert exc_info.value.message == MESSAGE_NOT_VALID_FIELDS

    def test_raises_validation_error_when_size_is_empty(self, interface_app: InterfaceApp) -> None:
        with pytest.raises(ValidationDialogError) as exc_info:
            interface_app._save_config_font(new_font="Arial", new_size="")
        assert exc_info.value.message == MESSAGE_NOT_VALID_FIELDS

    def test_raises_validation_error_when_both_are_empty(self, interface_app: InterfaceApp) -> None:
        with pytest.raises(ValidationDialogError) as exc_info:
            interface_app._save_config_font(new_font="", new_size="")
        assert exc_info.value.message == MESSAGE_NOT_VALID_FIELDS

    def test_raises_validation_error_when_size_is_not_a_number(self, interface_app: InterfaceApp) -> None:
        with pytest.raises(ValidationDialogError) as exc_info:
            interface_app._save_config_font(new_font="Arial", new_size="abc")
        assert exc_info.value.message == MESSAGE_NOT_VALID_FIELD_NUM

    def test_set_font_called_with_font_and_int_size(self, interface_app: InterfaceApp) -> None:
        interface_app._save_config_font(new_font="Arial", new_size="14")
        interface_app._main_view.set_font.assert_called_once_with("Arial", 14)

    def test_set_font_receives_size_as_int(self, interface_app: InterfaceApp) -> None:
        interface_app._save_config_font(new_font="Roboto", new_size="20")
        _, args = interface_app._main_view.set_font.call_args
        positional: tuple = interface_app._main_view.set_font.call_args[0]
        assert isinstance(positional[1], int)

    def test_set_font_not_called_when_font_is_empty(self, interface_app: InterfaceApp) -> None:
        with pytest.raises(ValidationDialogError):
            interface_app._save_config_font(new_font="", new_size="12")
        interface_app._main_view.set_font.assert_not_called()

    def test_set_font_not_called_when_size_is_invalid(self, interface_app: InterfaceApp) -> None:
        with pytest.raises(ValidationDialogError):
            interface_app._save_config_font(new_font="Arial", new_size="not_a_number")
        interface_app._main_view.set_font.assert_not_called()
