from tkinter import StringVar
from unittest.mock import MagicMock, patch

import pytest

from src.ui.views.font_config_view import FontConfigView


@pytest.fixture
def font_config_view(mock_root: MagicMock, mock_styles: MagicMock, mock_on_save_font: MagicMock) -> FontConfigView:
    with (
        patch("src.ui.views.font_config_view.Toplevel.__init__", return_value=None),
        patch("src.ui.views.font_config_view.FontConfigForm"),
        patch("src.ui.views.font_config_view.Button"),
        patch("src.ui.views.font_config_view.StringVar"),
        patch("src.ui.views.font_config_view.font.families", return_value=["Arial", "Roboto"]),
        patch.object(FontConfigView, "iconbitmap"),
        patch.object(FontConfigView, "title"),
        patch.object(FontConfigView, "geometry"),
        patch.object(FontConfigView, "resizable"),
        patch.object(FontConfigView, "columnconfigure"),
    ):
        instance: FontConfigView = FontConfigView.__new__(FontConfigView)
        instance._styles = mock_styles
        instance._on_save = mock_on_save_font
        instance._entry_number = MagicMock(spec=StringVar)
        instance._font_config_form = MagicMock()
        return instance


class TestFontConfigViewInit:
    def test_stores_styles(self, font_config_view: FontConfigView, mock_styles: MagicMock) -> None:
        assert font_config_view._styles == mock_styles

    def test_stores_on_save(self, font_config_view: FontConfigView, mock_on_save_font: MagicMock) -> None:
        assert font_config_view._on_save == mock_on_save_font

    def test_title_is_set(self, mock_root: MagicMock, mock_styles: MagicMock, mock_on_save_font: MagicMock) -> None:
        with (
            patch("src.ui.views.font_config_view.Toplevel.__init__", return_value=None),
            patch("src.ui.views.font_config_view.FontConfigForm") as mock_form,
            patch("src.ui.views.font_config_view.Button") as mock_button,
            patch("src.ui.views.font_config_view.StringVar"),
            patch("src.ui.views.font_config_view.font.families", return_value=[]),
            patch.object(FontConfigView, "iconbitmap"),
            patch.object(FontConfigView, "title") as mock_title,
            patch.object(FontConfigView, "geometry"),
            patch.object(FontConfigView, "resizable"),
            patch.object(FontConfigView, "columnconfigure"),
        ):
            mock_form.return_value.grid = MagicMock()
            mock_button.return_value.grid = MagicMock()
            instance: FontConfigView = FontConfigView.__new__(FontConfigView)
            instance._styles = mock_styles
            FontConfigView.__init__(instance, root=mock_root, styles=mock_styles, on_save=mock_on_save_font)

        mock_title.assert_called_once_with("Change font")

    def test_geometry_is_set(self, mock_root: MagicMock, mock_styles: MagicMock, mock_on_save_font: MagicMock) -> None:
        with (
            patch("src.ui.views.font_config_view.Toplevel.__init__", return_value=None),
            patch("src.ui.views.font_config_view.FontConfigForm") as mock_form,
            patch("src.ui.views.font_config_view.Button") as mock_button,
            patch("src.ui.views.font_config_view.StringVar"),
            patch("src.ui.views.font_config_view.font.families", return_value=[]),
            patch.object(FontConfigView, "iconbitmap"),
            patch.object(FontConfigView, "title"),
            patch.object(FontConfigView, "geometry") as mock_geometry,
            patch.object(FontConfigView, "resizable"),
            patch.object(FontConfigView, "columnconfigure"),
        ):
            mock_form.return_value.grid = MagicMock()
            mock_button.return_value.grid = MagicMock()
            instance: FontConfigView = FontConfigView.__new__(FontConfigView)
            instance._styles = mock_styles
            FontConfigView.__init__(instance, root=mock_root, styles=mock_styles, on_save=mock_on_save_font)

        mock_geometry.assert_called_once_with("400x200")

    def test_is_not_resizable(self, mock_root: MagicMock, mock_styles: MagicMock, mock_on_save_font: MagicMock) -> None:
        with (
            patch("src.ui.views.font_config_view.Toplevel.__init__", return_value=None),
            patch("src.ui.views.font_config_view.FontConfigForm") as mock_form,
            patch("src.ui.views.font_config_view.Button") as mock_button,
            patch("src.ui.views.font_config_view.StringVar"),
            patch("src.ui.views.font_config_view.font.families", return_value=[]),
            patch.object(FontConfigView, "iconbitmap"),
            patch.object(FontConfigView, "title"),
            patch.object(FontConfigView, "geometry"),
            patch.object(FontConfigView, "resizable") as mock_resizable,
            patch.object(FontConfigView, "columnconfigure"),
        ):
            mock_form.return_value.grid = MagicMock()
            mock_button.return_value.grid = MagicMock()
            instance: FontConfigView = FontConfigView.__new__(FontConfigView)
            instance._styles = mock_styles
            FontConfigView.__init__(instance, root=mock_root, styles=mock_styles, on_save=mock_on_save_font)

        mock_resizable.assert_called_once_with(False, False)

    def test_button_save_command_is_handle_save(self, mock_root: MagicMock, mock_styles: MagicMock, mock_on_save_font: MagicMock) -> None:
        with (
            patch("src.ui.views.font_config_view.Toplevel.__init__", return_value=None),
            patch("src.ui.views.font_config_view.FontConfigForm") as mock_form,
            patch("src.ui.views.font_config_view.Button") as mock_button,
            patch("src.ui.views.font_config_view.StringVar"),
            patch("src.ui.views.font_config_view.font.families", return_value=[]),
            patch.object(FontConfigView, "iconbitmap"),
            patch.object(FontConfigView, "title"),
            patch.object(FontConfigView, "geometry"),
            patch.object(FontConfigView, "resizable"),
            patch.object(FontConfigView, "columnconfigure"),
        ):
            mock_form.return_value.grid = MagicMock()
            mock_button.return_value.grid = MagicMock()
            instance: FontConfigView = FontConfigView.__new__(FontConfigView)
            instance._styles = mock_styles
            FontConfigView.__init__(instance, root=mock_root, styles=mock_styles, on_save=mock_on_save_font)

        _, kwargs = mock_button.call_args
        assert callable(kwargs.get("command"))

    def test_button_text_is_save(self, mock_root: MagicMock, mock_styles: MagicMock, mock_on_save_font: MagicMock) -> None:
        with (
            patch("src.ui.views.font_config_view.Toplevel.__init__", return_value=None),
            patch("src.ui.views.font_config_view.FontConfigForm") as mock_form,
            patch("src.ui.views.font_config_view.Button") as mock_button,
            patch("src.ui.views.font_config_view.StringVar"),
            patch("src.ui.views.font_config_view.font.families", return_value=[]),
            patch.object(FontConfigView, "iconbitmap"),
            patch.object(FontConfigView, "title"),
            patch.object(FontConfigView, "geometry"),
            patch.object(FontConfigView, "resizable"),
            patch.object(FontConfigView, "columnconfigure"),
        ):
            mock_form.return_value.grid = MagicMock()
            mock_button.return_value.grid = MagicMock()
            instance: FontConfigView = FontConfigView.__new__(FontConfigView)
            instance._styles = mock_styles
            FontConfigView.__init__(instance, root=mock_root, styles=mock_styles, on_save=mock_on_save_font)

        _, kwargs = mock_button.call_args
        assert kwargs.get("text") == "Save"


class TestFontConfigViewHandleSave:
    def test_on_save_called_with_font_and_size(self, font_config_view: FontConfigView) -> None:
        font_config_view._font_config_form.get_font.return_value = "Arial"
        font_config_view._entry_number.get.return_value = "12"

        with patch.object(font_config_view, "destroy"):
            font_config_view._handle_save()

        font_config_view._on_save.assert_called_once_with("Arial", "12")

    def test_destroy_is_called_after_save(self, font_config_view: FontConfigView) -> None:
        font_config_view._font_config_form.get_font.return_value = "Arial"
        font_config_view._entry_number.get.return_value = "12"

        with patch.object(font_config_view, "destroy") as mock_destroy:
            font_config_view._handle_save()

        mock_destroy.assert_called_once()
