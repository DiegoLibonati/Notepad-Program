from tkinter import filedialog


class FileService:
    @staticmethod
    def open_file() -> str | None:
        file_path = filedialog.askopenfilename(
            initialdir="/",
            title="Select a File",
            filetypes=(("Text files", "*.txt*"), ("All files", "*.*")),
        )

        if not file_path:
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def save_file(content: str) -> None:
        files = [("Text Document", "*.txt")]
        file = filedialog.asksaveasfile(
            mode="w", filetypes=files, defaultextension=files
        )
        if file:
            file.write(content)
            file.close()
