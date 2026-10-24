"""Etapa 4 — Executor: recorre el Program y muta el estado de la CPU.

"Todo lo que sea decisión de flujo o mutación de estado" vive aquí:
resolver operandos a valores, pedirle cálculos al evaluator, escribir el
resultado en registros/flags y mover EIP (incluidos los saltos).

Para agregar una instrucción: escribe un método ``_op_<mnemonic>`` y regístralo
en ``_handlers``. Ver docs/conventions.md.
"""

from collections.abc import Callable

from tinyasm.machine import CPU
from tinyasm.nodes import Instruction, Operand, Program
from tinyasm.parser import parse

type Handler = Callable[[Instruction], None]


class Executor:
    def __init__(self, program: Program, cpu: CPU | None = None) -> None:
        self.program = program
        self.cpu = cpu or CPU()
        self._handlers: dict[str, Handler] = {
            # "mov": self._op_mov,
        }

    def step(self) -> bool:
        """Ejecuta una instrucción. Devuelve False cuando el programa terminó."""
        raise NotImplementedError

    def run(self, max_steps: int = 10_000) -> CPU:
        """Ejecuta hasta terminar; ``max_steps`` evita ciclos infinitos."""
        raise NotImplementedError

    # --- operandos --------------------------------------------------------

    def _read(self, operand: Operand) -> int:
        raise NotImplementedError

    def _write(self, operand: Operand, value: int) -> None:
        raise NotImplementedError

    # --- instrucciones (_op_<mnemonic>) -----------------------------------


def run_source(source: str) -> CPU:
    """Pipeline completo: texto -> CPU final."""
    return Executor(parse(source)).run()
