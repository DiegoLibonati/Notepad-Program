from tkinter import Tk

from src.ui.interface_app import InterfaceApp


def main():
    root = Tk()
    app = InterfaceApp(root=root)
    root.mainloop()

    print(f"App: {app}")


if __name__ == "__main__":
    main()
