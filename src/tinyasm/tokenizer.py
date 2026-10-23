"""Etapa 1 — Tokenizer: texto fuente -> lista de tokens.

Sólo reconoce *formas* (identificadores, números, símbolos). No decide si un
identificador es registro, mnemónico o etiqueta: eso le toca al parser.

Reglas esperadas:
- Los comentarios empiezan con ``;`` y llegan hasta el fin de línea.
- Números: decimal (``10``), hex (``0x1F`` o ``1Fh``), binario (``0b101``).
- Cada línea termina con un token NEWLINE y la lista termina con EOF.
- Un carácter no reconocido lanza ``TokenizeError`` con su número de línea.
"""

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    IDENTIFIER = auto()  # mnemónicos, registros, etiquetas, "dword", "ptr"
    NUMBER = auto()
    COMMA = auto()
    COLON = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    NEWLINE = auto()
    EOF = auto()


@dataclass(frozen=True, slots=True)
class Token:
    type: TokenType
    text: str
    line: int
    column: int
    value: int | None = None  # sólo para NUMBER


def parse_number(text: str) -> int:
    """Convierte un literal numérico (``10``, ``0x1F``, ``1Fh``, ``0b101``) a entero."""
    raise NotImplementedError


def tokenize(source: str) -> list[Token]:
    """Divide ``source`` en tokens. Siempre termina con un token EOF."""
    raise NotImplementedError
