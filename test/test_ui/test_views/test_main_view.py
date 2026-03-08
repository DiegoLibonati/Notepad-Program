from unittest.mock import MagicMock, patch

import pytest

from src.ui.views.main_view import MainView


@pytest.fixture
def main_view(
    mock_root: MagicMock,
    mock_styles: MagicMock,
    mock_on_open: MagicMock,
    mock_on_save: MagicMock,
    mock_on_delete: MagicMock,
    mock_on_change_font: MagicMock,
) -> MainView:
    with (
        patch("src.ui.views.main_view.Frame.__init__", return_value=None),
        patch("src.ui.views.main_view.Scrollbar"),
        patch("src.ui.views.main_view.Text"),
        patch("src.ui.views.main_view.Menu"),
        patch.object(MainView, "columnconfigure"),
        patch.object(MainView, "rowconfigure"),
    ):
        instance: MainView = MainView.__new__(MainView)
        instance._styles = mock_styles
        instance._on_open = mock_on_open
        instance._on_save = mock_on_save
        instance._on_delete = mock_on_delete
        instance._on_change_font = mock_on_change_font
        instance._text_entry = MagicMock()
        instance._scrollbar_vertical = MagicMock()
        instance._scrollbar_horizontal = MagicMock()
        return instance


class TestMainViewInit:
    def test_stores_styles(self, main_view: MainView, mock_styles: MagicMock) -> None:
        assert main_view._styles == mock_styles

    def test_stores_on_open(self, main_view: MainView, mock_on_open: MagicMock) -> None:
        assert main_view._on_open == mock_on_open

    def test_stores_on_save(self, main_view: MainView, mock_on_save: MagicMock) -> None:
        assert main_view._on_save == mock_on_save

    def test_stores_on_delete(self, main_view: MainView, mock_on_delete: MagicMock) -> None:
        assert main_view._on_delete == mock_on_delete

    def test_stores_on_change_font(self, main_view: MainView, mock_on_change_font: MagicMock) -> None:
        assert main_view._on_change_font == mock_on_change_font


class TestMainViewGetText:
    def test_calls_text_entry_get(self, main_view: MainView) -> None:
        main_view._text_entry.get.return_value = "Hello world"
        main_view.get_text()
        main_view._text_entry.get.assert_called_once_with(1.0, main_view._styles.POSITION_END)

    def test_returns_text_content(self, main_view: MainView) -> None:
        main_view._text_entry.get.return_value = "Hello world"
        result: str = main_view.get_text()
        assert result == "Hello world"


class TestMainViewSetText:
    def test_deletes_existing_content_before_insert(self, main_view: MainView) -> None:
        main_view.set_text("new content")
        main_view._text_entry.delete.assert_called_once_with(1.0, main_view._styles.POSITION_END)

    def test_inserts_new_content(self, main_view: MainView) -> None:
        main_view.set_text("new content")
        main_view._text_entry.insert.assert_called_once_with(main_view._styles.POSITION_END, "new content")


class TestMainViewClearText:
    def test_deletes_all_content(self, main_view: MainView) -> None:
        main_view.clear_text()
        main_view._text_entry.delete.assert_called_once_with(1.0, main_view._styles.POSITION_END)


class TestMainViewSetFont:
    def test_sets_font_on_text_entry(self, main_view: MainView) -> None:
        main_view._text_entry.__setitem__ = MagicMock()
        main_view.set_font("Arial", 14)
        main_view._text_entry.__setitem__.assert_called_once_with("font", ("Arial", "14"))

    def test_font_values_are_converted_to_string(self, main_view: MainView) -> None:
        main_view._text_entry.__setitem__ = MagicMock()
        main_view.set_font("Roboto", 12)
        _, value = main_view._text_entry.__setitem__.call_args[0]
        assert isinstance(value[0], str)
        assert isinstance(value[1], str)
