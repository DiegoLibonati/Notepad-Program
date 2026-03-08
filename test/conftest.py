from tkinter import StringVar
from unittest.mock import MagicMock

import pytest

from src.ui.styles import Styles


@pytest.fixture
def mock_root() -> MagicMock:
    root: MagicMock = MagicMock()
    root.title = MagicMock()
    root.geometry = MagicMock()
    root.resizable = MagicMock()
    root.config = MagicMock()
    root.iconbitmap = MagicMock()
    root.columnconfigure = MagicMock()
    root.rowconfigure = MagicMock()
    return root


@pytest.fixture
def mock_styles() -> MagicMock:
    styles: MagicMock = MagicMock()
    styles.WHITE_COLOR = "#FFFFFF"
    styles.BLACK_COLOR = "#000000"
    styles.FONT_ARIAL_10 = "Arial 10"
    styles.FONT_ROBOTO_10 = "Roboto 10"
    styles.FONT_ROBOTO_12 = "Roboto 12"
    styles.WRAP_NONE = "none"
    styles.ORIENT_HORIZONTAL = "horizontal"
    styles.POSITION_END = "end"
    return styles


@pytest.fixture
def real_styles() -> Styles:
    return Styles()


@pytest.fixture
def mock_on_open() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_on_save() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_on_delete() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_on_change_font() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_on_save_font() -> MagicMock:
    return MagicMock()


@pytest.fixture
def variable() -> MagicMock:
    return MagicMock(spec=StringVar)
