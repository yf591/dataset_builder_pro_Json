# main.py

from tkinter import Tk
from gui.main_window import MainWindow

if __name__ == "__main__":
    root = Tk()
    app = MainWindow(root)
    app.pack(expand=True, fill="both")  # MainWindow を root にフィットさせる
    root.mainloop()