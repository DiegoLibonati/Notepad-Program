# Notepad-Program

## Getting Started

1. Clone the repository
2. Join to the correct path of the clone
3. Use `python notepad.py` to execute program

## Description

I made a python program with user interface using tkinter. This program works like notepad, you can open text files, create and edit them. In addition you can change the font type and change the font type.

## Technologies used

1. Python

## Libraries used

1. Tkinter

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/29`](https://www.diegolibonati.com.ar/#/project/29)

## Video

https://user-images.githubusercontent.com/99032604/199620478-9fc51184-1cc8-45ef-b1cb-24c873a39014.mp4

## Documentation

The `browser_file()` function allows you to open text files in this notepad:

```
def browser_file():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))

    return filename
```

The `get_txt_from_file()` function allows you to get the content of a text file for editing:

```
def get_txt_from_file(entry):

    file = browser_file()

    txt = open(file, "r")

    final_text = txt.read()

    entry.delete(1.0, END)
    entry.insert(END, str(final_text))

    txt.close()
```

The `save_file()` function allows us to save a text file in our operating system:

```
def save_file(entry):
    files = [('Text Document', '*.txt')]

    file = filedialog.asksaveasfile(mode="w",filetypes = files, defaultextension = files)

    file.write(str(entry.get(1.0, END)))

    file.close()
```

The `delete_txt()` function allows you to delete the entire content of a text:

```
def delete_txt(entry):
    entry.delete(1.0, END)
```

The `change_font()` function allows you to change the font of the text:

```
def change_font():
    win = Toplevel(root)
    win.iconbitmap("./icon.ico")
    win.title("Cambiar fuente")
    win.geometry("400x200")
    win.resizable(False, False)
    number_entry = StringVar()

    Label(win, text="Cambia el tipo de la fuente: ", font=("Roboto", 10)).place(x=5, y=10)
    combo_fonts = ttk.Combobox(win, values=font.families(), font=("Roboto", 10))
    combo_fonts.place(x=170, y=10)

    Label(win, text="Cambia el tamaño de la fuente: ", font=("Roboto", 10)).place(x=5, y=40)
    Entry(win, font=("Roboto", 10), width=5, textvariable=number_entry).place(x=200, y=40)

    Button(win, text="Guardar", command=lambda:set_config(combo_fonts ,entry_text, number_entry, win)).place(x=200, y=180, anchor="center")
```

The `set_config()` function allows you to change the current configuration to a new one chosen by the user, you can change the font type and the font size:

```
def set_config(font, entry,size, win):

    try:
        new_font = font.get()

        if isinstance(int(size.get()), int):
            new_size = size.get()
        else:
            new_size = 10

        entry["font"] = (f"{new_font}", f"{new_size}")

        win.destroy()
    except ValueError:
        print("No se hicieron cambios por un error o porque no se llenaron nuevos campos")

        win.destroy()
```
