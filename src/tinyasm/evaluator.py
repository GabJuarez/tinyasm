"""Etapa 3 — Evaluator: funciones puras que *calculan*.

Reglas de este módulo:
- Reciben valores ya resueltos (enteros, ``Flags``), nunca tokens ni nodos.
- No leen ni modifican la CPU: devuelven resultados nuevos.
- "Todo lo que sea pregunta con respuesta" vive aquí: ¿cuánto da esta suma y
  qué flags deja?, ¿se cumple la condición ``jg`` con estas flags?, etc.

El executor es quien las invoca y decide qué hacer con el resultado.
"""

from dataclasses import dataclass

from tinyasm.isa import WORD_BITS


@dataclass(frozen=True, slots=True)
class Flags:
    """Subconjunto de EFLAGS que modelamos. PF y AF quedan para después (ver roadmap)."""

    cf: bool = False  # carry
    zf: bool = False  # zero
    sf: bool = False  # sign
    of: bool = False  # overflow


@dataclass(frozen=True, slots=True)
class AluResult:
    value: int  # ya truncado a ``bits``
    flags: Flags


def to_signed(value: int, bits: int = WORD_BITS) -> int:
    """Interpreta ``value`` (sin signo) como entero con signo en complemento a 2."""
    raise NotImplementedError


def add(a: int, b: int, bits: int = WORD_BITS) -> AluResult:
    raise NotImplementedError


def sub(a: int, b: int, bits: int = WORD_BITS) -> AluResult:
    """También sirve para ``cmp``: el executor descarta ``value`` y se queda con las flags."""
    raise NotImplementedError


def condition_met(condition: str, flags: Flags) -> bool:
    """¿Se cumple el sufijo de condición (``e``, ``ne``, ``g``, ``l``, ...) con estas flags?"""
    raise NotImplementedError
