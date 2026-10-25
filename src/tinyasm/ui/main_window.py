"""Ventana principal: es la única pieza de la UI que conoce al Executor.

Cada botón sigue el mismo camino: tomar el texto del editor, parsearlo si hace
falta, pedirle al executor ``step()`` o ``run()`` y pasarle el estado a los paneles.
"""

from collections.abc import Callable
from pathlib import Path

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QComboBox,
    QLabel,
    QMainWindow,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from tinyasm.errors import TinyAsmError
from tinyasm.evaluator import Flags
from tinyasm.executor import Executor
from tinyasm.machine import CPU
from tinyasm.parser import parse
from tinyasm.ui.editor import CodeEditor
from tinyasm.ui.panels import FLAG_NAMES, FlagsPanel, JumpPanel, RegistersPanel

# src/tinyasm/ui/main_window.py -> raíz del repositorio
EXAMPLES_DIR = Path(__file__).resolve().parents[3] / "examples"


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("tinyasm")
        self.resize(1000, 620)
        self._executor: Executor | None = None

        self._editor = CodeEditor()
        self._registers = RegistersPanel()
        self._flags = FlagsPanel()
        self._jump = JumpPanel()

        toolbar = self.addToolBar("Ejecución")
        toolbar.setMovable(False)
        self._run_action = self._add_action(toolbar, "Ejecutar", self._run)
        self._step_action = self._add_action(toolbar, "Paso", self._step)
        self._add_action(toolbar, "Reiniciar", self._reset)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)
        toolbar.addWidget(QLabel("Ejemplos: "))
        self._examples = QComboBox()
        toolbar.addWidget(self._examples)

        side = QWidget()
        side_layout = QVBoxLayout(side)
        side_layout.setContentsMargins(0, 0, 0, 0)
        side_layout.addWidget(self._registers)
        side_layout.addWidget(self._flags)
        side_layout.addWidget(self._jump)
        side_layout.addStretch()

        splitter = QSplitter()
        splitter.addWidget(self._editor)
        splitter.addWidget(side)
        splitter.setStretchFactor(0, 1)
        splitter.setSizes([560, 440])
        splitter.setChildrenCollapsible(False)
        self.setCentralWidget(splitter)

        self._status = QLabel()
        self.statusBar().addWidget(self._status)

        # Cualquier cambio en el código invalida la ejecución en curso.
        self._editor.textChanged.connect(self._reset)
        self._examples.currentIndexChanged.connect(self._load_example)
        self._fill_examples()
        self._reset()

    def _add_action(self, toolbar, text: str, slot: Callable[[], None]) -> QAction:
        action = QAction(text, self)
        action.triggered.connect(slot)
        toolbar.addAction(action)
        return action

    # --- ejemplos -----------------------------------------------------------

    def _fill_examples(self) -> None:
        paths = sorted(EXAMPLES_DIR.glob("*.asm")) if EXAMPLES_DIR.is_dir() else []
        for path in paths:
            self._examples.addItem(path.stem, path)
        self._examples.setEnabled(bool(paths))

    def _load_example(self, index: int) -> None:
        path = self._examples.itemData(index)
        if path is not None:
            self._editor.setPlainText(path.read_text(encoding="utf-8"))

    # --- acciones -----------------------------------------------------------

    def _run(self) -> None:
        self._execute(Executor.run)

    def _step(self) -> None:
        self._execute(Executor.step)

    def _reset(self) -> None:
        # Se parsea en silencio para resaltar la primera instrucción antes del primer paso.
        # Si el código tiene errores (p. ej. a medio escribir), el error se muestra hasta
        # que se presione Ejecutar o Paso.
        try:
            self._executor = Executor(parse(self._editor.toPlainText()))
        except TinyAsmError:
            self._executor = None

        line = None
        finished = False
        if self._executor is not None:
            finished = self._executor.finished
            if not finished:
                line = self._executor.program.instructions[0].line

        cpu = CPU()
        self._registers.refresh(cpu, changed=set(), line=line, finished=finished)
        self._flags.refresh(cpu.flags, changed=set())
        self._jump.refresh(None)
        self._editor.set_current_line(line)
        self._editor.set_error_line(None)
        self._set_running(True)
        self._status.setText("Listo")

    def _execute(self, action: Callable[[Executor], object]) -> None:
        try:
            if self._executor is None:
                self._executor = Executor(parse(self._editor.toPlainText()))
        except TinyAsmError as error:
            self._show_error(error)
            return

        cpu = self._executor.cpu
        registers_before, flags_before = dict(cpu.registers), cpu.flags
        try:
            action(self._executor)
        except TinyAsmError as error:
            self._refresh(registers_before, flags_before)
            self._show_error(error)
            return
        self._refresh(registers_before, flags_before)

    # --- pintar el estado ---------------------------------------------------

    def _refresh(self, registers_before: dict[str, int], flags_before: Flags) -> None:
        executor = self._executor
        cpu = executor.cpu
        changed = {name for name, value in cpu.registers.items() if value != registers_before[name]}
        changed_flags = {
            name for name in FLAG_NAMES if getattr(cpu.flags, name) != getattr(flags_before, name)
        }
        line = None if executor.finished else executor.program.instructions[cpu.eip].line

        self._registers.refresh(cpu, changed, line, executor.finished)
        self._flags.refresh(cpu.flags, changed_flags)
        self._jump.refresh(executor.last_jump)
        self._editor.set_current_line(line)
        self._editor.set_error_line(None)
        self._set_running(not executor.finished)

        if executor.finished:
            how = "con hlt" if cpu.halted else "al llegar al final"
            self._status.setText(f"Terminado {how} en {executor.steps} pasos")
        else:
            self._status.setText(f"Paso {executor.steps}")

    def _show_error(self, error: TinyAsmError) -> None:
        self._editor.set_error_line(error.line)
        self._set_running(False)
        where = f" en la línea {error.line}" if error.line is not None else ""
        self._status.setText(f"Error{where}: {error.message}")

    def _set_running(self, enabled: bool) -> None:
        self._run_action.setEnabled(enabled)
        self._step_action.setEnabled(enabled)
