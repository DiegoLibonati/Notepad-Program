from unittest.mock import MagicMock, mock_open, patch

from src.services.file_service import FileService


class TestFileServiceOpenFile:
    def test_returns_none_when_no_file_selected(self) -> None:
        with patch("src.services.file_service.filedialog.askopenfilename", return_value=""):
            result: str | None = FileService.open_file()
        assert result is None

    def test_returns_file_content_when_file_selected(self) -> None:
        mock_content: str = "Hello world"
        with (
            patch("src.services.file_service.filedialog.askopenfilename", return_value="/path/to/file.txt"),
            patch("builtins.open", mock_open(read_data=mock_content)),
        ):
            result: str | None = FileService.open_file()
        assert result == mock_content

    def test_opens_file_with_utf8_encoding(self) -> None:
        with (
            patch("src.services.file_service.filedialog.askopenfilename", return_value="/path/to/file.txt"),
            patch("builtins.open", mock_open(read_data="content")) as mock_file,
        ):
            FileService.open_file()
        mock_file.assert_called_once_with("/path/to/file.txt", "r", encoding="utf-8")

    def test_returns_none_when_dialog_cancelled(self) -> None:
        with patch("src.services.file_service.filedialog.askopenfilename", return_value=None):
            result: str | None = FileService.open_file()
        assert result is None


class TestFileServiceSaveFile:
    def test_writes_content_when_file_is_selected(self) -> None:
        mock_file: MagicMock = MagicMock()
        with (
            patch("src.services.file_service.filedialog.asksaveasfile", return_value=mock_file),
        ):
            FileService.save_file("Hello world")

        mock_file.write.assert_called_once_with("Hello world")
        mock_file.close.assert_called_once()

    def test_does_not_write_when_no_file_selected(self) -> None:
        with patch("src.services.file_service.filedialog.asksaveasfile", return_value=None):
            FileService.save_file("Hello world")

    def test_save_file_called_with_correct_mode(self) -> None:
        mock_file: MagicMock = MagicMock()
        with (
            patch("src.services.file_service.filedialog.asksaveasfile", return_value=mock_file) as mock_dialog,
        ):
            FileService.save_file("content")

        _, kwargs = mock_dialog.call_args
        assert kwargs.get("mode") == "w"
