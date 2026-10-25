"""Definiciones estáticas de la arquitectura IA-32 que comparten varias etapas."""

WORD_BITS = 32
MASK32 = 0xFFFF_FFFF

# Sólo los registros de propósito general de 32 bits (ver docs/roadmap.md).
REGISTERS = ("eax", "ebx", "ecx", "edx", "esi", "edi", "esp", "ebp")


def is_register(name: str) -> bool:
    return name.lower() in REGISTERS


# Sufijos de condición de los saltos condicionales (``j`` + sufijo), alias incluidos.
# El significado de cada uno está en ``evaluator.condition_met`` y en docs/instructions.md.
CONDITIONS = (
    "e", "z", "ne", "nz",
    "g", "nle", "ge", "nl", "l", "nge", "le", "ng",
    "a", "nbe", "ae", "nb", "nc", "b", "nae", "c", "be", "na",
    "s", "ns", "o", "no",
)  # fmt: skip
