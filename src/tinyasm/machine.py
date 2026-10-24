"""Estado de la máquina: registros, flags y EIP.

Es el único estado mutable del proyecto y sólo el executor lo modifica.
"""

from dataclasses import dataclass, field

from tinyasm.evaluator import Flags
from tinyasm.isa import REGISTERS


@dataclass
class CPU:
    registers: dict[str, int] = field(default_factory=lambda: dict.fromkeys(REGISTERS, 0))
    flags: Flags = field(default_factory=Flags)
    # Simplificación: EIP es el índice de la instrucción, no una dirección en bytes.
    eip: int = 0
    halted: bool = False

    def read_register(self, name: str) -> int:
        """Lee un registro de 32 bits (``eax``, ``ebx``...)."""
        raise NotImplementedError

    def write_register(self, name: str, value: int) -> None:
        """Escribe un registro truncando a 32 bits sin signo (``-1`` queda como ``0xFFFFFFFF``)."""
        raise NotImplementedError
