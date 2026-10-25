"""Etapa 4 — Executor: recorre el Program y muta el estado de la CPU.

"Todo lo que sea decisión de flujo o mutación de estado" vive aquí:
resolver operandos a valores, pedirle cálculos al evaluator, escribir el
resultado en registros/flags y mover EIP (incluidos los saltos).

Para agregar una instrucción: escribe un método ``_op_<mnemonic>`` y regístralo
en ``_handlers``. Ver docs/conventions.md.
"""

from collections.abc import Callable

from tinyasm.errors import ExecutionError
from tinyasm.isa import MASK32
from tinyasm.machine import CPU
from tinyasm.nodes import Immediate, Instruction, LabelRef, Operand, Program, Register
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
        """Resuelve un operando a su valor de 32 bits sin signo."""
        match operand:
            case Register(name):
                return self.cpu.read_register(name)
            case Immediate(value):
                # Un inmediato negativo queda en complemento a 2, igual que en un registro.
                return value & MASK32
            case LabelRef(name):
                raise ExecutionError(f"la etiqueta {name!r} no se puede usar como valor")

    def _write(self, operand: Operand, value: int) -> None:
        """Guarda ``value`` en el operando destino; sólo los registros son destinos válidos."""
        match operand:
            case Register(name):
                self.cpu.write_register(name, value)
            case Immediate(value=imm):
                raise ExecutionError(f"no se puede escribir en el inmediato {imm}")
            case LabelRef(name):
                raise ExecutionError(f"no se puede escribir en la etiqueta {name!r}")

    # --- instrucciones (_op_<mnemonic>) -----------------------------------


def run_source(source: str) -> CPU:
    """Pipeline completo: texto -> CPU final."""
    return Executor(parse(source)).run()
