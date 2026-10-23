"""Nodos que produce el parser y consume el executor.

Son inmutables: el executor nunca modifica el programa, sólo el estado de la CPU.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Register:
    name: str  # siempre en minúsculas


@dataclass(frozen=True, slots=True)
class Immediate:
    value: int


@dataclass(frozen=True, slots=True)
class Memory:
    """Dirección efectiva: ``[base + index*scale + displacement]``."""

    base: str | None = None
    index: str | None = None
    scale: int = 1
    displacement: int = 0
    size: int | None = None  # bits; None si no se indicó "byte/word/dword ptr"


@dataclass(frozen=True, slots=True)
class LabelRef:
    name: str


type Operand = Register | Immediate | Memory | LabelRef


@dataclass(frozen=True, slots=True)
class Instruction:
    mnemonic: str  # siempre en minúsculas
    operands: tuple[Operand, ...]
    line: int


@dataclass(frozen=True, slots=True)
class Program:
    instructions: tuple[Instruction, ...]
    # etiqueta -> índice de la instrucción a la que apunta
    labels: Mapping[str, int] = field(default_factory=dict)
