from tkinter import *
from tkinter import ttk, filedialog
from tkinter import font

root = Tk()

root.title("Notepad APP")
root.geometry("800x800")
root.iconbitmap("icon.ico")

def browser_file():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
      
    return filename

def get_txt_from_file(entry):
    
    file = browser_file()

    txt = open(file, "r")

    final_text = txt.read()

    entry.delete(1.0, END)
    entry.insert(END, str(final_text))

    txt.close()

def save_file(entry):
    files = [('Text Document', '*.txt')]

    file = filedialog.asksaveasfile(mode="w",filetypes = files, defaultextension = files)

    file.write(str(entry.get(1.0, END)))

    file.close()

def delete_txt(entry):
    entry.delete(1.0, END)

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


# Menu
menu_bar = Menu(root)
root.config(menu=menu_bar)
filemenu = Menu(menu_bar, tearoff=0)
configmenu = Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label="Archivo", menu=filemenu)
menu_bar.add_cascade(label="Configuracion", menu=configmenu)

filemenu.add_command(label="Abrir", command=lambda:get_txt_from_file(entry_text))
filemenu.add_command(label="Guardar", command=lambda:save_file(entry_text))
filemenu.add_command(label="Borrar todo el texto", command=lambda:delete_txt(entry_text))
filemenu.add_separator()
filemenu.add_command(label="Salir", command=lambda:exit())

configmenu.add_command(label="Cambiar fuente", command=lambda:change_font())

# Scroll bar
scrollbar_vertical = Scrollbar(root)
scrollbar_vertical.pack(side=RIGHT, fill=Y)
scrollbar_horizontal = Scrollbar(root, orient=HORIZONTAL)
scrollbar_horizontal.pack(side=BOTTOM, fill=X)

# Entry Text
entry_text = Text(root, font=('Arial 10'), wrap=NONE, padx=5, pady=5, yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)
entry_text.pack(expand=True, fill=BOTH)

# Scroll bar final config
scrollbar_vertical.config(command=entry_text.yview)
scrollbar_horizontal.config(command=entry_text.xview)



root.mainloop()