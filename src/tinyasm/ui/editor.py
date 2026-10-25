"""Editor de código con números de línea y resaltado de líneas."""

from PyQt6.QtCore import QRect, QSize, Qt
from PyQt6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPaintEvent,
    QPalette,
    QResizeEvent,
    QSyntaxHighlighter,
    QTextCharFormat,
    QTextCursor,
    QTextDocument,
    QTextFormat,
)
from PyQt6.QtWidgets import QApplication, QPlainTextEdit, QTextEdit, QWidget

from tinyasm.errors import TokenizeError
from tinyasm.isa import is_register
from tinyasm.tokenizer import TokenType, tokenize
from tinyasm.ui.fonts import fixed_font

# Colores para fondo claro y fondo oscuro: línea actual, línea con error y sintaxis.
LIGHT_LINES = {"current": "#fff3b0", "error": "#f6c6c6"}
DARK_LINES = {"current": "#4a4520", "error": "#5c2a2a"}
LIGHT_SYNTAX = {
    "mnemonic": "#0033b3",
    "register": "#871094",
    "number": "#1750eb",
    "label": "#8c4600",
    "comment": "#8c8c8c",
}
DARK_SYNTAX = {
    "mnemonic": "#cc7832",
    "register": "#9876aa",
    "number": "#6897bb",
    "label": "#e0b060",
    "comment": "#808080",
}


def is_dark() -> bool:
    """True si el sistema usa un tema oscuro (fondo de los editores oscuro)."""
    return QApplication.palette().color(QPalette.ColorRole.Base).lightness() < 128


class AsmHighlighter(QSyntaxHighlighter):
    """Colorea cada línea usando el tokenizer del propio proyecto.

    Así el resaltado coincide con lo que entiende el emulador: el primer
    identificador es el mnemónico, ``nombre:`` es una etiqueta, etc.
    """

    def __init__(self, document: QTextDocument) -> None:
        super().__init__(document)
        colors = DARK_SYNTAX if is_dark() else LIGHT_SYNTAX
        self._formats: dict[str, QTextCharFormat] = {}
        for kind, color in colors.items():
            text_format = QTextCharFormat()
            text_format.setForeground(QColor(color))
            if kind == "mnemonic":
                text_format.setFontWeight(QFont.Weight.Bold)
            if kind == "comment":
                text_format.setFontItalic(True)
            self._formats[kind] = text_format

    def highlightBlock(self, text: str | None) -> None:  # noqa: N802 (nombre impuesto por Qt)
        text = text or ""
        code, semicolon, _ = text.partition(";")
        if semicolon:
            self.setFormat(len(code), len(text) - len(code), self._formats["comment"])

        try:
            tokens = tokenize(code)
        except TokenizeError:
            return  # línea a medio escribir: sólo queda el comentario

        expecting_mnemonic = True
        for i, token in enumerate(tokens):
            if token.type is TokenType.NUMBER:
                kind = "number"
            elif token.type is TokenType.IDENTIFIER:
                followed_by_colon = i + 1 < len(tokens) and tokens[i + 1].type is TokenType.COLON
                if followed_by_colon:
                    kind = "label"
                elif expecting_mnemonic:
                    kind = "mnemonic"
                    expecting_mnemonic = False
                elif is_register(token.text):
                    kind = "register"
                else:
                    kind = "label"
            else:
                continue
            self.setFormat(token.column - 1, len(token.text), self._formats[kind])


class _LineNumberArea(QWidget):
    """Margen izquierdo; el dibujo lo hace el editor."""

    def __init__(self, editor: "CodeEditor") -> None:
        super().__init__(editor)
        self._editor = editor

    def sizeHint(self) -> QSize:  # noqa: N802 (nombre impuesto por Qt)
        return QSize(self._editor.line_number_width(), 0)

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        self._editor.paint_line_numbers(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFont(fixed_font())
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(" ") * 8)

        self._highlighter = AsmHighlighter(self.document())
        self._line_colors = DARK_LINES if is_dark() else LIGHT_LINES
        self._numbers = _LineNumberArea(self)
        self._current_line: int | None = None
        self._error_line: int | None = None

        self.blockCountChanged.connect(self._update_margin)
        self.updateRequest.connect(self._update_numbers)
        self._update_margin()

    # --- resaltado ----------------------------------------------------------

    def set_current_line(self, line: int | None) -> None:
        """Resalta la próxima instrucción a ejecutar (líneas desde 1)."""
        self._current_line = line
        self._refresh_highlights()

    def set_error_line(self, line: int | None) -> None:
        self._error_line = line
        self._refresh_highlights()

    def _refresh_highlights(self) -> None:
        selections = []
        # El error va después para quedar encima si coincide con la línea actual.
        for line, color in (
            (self._current_line, self._line_colors["current"]),
            (self._error_line, self._line_colors["error"]),
        ):
            if line is None:
                continue
            block = self.document().findBlockByNumber(line - 1)
            if not block.isValid():
                continue
            text_format = QTextCharFormat()
            text_format.setBackground(QColor(color))
            text_format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection = QTextEdit.ExtraSelection()
            selection.format = text_format
            selection.cursor = QTextCursor(block)
            selections.append(selection)
        self.setExtraSelections(selections)

    # --- números de línea ---------------------------------------------------

    def line_number_width(self) -> int:
        digits = len(str(max(1, self.blockCount())))
        return 12 + self.fontMetrics().horizontalAdvance("9") * digits

    def _update_margin(self) -> None:
        self.setViewportMargins(self.line_number_width(), 0, 0, 0)

    def _update_numbers(self, rect: QRect, dy: int) -> None:
        if dy:
            self._numbers.scroll(0, dy)
        else:
            self._numbers.update(0, rect.y(), self._numbers.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self._update_margin()

    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: N802
        super().resizeEvent(event)
        area = self.contentsRect()
        self._numbers.setGeometry(
            QRect(area.left(), area.top(), self.line_number_width(), area.height())
        )

    def paint_line_numbers(self, event: QPaintEvent) -> None:
        painter = QPainter(self._numbers)
        painter.fillRect(event.rect(), self.palette().color(QPalette.ColorRole.Window))
        painter.setPen(self.palette().color(QPalette.ColorRole.PlaceholderText))

        block = self.firstVisibleBlock()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.drawText(
                    0,
                    top,
                    self._numbers.width() - 6,
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight,
                    str(block.blockNumber() + 1),
                )
            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
