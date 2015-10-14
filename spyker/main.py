from spyker.gui.tkgui import *
import tkinter

if __name__ == "__main__":
    root = Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    MainFrame(root, padding=(3, 3, 12, 12))
    menubar = MenuBar(root)
    root.config(menu=menubar)
    root.mainloop()
