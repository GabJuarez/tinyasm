"""Estado de la máquina: registros, flags, memoria y EIP.

Es el único estado mutable del proyecto y sólo el executor lo modifica.
"""

from dataclasses import dataclass, field

from tinyasm.evaluator import Flags
from tinyasm.isa import GENERAL_REGISTERS


class Memory:
    """Memoria dispersa direccionable por byte, little-endian."""

    def __init__(self) -> None:
        self._bytes: dict[int, int] = {}

    def read(self, address: int, bits: int) -> int:
        raise NotImplementedError

    def write(self, address: int, value: int, bits: int) -> None:
        raise NotImplementedError


@dataclass
class CPU:
    registers: dict[str, int] = field(default_factory=lambda: dict.fromkeys(GENERAL_REGISTERS, 0))
    flags: Flags = field(default_factory=Flags)
    memory: Memory = field(default_factory=Memory)
    # Simplificación: EIP es el índice de la instrucción, no una dirección en bytes.
    eip: int = 0
    halted: bool = False

    def read_register(self, name: str) -> int:
        """Lee cualquier registro (``eax``, ``ax``, ``al``, ``ah``...) usando ``isa.REGISTERS``."""
        raise NotImplementedError

    def write_register(self, name: str, value: int) -> None:
        """Escribe respetando el tamaño: escribir ``al`` no debe tocar el resto de ``eax``."""
        raise NotImplementedError
