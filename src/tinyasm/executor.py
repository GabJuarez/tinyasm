"""Etapa 4 — Executor: recorre el Program y muta el estado de la CPU.

"Todo lo que sea decisión de flujo o mutación de estado" vive aquí:
resolver operandos a valores, pedirle cálculos al evaluator, escribir el
resultado en registros/flags y mover EIP (incluidos los saltos).

Para agregar una instrucción: escribe un método ``_op_<mnemonic>`` y regístralo
en ``_handlers``. Ver docs/conventions.md.
"""

from collections.abc import Callable
from dataclasses import dataclass, replace
from functools import partial

from tinyasm import evaluator
from tinyasm.errors import ExecutionError
from tinyasm.isa import CONDITIONS, MASK32
from tinyasm.machine import CPU
from tinyasm.nodes import Immediate, Instruction, LabelRef, Operand, Program, Register
from tinyasm.parser import parse

type Handler = Callable[[Instruction], None]


@dataclass(frozen=True, slots=True)
class Jump:
    """Registro del último salto ejecutado, para mostrarlo en la interfaz."""

    line: int
    mnemonic: str
    target: str
    taken: bool


class Executor:
    def __init__(self, program: Program, cpu: CPU | None = None) -> None:
        self.program = program
        self.cpu = cpu or CPU()
        self.steps = 0
        self.last_jump: Jump | None = None
        self._handlers: dict[str, Handler] = {
            "mov": self._op_mov,
            "add": self._op_add,
            "sub": self._op_sub,
            "inc": self._op_inc,
            "dec": self._op_dec,
            "cmp": self._op_cmp,
            "jmp": self._op_jmp,
            "hlt": self._op_hlt,
        }
        # Todos los jcc comparten handler; sólo cambia la condición.
        for condition in CONDITIONS:
            self._handlers[f"j{condition}"] = partial(self._op_jcc, condition)

    @property
    def finished(self) -> bool:
        """True si se ejecutó ``hlt`` o EIP pasó la última instrucción."""
        return self.cpu.halted or self.cpu.eip >= len(self.program.instructions)

    def step(self) -> bool:
        """Ejecuta una instrucción. Devuelve False cuando el programa terminó."""
        if self.finished:
            return False

        instruction = self.program.instructions[self.cpu.eip]
        handler = self._handlers.get(instruction.mnemonic)
        if handler is None:
            raise ExecutionError(
                f"instrucción no soportada {instruction.mnemonic!r}", instruction.line
            )

        # Se avanza antes de ejecutar: si el handler es un salto tomado, sobrescribe EIP.
        self.cpu.eip += 1
        try:
            handler(instruction)
        except ExecutionError as error:
            # Si falla, EIP se queda en la instrucción que falló.
            self.cpu.eip -= 1
            # _read/_write no conocen la instrucción: aquí se les agrega la línea.
            if error.line is None:
                raise ExecutionError(error.message, instruction.line) from error
            raise
        self.steps += 1
        return True

    def run(self, max_steps: int = 10_000) -> CPU:
        """Ejecuta hasta terminar; ``max_steps`` evita ciclos infinitos."""
        for _ in range(max_steps):
            if not self.step():
                return self.cpu
        if self.finished:
            return self.cpu
        line = self.program.instructions[self.cpu.eip].line
        raise ExecutionError(f"se superó el límite de {max_steps} pasos (¿ciclo infinito?)", line)

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

    def _target(self, operand: Operand) -> int:
        """Resuelve el destino de un salto al índice de la instrucción."""
        match operand:
            case LabelRef(name):
                if name not in self.program.labels:
                    raise ExecutionError(f"etiqueta inexistente {name!r}")
                return self.program.labels[name]
            case _:
                raise ExecutionError("el destino de un salto debe ser una etiqueta")

    def _expect(self, instruction: Instruction, count: int) -> tuple[Operand, ...]:
        """Devuelve los operandos si son exactamente ``count``; si no, lanza el error."""
        if len(instruction.operands) != count:
            raise ExecutionError(
                f"{instruction.mnemonic} espera {count} operando(s), "
                f"recibió {len(instruction.operands)}",
                instruction.line,
            )
        return instruction.operands

    # --- instrucciones (_op_<mnemonic>) -----------------------------------

    def _op_mov(self, instruction: Instruction) -> None:
        dst, src = self._expect(instruction, 2)
        self._write(dst, self._read(src))

    def _op_add(self, instruction: Instruction) -> None:
        dst, src = self._expect(instruction, 2)
        result = evaluator.add(self._read(dst), self._read(src))
        self._write(dst, result.value)
        self.cpu.flags = result.flags

    def _op_sub(self, instruction: Instruction) -> None:
        dst, src = self._expect(instruction, 2)
        result = evaluator.sub(self._read(dst), self._read(src))
        self._write(dst, result.value)
        self.cpu.flags = result.flags

    def _op_inc(self, instruction: Instruction) -> None:
        (dst,) = self._expect(instruction, 1)
        result = evaluator.add(self._read(dst), 1)
        self._write(dst, result.value)
        # inc no toca CF: se conserva el que había.
        self.cpu.flags = replace(result.flags, cf=self.cpu.flags.cf)

    def _op_dec(self, instruction: Instruction) -> None:
        (dst,) = self._expect(instruction, 1)
        result = evaluator.sub(self._read(dst), 1)
        self._write(dst, result.value)
        # dec no toca CF: se conserva el que había.
        self.cpu.flags = replace(result.flags, cf=self.cpu.flags.cf)

    def _op_cmp(self, instruction: Instruction) -> None:
        a, b = self._expect(instruction, 2)
        # Como en x86, el primer operando debe ser un registro (reg, reg · reg, imm).
        if not isinstance(a, Register):
            raise ExecutionError("cmp espera un registro como primer operando")
        # Igual que sub, pero el resultado se descarta: sólo quedan las flags.
        self.cpu.flags = evaluator.sub(self._read(a), self._read(b)).flags

    def _op_jmp(self, instruction: Instruction) -> None:
        (target,) = self._expect(instruction, 1)
        self.cpu.eip = self._target(target)
        self.last_jump = Jump(instruction.line, instruction.mnemonic, target.name, taken=True)

    def _op_jcc(self, condition: str, instruction: Instruction) -> None:
        (target,) = self._expect(instruction, 1)
        # El destino se valida aunque el salto no se tome.
        destination = self._target(target)
        taken = evaluator.condition_met(condition, self.cpu.flags)
        if taken:
            self.cpu.eip = destination
        self.last_jump = Jump(instruction.line, instruction.mnemonic, target.name, taken)

    def _op_hlt(self, instruction: Instruction) -> None:
        self._expect(instruction, 0)
        self.cpu.halted = True


def run_source(source: str) -> CPU:
    """Pipeline completo: texto -> CPU final."""
    return Executor(parse(source)).run()
