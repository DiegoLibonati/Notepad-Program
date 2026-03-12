from unittest.mock import MagicMock, patch

import pytest

from src.constants.messages import MESSAGE_NOT_VALID_FIELD_NUM, MESSAGE_NOT_VALID_FIELDS
from src.ui.interface_app import InterfaceApp
from src.ui.styles import Styles


@pytest.fixture
def interface_app(mock_root: MagicMock, mock_styles: MagicMock) -> InterfaceApp:
    with (
        patch("src.ui.interface_app.MainView") as mock_main_view_class,
        patch("src.ui.interface_app.PATH_ICON", "icon.ico"),
    ):
        mock_main_view: MagicMock = MagicMock()
        mock_main_view.grid = MagicMock()
        mock_main_view_class.return_value = mock_main_view
        instance: InterfaceApp = InterfaceApp.__new__(InterfaceApp)
        instance._styles = mock_styles
        instance._root = mock_root
        instance._config = MagicMock()
        instance._main_view = mock_main_view
        return instance


class TestInterfaceAppInit:
    def test_stores_styles(self, interface_app: InterfaceApp, mock_styles: MagicMock) -> None:
        assert interface_app._styles == mock_styles

    def test_stores_root(self, interface_app: InterfaceApp, mock_root: MagicMock) -> None:
        assert interface_app._root == mock_root

    def test_title_is_set(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PATH_ICON", "icon.ico"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)

        mock_root.title.assert_called_once_with("Notepad APP")

    def test_geometry_is_set(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PATH_ICON", "icon.ico"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)

        mock_root.geometry.assert_called_once_with("800x800")

    def test_is_not_resizable(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PATH_ICON", "icon.ico"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)

        mock_root.resizable.assert_called_once_with(False, False)

    def test_iconbitmap_is_set(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PATH_ICON", "icon.ico"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)

        mock_root.iconbitmap.assert_called_once_with("icon.ico")

    def test_default_styles_is_styles_instance(self, mock_root: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PATH_ICON", "icon.ico"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            app: InterfaceApp = InterfaceApp(root=mock_root, config=MagicMock())

        assert isinstance(app._styles, Styles)

    def test_main_view_receives_callbacks(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PATH_ICON", "icon.ico"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)

        _, kwargs = mock_main_view_class.call_args
        assert callable(kwargs.get("on_open"))
        assert callable(kwargs.get("on_save"))
        assert callable(kwargs.get("on_delete"))
        assert callable(kwargs.get("on_change_font"))


class TestInterfaceAppGetTxtFromFile:
    def test_set_text_called_when_file_content_is_not_empty(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.FileService.open_file", return_value="hello world"):
            interface_app._get_txt_from_file()

        interface_app._main_view.set_text.assert_called_once_with("hello world")

    def test_set_text_not_called_when_file_content_is_none(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.FileService.open_file", return_value=None):
            interface_app._get_txt_from_file()

        interface_app._main_view.set_text.assert_not_called()

    def test_set_text_not_called_when_file_content_is_empty_string(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.FileService.open_file", return_value=""):
            interface_app._get_txt_from_file()

        interface_app._main_view.set_text.assert_not_called()


class TestInterfaceAppSaveFile:
    def test_file_service_save_called_with_text_content(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_text.return_value = "some text"

        with patch("src.ui.interface_app.FileService.save_file") as mock_save:
            interface_app._save_file()

        mock_save.assert_called_once_with("some text")

    def test_get_text_called_before_saving(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_text.return_value = "content"

        with patch("src.ui.interface_app.FileService.save_file"):
            interface_app._save_file()

        interface_app._main_view.get_text.assert_called_once()


class TestInterfaceAppDeleteTxt:
    def test_clear_text_called(self, interface_app: InterfaceApp) -> None:
        interface_app._delete_txt()
        interface_app._main_view.clear_text.assert_called_once()


class TestInterfaceAppOpenWinConfigFont:
    def test_font_config_view_is_created(self, interface_app: InterfaceApp, mock_styles: MagicMock) -> None:
        with patch("src.ui.interface_app.FontConfigView") as mock_font_config_view:
            interface_app._open_win_config_font()

        mock_font_config_view.assert_called_once()

    def test_font_config_view_receives_on_save(self, interface_app: InterfaceApp, mock_styles: MagicMock) -> None:
        with patch("src.ui.interface_app.FontConfigView") as mock_font_config_view:
            interface_app._open_win_config_font()

        _, kwargs = mock_font_config_view.call_args
        assert callable(kwargs.get("on_save"))

    def test_font_config_view_receives_root(self, interface_app: InterfaceApp, mock_root: MagicMock) -> None:
        with patch("src.ui.interface_app.FontConfigView") as mock_font_config_view:
            interface_app._open_win_config_font()

        _, kwargs = mock_font_config_view.call_args
        assert kwargs.get("root") is mock_root


class TestInterfaceAppSaveConfigFont:
    def test_validation_dialog_called_when_font_is_empty(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.ValidationDialogError") as mock_dialog_class:
            mock_dialog_class.return_value = MagicMock()
            interface_app._save_config_font(new_font="", new_size="12")

        mock_dialog_class.assert_called_once_with(message=MESSAGE_NOT_VALID_FIELDS)
        mock_dialog_class.return_value.dialog.assert_called_once()

    def test_validation_dialog_called_when_size_is_empty(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.ValidationDialogError") as mock_dialog_class:
            mock_dialog_class.return_value = MagicMock()
            interface_app._save_config_font(new_font="Arial", new_size="")

        mock_dialog_class.assert_called_once_with(message=MESSAGE_NOT_VALID_FIELDS)
        mock_dialog_class.return_value.dialog.assert_called_once()

    def test_set_font_not_called_when_fields_are_empty(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.ValidationDialogError") as mock_dialog_class:
            mock_dialog_class.return_value = MagicMock()
            interface_app._save_config_font(new_font="", new_size="")

        interface_app._main_view.set_font.assert_not_called()

    def test_validation_dialog_called_when_size_is_not_numeric(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.ValidationDialogError") as mock_dialog_class:
            mock_dialog_class.return_value = MagicMock()
            interface_app._save_config_font(new_font="Arial", new_size="abc")

        mock_dialog_class.assert_called_once_with(message=MESSAGE_NOT_VALID_FIELD_NUM)
        mock_dialog_class.return_value.dialog.assert_called_once()

    def test_set_font_not_called_when_size_is_not_numeric(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.ValidationDialogError") as mock_dialog_class:
            mock_dialog_class.return_value = MagicMock()
            interface_app._save_config_font(new_font="Arial", new_size="abc")

        interface_app._main_view.set_font.assert_not_called()

    def test_set_font_called_with_parsed_int_size(self, interface_app: InterfaceApp) -> None:
        interface_app._save_config_font(new_font="Arial", new_size="14")
        interface_app._main_view.set_font.assert_called_once_with("Arial", 14)

    def test_set_font_receives_int_not_string_size(self, interface_app: InterfaceApp) -> None:
        interface_app._save_config_font(new_font="Roboto", new_size="12")
        _, args = interface_app._main_view.set_font.call_args
        assert isinstance(args.get("new_size") or interface_app._main_view.set_font.call_args[0][1], int)

    def test_validation_dialog_not_called_when_inputs_are_valid(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.ValidationDialogError") as mock_dialog_class:
            interface_app._save_config_font(new_font="Arial", new_size="14")

        mock_dialog_class.assert_not_called()
