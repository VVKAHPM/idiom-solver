import tkinter as tk
from gui import IdiomSolverApp

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Idiom-solver")
    root.iconbitmap("images/favicon_k3k_icon.ico")

    app = IdiomSolverApp(root)
    root.mainloop()