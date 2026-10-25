"""Paneles de sólo lectura: muestran el estado que les pasa la ventana."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from tinyasm.evaluator import Flags, to_signed
from tinyasm.executor import Jump
from tinyasm.isa import CONDITIONS, REGISTERS
from tinyasm.machine import CPU
from tinyasm.ui.fonts import fixed_font

CHANGED_COLOR = QColor("#fff3b0")
CHANGED_TEXT_COLOR = QColor("#000000")
FLAG_NAMES = ("cf", "zf", "sf", "of")


class RegistersPanel(QGroupBox):
    """Los 8 registros en hexadecimal, decimal sin signo y decimal con signo."""

    def __init__(self) -> None:
        super().__init__("Registros")
        self._table = QTableWidget(len(REGISTERS), 3)
        self._table.setHorizontalHeaderLabels(["Hex", "Sin signo", "Con signo"])
        self._table.setVerticalHeaderLabels(REGISTERS)
        self._table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self._table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._table.setFont(fixed_font())
        self._table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self._table.verticalHeader().setDefaultSectionSize(self._table.fontMetrics().height() + 8)

        for row in range(len(REGISTERS)):
            for column in range(3):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self._table.setItem(row, column, item)

        # Alto justo para las 8 filas, sin barra de desplazamiento.
        height = self._table.horizontalHeader().sizeHint().height() + 2 * self._table.frameWidth()
        height += sum(self._table.rowHeight(row) for row in range(len(REGISTERS)))
        self._table.setFixedHeight(height)

        self._eip = QLabel()
        self._eip.setFont(fixed_font())

        layout = QVBoxLayout(self)
        layout.addWidget(self._table)
        layout.addWidget(self._eip)

    def refresh(self, cpu: CPU, changed: set[str], line: int | None, finished: bool) -> None:
        for row, name in enumerate(REGISTERS):
            value = cpu.registers[name]
            texts = (f"0x{value:08X}", str(value), str(to_signed(value)))
            for column, text in enumerate(texts):
                item = self._table.item(row, column)
                item.setText(text)
                if name in changed:
                    item.setBackground(CHANGED_COLOR)
                    item.setForeground(CHANGED_TEXT_COLOR)
                else:
                    item.setBackground(QBrush())
                    item.setForeground(QBrush())

        if line is not None:
            self._eip.setText(f"EIP  {cpu.eip}  (línea {line})")
        elif finished:
            self._eip.setText(f"EIP  {cpu.eip}  (fin del programa)")
        else:
            self._eip.setText(f"EIP  {cpu.eip}")


class FlagsPanel(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Flags")
        layout = QHBoxLayout(self)
        self._labels: dict[str, QLabel] = {}
        for name in FLAG_NAMES:
            label = QLabel()
            label.setFont(fixed_font())
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
            label.setMinimumWidth(56)
            layout.addWidget(label)
            self._labels[name] = label

    def refresh(self, flags: Flags, changed: set[str]) -> None:
        for name, label in self._labels.items():
            value = int(getattr(flags, name))
            label.setText(f"{name.upper()}  {value}")
            font = label.font()
            font.setBold(bool(value))
            label.setFont(font)
            if name in changed:
                label.setStyleSheet(
                    f"background: {CHANGED_COLOR.name()}; color: {CHANGED_TEXT_COLOR.name()};"
                )
            else:
                label.setStyleSheet("")


class JumpPanel(QGroupBox):
    """El último jmp/jcc ejecutado: si se tomó y qué condición lo decidió."""

    def __init__(self) -> None:
        super().__init__("Último salto")
        self._instruction = QLabel()
        self._instruction.setFont(fixed_font())
        self._result = QLabel()
        layout = QVBoxLayout(self)
        layout.addWidget(self._instruction)
        layout.addWidget(self._result)

    def refresh(self, jump: Jump | None) -> None:
        if jump is None:
            self._instruction.setText("Ningún salto ejecutado")
            self._result.setText("")
            return

        self._instruction.setText(f"Línea {jump.line}:  {jump.mnemonic} {jump.target}")
        result = "Tomado" if jump.taken else "No tomado"
        if jump.mnemonic == "jmp":
            reason = "salto incondicional"
        else:
            reason = f"salta si {CONDITIONS[jump.mnemonic.removeprefix('j')]}"
        self._result.setText(f"{result}  ({reason})")
