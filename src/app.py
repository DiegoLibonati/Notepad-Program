from tkinter import Tk

from src.models import InterfaceApp


def main():
    root = Tk()
    app = InterfaceApp(root=root)
    root.mainloop()

    print(f"App: {app}")


if __name__ == "__main__":
    main()
