"""Definiciones estáticas de la arquitectura IA-32 que comparten varias etapas."""

WORD_BITS = 32
MASK32 = 0xFFFF_FFFF

# Sólo los registros de propósito general de 32 bits (ver docs/roadmap.md).
REGISTERS = ("eax", "ebx", "ecx", "edx", "esi", "edi", "esp", "ebp")


def is_register(name: str) -> bool:
    return name.lower() in REGISTERS


# Sufijos de condición de los saltos condicionales (``j`` + sufijo), alias incluidos,
# con la condición sobre las flags que los decide (ver docs/instructions.md).
# El cálculo real está en ``evaluator.condition_met``; esto es sólo la descripción.
CONDITIONS = {
    "e": "ZF = 1",
    "z": "ZF = 1",
    "ne": "ZF = 0",
    "nz": "ZF = 0",
    "g": "ZF = 0 y SF = OF",
    "nle": "ZF = 0 y SF = OF",
    "ge": "SF = OF",
    "nl": "SF = OF",
    "l": "SF ≠ OF",
    "nge": "SF ≠ OF",
    "le": "ZF = 1 o SF ≠ OF",
    "ng": "ZF = 1 o SF ≠ OF",
    "a": "CF = 0 y ZF = 0",
    "nbe": "CF = 0 y ZF = 0",
    "ae": "CF = 0",
    "nb": "CF = 0",
    "nc": "CF = 0",
    "b": "CF = 1",
    "nae": "CF = 1",
    "c": "CF = 1",
    "be": "CF = 1 o ZF = 1",
    "na": "CF = 1 o ZF = 1",
    "s": "SF = 1",
    "ns": "SF = 0",
    "o": "OF = 1",
    "no": "OF = 0",
}
