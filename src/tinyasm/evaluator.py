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
    """Interpreta un valor como entero con signo en complemento a dos."""
    if bits <= 0:
        raise ValueError("bits debe ser mayor que cero")

    mask = (1 << bits) - 1
    value = value & mask
    sign_bit = 1 << (bits - 1)

    if value & sign_bit:
        return value - (1 << bits)

    return value


def add(a: int, b: int, bits: int = WORD_BITS) -> AluResult:
    """Suma dos valores y calcula las flags."""
    mask = (1 << bits) - 1

    a = a & mask
    b = b & mask

    raw_result = a + b
    value = raw_result & mask

    cf = raw_result > mask
    zf = value == 0
    sf = bool((value >> (bits - 1)) & 1)

    sign_a = bool((a >> (bits - 1)) & 1)
    sign_b = bool((b >> (bits - 1)) & 1)

    of = (sign_a == sign_b) and (sf != sign_a)

    flags = Flags(cf=cf, zf=zf, sf=sf, of=of)

    return AluResult(value=value, flags=flags)


def sub(a: int, b: int, bits: int = WORD_BITS) -> AluResult:
    """Resta dos valores y calcula las flags. Tambien sirve para CMP."""
    mask = (1 << bits) - 1

    a = a & mask
    b = b & mask

    raw_result = a - b
    value = raw_result & mask

    cf = a < b
    zf = value == 0
    sf = bool((value >> (bits - 1)) & 1)

    sign_a = bool((a >> (bits - 1)) & 1)
    sign_b = bool((b >> (bits - 1)) & 1)

    of = (sign_a != sign_b) and (sf != sign_a)

    flags = Flags(cf=cf, zf=zf, sf=sf, of=of)

    return AluResult(value=value, flags=flags)


def condition_met(condition: str, flags: Flags) -> bool:
    """Comprueba si se cumple una condicion de salto."""
    condition = condition.strip().lower()

    conditions = {
        # Igualdad
        "e": flags.zf,
        "z": flags.zf,
        "ne": not flags.zf,
        "nz": not flags.zf,
        # Comparaciones con signo
        "g": not flags.zf and flags.sf == flags.of,
        "nle": not flags.zf and flags.sf == flags.of,
        "ge": flags.sf == flags.of,
        "nl": flags.sf == flags.of,
        "l": flags.sf != flags.of,
        "nge": flags.sf != flags.of,
        "le": flags.zf or flags.sf != flags.of,
        "ng": flags.zf or flags.sf != flags.of,
        # Comparaciones sin signo
        "a": not flags.cf and not flags.zf,
        "nbe": not flags.cf and not flags.zf,
        "ae": not flags.cf,
        "nb": not flags.cf,
        "nc": not flags.cf,
        "b": flags.cf,
        "nae": flags.cf,
        "c": flags.cf,
        "be": flags.cf or flags.zf,
        "na": flags.cf or flags.zf,
        # Signo y desbordamiento
        "s": flags.sf,
        "ns": not flags.sf,
        "o": flags.of,
        "no": not flags.of,
    }

    if condition not in conditions:
        raise ValueError(f"Condicion desconocida: {condition}")

    return conditions[condition]
