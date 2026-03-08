from unittest.mock import MagicMock, patch

import pytest

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

    def test_default_styles_is_styles_instance(self, mock_root: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PATH_ICON", "icon.ico"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            app: InterfaceApp = InterfaceApp(root=mock_root, config=MagicMock())

        assert isinstance(app._styles, Styles)

    def test_main_view_is_created(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PATH_ICON", "icon.ico"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)

        mock_main_view_class.assert_called_once()


class TestInterfaceAppGetTxtFromFile:
    def test_set_text_called_when_file_content_is_not_none(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.FileService.open_file", return_value="file content"):
            interface_app._get_txt_from_file()

        interface_app._main_view.set_text.assert_called_once_with("file content")

    def test_set_text_not_called_when_file_content_is_none(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.FileService.open_file", return_value=None):
            interface_app._get_txt_from_file()

        interface_app._main_view.set_text.assert_not_called()


class TestInterfaceAppSaveFile:
    def test_get_text_called_before_save(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_text.return_value = "some text"

        with patch("src.ui.interface_app.FileService.save_file") as _mock_save:
            interface_app._save_file()

        interface_app._main_view.get_text.assert_called_once()

    def test_save_file_called_with_text_content(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_text.return_value = "some text"

        with patch("src.ui.interface_app.FileService.save_file") as mock_save:
            interface_app._save_file()

        mock_save.assert_called_once_with("some text")


class TestInterfaceAppDeleteTxt:
    def test_clear_text_is_called(self, interface_app: InterfaceApp) -> None:
        interface_app._delete_txt()
        interface_app._main_view.clear_text.assert_called_once()


class TestInterfaceAppOpenWinConfigFont:
    def test_font_config_view_is_created(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.FontConfigView") as mock_font_config_view:
            interface_app._open_win_config_font()

        mock_font_config_view.assert_called_once()

    def test_font_config_view_receives_on_save(self, interface_app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.FontConfigView") as mock_font_config_view:
            interface_app._open_win_config_font()

        _, kwargs = mock_font_config_view.call_args
        assert callable(kwargs.get("on_save"))


class TestInterfaceAppSaveConfigFont:
    def test_raises_value_error_when_font_is_empty(self, interface_app: InterfaceApp) -> None:
        with pytest.raises(ValueError, match="valid fields"):
            interface_app._save_config_font("", "12")

    def test_raises_value_error_when_size_is_empty(self, interface_app: InterfaceApp) -> None:
        with pytest.raises(ValueError, match="valid fields"):
            interface_app._save_config_font("Arial", "")

    def test_raises_value_error_when_size_is_not_numeric(self, interface_app: InterfaceApp) -> None:
        with pytest.raises(ValueError, match="valid number"):
            interface_app._save_config_font("Arial", "abc")

    def test_set_font_called_with_correct_values(self, interface_app: InterfaceApp) -> None:
        interface_app._save_config_font("Arial", "14")
        interface_app._main_view.set_font.assert_called_once_with("Arial", 14)

    def test_size_is_converted_to_int(self, interface_app: InterfaceApp) -> None:
        interface_app._save_config_font("Arial", "14")
        _, kwargs = interface_app._main_view.set_font.call_args
        call_args: tuple = interface_app._main_view.set_font.call_args[0]
        assert isinstance(call_args[1], int)
