# main.py (in project root)
from balatro.gui import GameGUI  # <-- Must match class name
import tkinter as tk

def main():
    root = tk.Tk()
    GameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()