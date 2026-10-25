"""Interfaz gráfica (PyQt6).

Sólo consume el motor: el motor nunca importa nada de aquí, así que funciona
y se prueba sin tener PyQt instalado.
"""

import sys

from PyQt6.QtWidgets import QApplication

from tinyasm.ui.fonts import enlarged
from tinyasm.ui.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("tinyasm")
    app.setFont(enlarged(app.font()))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
