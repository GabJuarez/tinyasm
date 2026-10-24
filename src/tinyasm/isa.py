"""Definiciones estáticas de la arquitectura IA-32 que comparten varias etapas."""

WORD_BITS = 32
MASK32 = 0xFFFF_FFFF

# Sólo los registros de propósito general de 32 bits (ver docs/roadmap.md).
REGISTERS = ("eax", "ebx", "ecx", "edx", "esi", "edi", "esp", "ebp")


def is_register(name: str) -> bool:
    return name.lower() in REGISTERS
