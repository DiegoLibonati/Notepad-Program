from pathlib import Path
from test.constants import TEXT_TXT
from unittest.mock import MagicMock, patch

from src.services.file_service import FileService


def test_open_file_returns_content(tmp_path: Path, file_service: FileService):
    test_file = tmp_path / "sample.txt"
    test_file.write_text(TEXT_TXT, encoding="utf-8")

    with patch("tkinter.filedialog.askopenfilename") as mock_dialog:
        mock_dialog.return_value = str(test_file)

        result = file_service.open_file()

        assert result == TEXT_TXT
        mock_dialog.assert_called_once_with(
            initialdir="/",
            title="Select a File",
            filetypes=(("Text files", "*.txt*"), ("All files", "*.*")),
        )


def test_open_file_no_selection_returns_none(file_service: FileService):
    with patch("tkinter.filedialog.askopenfilename") as mock_dialog:
        mock_dialog.return_value = ""

        result = file_service.open_file()

        assert result is None
        mock_dialog.assert_called_once()


def test_save_file_writes_content(file_service: FileService):
    mock_file = MagicMock()

    with patch("tkinter.filedialog.asksaveasfile") as mock_dialog:
        mock_dialog.return_value = mock_file

        file_service.save_file(TEXT_TXT)

        mock_dialog.assert_called_once_with(
            mode="w",
            filetypes=[("Text Document", "*.txt")],
            defaultextension=[("Text Document", "*.txt")],
        )

        mock_file.write.assert_called_once_with(TEXT_TXT)
        mock_file.close.assert_called_once()


def test_save_file_no_selection_does_nothing(file_service: FileService):
    with patch("tkinter.filedialog.asksaveasfile") as mock_dialog:
        mock_dialog.return_value = None

        file_service.save_file(TEXT_TXT)

        mock_dialog.assert_called_once()
