"""Fuentes compartidas por la interfaz."""

from PyQt6.QtGui import QFont, QFontDatabase

# Puntos que se suman al tamaño por defecto del sistema.
SIZE_INCREASE = 2


def enlarged(font: QFont) -> QFont:
    font = QFont(font)
    font.setPointSizeF(font.pointSizeF() + SIZE_INCREASE)
    return font


def fixed_font() -> QFont:
    """Fuente monoespaciada del sistema, para código y valores numéricos."""
    return enlarged(QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont))
