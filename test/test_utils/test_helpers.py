import os
import sys
from unittest.mock import patch

from src.utils.helpers import resource_path


class TestResourcePath:
    def test_returns_string(self) -> None:
        result: str = resource_path("some/path.png")
        assert isinstance(result, str)

    def test_path_contains_relative_path(self) -> None:
        result: str = resource_path("some/path.png")
        assert result.endswith("some/path.png")

    def test_uses_meipass_when_available(self) -> None:
        with patch.object(sys, "_MEIPASS", "/frozen/base", create=True):
            result: str = resource_path("assets/icon.ico")
        assert result == os.path.join("/frozen/base", "assets/icon.ico")

    def test_uses_abspath_when_meipass_not_available(self) -> None:
        result: str = resource_path("assets/icon.ico")
        expected: str = os.path.join(os.path.abspath("."), "assets/icon.ico")
        assert result == expected
