import codec
import tkinter as tk
import webbrowser
import easygui

# Instance of CODEC class
codec = codec.CODEC()

# Main function
def main():
    # Window management, size, colors, title ..
    root = tk.Tk()
    root.geometry('440x210')
    root.title('CODEC GUI')
    root.configure(bg='black')

    # Row 1 -> Load matrix
    row_2 = tk.Frame(root)
    tk.Button(row_2, text='Charger la matrice', command=load, fg='white', bg='black', width="70", height="4").pack(side=tk.LEFT)
    row_2.pack()

    # Row 2 -> Encode / Decode file
    row_2 = tk.Frame(root)
    tk.Button(row_2, text='Chiffrer', command=encode, fg='white', bg='black', width="30", height="4").pack(side=tk.LEFT)
    tk.Button(row_2, text='Déchiffrer', command=decode, fg='white', bg='black', width="30", height="4").pack(side=tk.LEFT)
    row_2.pack()

    # Row 3 -> Github or leave
    row_3 = tk.Frame(root)
    tk.Button(row_3, text='Github', command=github, fg='white', bg='black', width="30", height="4").pack(side=tk.LEFT)
    tk.Button(row_3, text='Quitter', command=root.quit, bg='red', fg='white', width="30", height="4").pack(side=tk.LEFT)
    row_3.pack()
    root.mainloop()


# Load matrix
def load():
    # Select file
    file = easygui.fileopenbox(msg="Charger la matrice G4C", title="CODEC", default='*', filetypes=None, multiple=False)

    if file is not None:
        codec.load_matrix(file)
    else:
        easygui.msgbox(msg="La matrice n'a pas pu être chargé.", title="CODEC - Erreur", ok_button="J'ai compris", root=None)


# Encode file
def encode():
    # Select file
    file = easygui.fileopenbox(msg="Charger le fichier à encoder", title="CODEC", default='*', filetypes=None, multiple=False)

    if file is not None:
        codec.encode(file)
    else:
        easygui.msgbox(msg="Le fichier n'a pas pu être chargé.", title="CODEC - Erreur", ok_button="J'ai compris", root=None)


# Decode file
def decode():
    # Select file
    file = easygui.fileopenbox(msg="Charger le fichier à décoder", title="CODEC", default='*', filetypes=None, multiple=False)

    if file is not None:
        codec.decode(file)
    else:
        easygui.msgbox(msg="Le fichier n'a pas pu être chargé.", title="CODEC - Erreur", ok_button="J'ai compris", root=None)


# Launch github in web browser
def github():
    webbrowser.open('https://github.com/MaaximeLH/codec-gui')


if __name__ == "__main__":
    main()