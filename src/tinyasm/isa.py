"""Definiciones estáticas de la arquitectura IA-32 que comparten varias etapas."""

from dataclasses import dataclass

WORD_BITS = 32
MASK32 = 0xFFFF_FFFF

GENERAL_REGISTERS = ("eax", "ebx", "ecx", "edx", "esi", "edi", "esp", "ebp")


@dataclass(frozen=True, slots=True)
class RegisterInfo:
    """Ubicación de un registro dentro de su registro padre de 32 bits.

    Ejemplo: ``ah`` vive en ``eax``, mide 8 bits y está desplazado 8 bits.
    """

    parent: str
    bits: int
    shift: int = 0


def _build_register_table() -> dict[str, RegisterInfo]:
    table = {name: RegisterInfo(name, 32) for name in GENERAL_REGISTERS}
    for name in GENERAL_REGISTERS:
        table[name[1:]] = RegisterInfo(name, 16)  # ax, bx, ..., sp, bp
    for letter in "abcd":
        parent = f"e{letter}x"
        table[f"{letter}l"] = RegisterInfo(parent, 8, 0)
        table[f"{letter}h"] = RegisterInfo(parent, 8, 8)
    return table


REGISTERS: dict[str, RegisterInfo] = _build_register_table()

# Tamaños explícitos de operando en memoria: "dword ptr [eax]".
SIZE_KEYWORDS: dict[str, int] = {"byte": 8, "word": 16, "dword": 32}


def is_register(name: str) -> bool:
    return name.lower() in REGISTERS
