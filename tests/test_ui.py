"""Pruebas de la interfaz sin abrir ventanas (plataforma ``offscreen`` de Qt).

Se saltan si PyQt6 no está instalado: el motor no depende de la UI.
"""

import os

import pytest

pytest.importorskip("PyQt6.QtWidgets")
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication

from tinyasm.ui.main_window import MainWindow


@pytest.fixture
def window():
    _app = QApplication.instance() or QApplication([])
    window = MainWindow()
    yield window
    window.close()


def test_loads_first_example(window):
    assert window._examples.currentText() == "01_jmp"
    assert "jmp fin" in window._editor.toPlainText()
    assert window._status.text() == "Listo"


def test_first_instruction_is_highlighted_before_stepping(window):
    window._editor.setPlainText("; comentario\n\ninicio:\n    mov eax, 1\n    hlt")
    assert window._editor._current_line == 4
    window._step()
    assert window._editor._current_line == 5


def test_invalid_code_highlights_nothing_until_run(window):
    window._editor.setPlainText("mov eax, [ebx]")
    assert window._editor._current_line is None
    assert window._status.text() == "Listo"
    window._run()
    assert window._editor._error_line == 1


def test_step_updates_state(window):
    window._editor.setPlainText("mov eax, 5\nmov ebx, 1")
    window._step()
    assert window._executor.cpu.registers["eax"] == 5
    assert window._status.text() == "Paso 1"
    assert window._step_action.isEnabled()


def test_run_until_finished_disables_buttons(window):
    window._editor.setPlainText("mov eax, 5\nhlt")
    window._run()
    assert window._status.text() == "Terminado con hlt en 2 pasos"
    assert not window._step_action.isEnabled()
    assert not window._run_action.isEnabled()


def test_error_is_shown_with_line(window):
    window._editor.setPlainText("mov eax, 1\njmp noexiste")
    window._run()
    assert window._status.text() == "Error en la línea 2: etiqueta inexistente 'noexiste'"
    assert not window._step_action.isEnabled()


def test_editing_resets_execution(window):
    window._editor.setPlainText("mov eax, 5")
    window._run()
    window._editor.setPlainText("mov eax, 6")
    # Ejecución nueva: CPU en ceros y lista en la primera instrucción.
    assert window._executor.steps == 0
    assert window._executor.cpu.registers["eax"] == 0
    assert window._editor._current_line == 1
    assert window._status.text() == "Listo"
    assert window._run_action.isEnabled()
