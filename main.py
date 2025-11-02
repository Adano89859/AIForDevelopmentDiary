"""
Development Diary - Aplicación de diario de desarrollo
Punto de entrada principal
"""

import tkinter as tk
from ui.main_window import MainWindow


def main():
    """Inicializa y ejecuta la aplicación"""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()