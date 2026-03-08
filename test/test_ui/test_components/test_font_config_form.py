from unittest.mock import MagicMock, patch

import pytest

from src.ui.components.font_config_form import FontConfigForm


@pytest.fixture
def font_config_form(mock_styles: MagicMock, variable: MagicMock) -> FontConfigForm:
    with (
        patch("src.ui.components.font_config_form.Frame.__init__", return_value=None),
        patch("src.ui.components.font_config_form.Label"),
        patch("src.ui.components.font_config_form.Entry"),
        patch("src.ui.components.font_config_form.Combobox"),
        patch.object(FontConfigForm, "columnconfigure"),
    ):
        instance: FontConfigForm = FontConfigForm.__new__(FontConfigForm)
        instance._styles = mock_styles
        instance._font_families = [("Arial",), ("Roboto",)]
        instance._entry_number = variable
        instance._combo_fonts = MagicMock()
        return instance


class TestFontConfigFormInit:
    def test_stores_styles(self, font_config_form: FontConfigForm, mock_styles: MagicMock) -> None:
        assert font_config_form._styles == mock_styles

    def test_stores_font_families(self, font_config_form: FontConfigForm) -> None:
        assert font_config_form._font_families == [("Arial",), ("Roboto",)]

    def test_stores_entry_number(self, font_config_form: FontConfigForm, variable: MagicMock) -> None:
        assert font_config_form._entry_number == variable

    def test_combobox_created_with_font_families(self, mock_styles: MagicMock, variable: MagicMock) -> None:
        families: list[tuple[str]] = [("Arial",), ("Roboto",)]
        with (
            patch("src.ui.components.font_config_form.Frame.__init__", return_value=None),
            patch("src.ui.components.font_config_form.Label") as mock_label,
            patch("src.ui.components.font_config_form.Entry") as mock_entry,
            patch("src.ui.components.font_config_form.Combobox") as mock_combo,
            patch.object(FontConfigForm, "columnconfigure"),
        ):
            mock_label.return_value.grid = MagicMock()
            mock_entry.return_value.grid = MagicMock()
            mock_combo.return_value.grid = MagicMock()
            instance: FontConfigForm = FontConfigForm.__new__(FontConfigForm)
            instance._styles = mock_styles
            FontConfigForm.__init__(
                instance,
                parent=MagicMock(),
                styles=mock_styles,
                font_families=families,
                entry_number=variable,
            )

        _, kwargs = mock_combo.call_args
        assert kwargs.get("values") == families

    def test_entry_created_with_entry_number_variable(self, mock_styles: MagicMock, variable: MagicMock) -> None:
        with (
            patch("src.ui.components.font_config_form.Frame.__init__", return_value=None),
            patch("src.ui.components.font_config_form.Label") as mock_label,
            patch("src.ui.components.font_config_form.Entry") as mock_entry,
            patch("src.ui.components.font_config_form.Combobox") as mock_combo,
            patch.object(FontConfigForm, "columnconfigure"),
        ):
            mock_label.return_value.grid = MagicMock()
            mock_entry.return_value.grid = MagicMock()
            mock_combo.return_value.grid = MagicMock()
            instance: FontConfigForm = FontConfigForm.__new__(FontConfigForm)
            instance._styles = mock_styles
            FontConfigForm.__init__(
                instance,
                parent=MagicMock(),
                styles=mock_styles,
                font_families=[],
                entry_number=variable,
            )

        _, kwargs = mock_entry.call_args
        assert kwargs.get("textvariable") == variable

    def test_columnconfigure_called_twice(self, mock_styles: MagicMock, variable: MagicMock) -> None:
        with (
            patch("src.ui.components.font_config_form.Frame.__init__", return_value=None),
            patch("src.ui.components.font_config_form.Label") as mock_label,
            patch("src.ui.components.font_config_form.Entry") as mock_entry,
            patch("src.ui.components.font_config_form.Combobox") as mock_combo,
            patch.object(FontConfigForm, "columnconfigure") as mock_columnconfigure,
        ):
            mock_label.return_value.grid = MagicMock()
            mock_entry.return_value.grid = MagicMock()
            mock_combo.return_value.grid = MagicMock()
            instance: FontConfigForm = FontConfigForm.__new__(FontConfigForm)
            instance._styles = mock_styles
            FontConfigForm.__init__(
                instance,
                parent=MagicMock(),
                styles=mock_styles,
                font_families=[],
                entry_number=variable,
            )

        assert mock_columnconfigure.call_count == 2


class TestFontConfigFormGetFont:
    def test_returns_combo_value(self, font_config_form: FontConfigForm) -> None:
        font_config_form._combo_fonts.get.return_value = "Arial"
        result: str = font_config_form.get_font()
        assert result == "Arial"

    def test_returns_empty_string_when_nothing_selected(self, font_config_form: FontConfigForm) -> None:
        font_config_form._combo_fonts.get.return_value = ""
        result: str = font_config_form.get_font()
        assert result == ""

    def test_calls_combo_get(self, font_config_form: FontConfigForm) -> None:
        font_config_form._combo_fonts.get.return_value = "Roboto"
        font_config_form.get_font()
        font_config_form._combo_fonts.get.assert_called_once()
