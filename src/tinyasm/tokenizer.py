"""Etapa 1 — Tokenizer: texto fuente -> lista de tokens.

Sólo reconoce *formas* (identificadores, números, símbolos). No decide si un
identificador es registro, mnemónico o etiqueta: eso le toca al parser.
"""

from dataclasses import dataclass
from enum import Enum, auto

from tinyasm.errors import TokenizeError


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


# Símbolos de un solo carácter -> su tipo de token
SYMBOLS: dict[str, TokenType] = {
    ",": TokenType.COMMA,
    ":": TokenType.COLON,
    "[": TokenType.LBRACKET,
    "]": TokenType.RBRACKET,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
}


def parse_number(text: str) -> int:
    """Convierte un literal numérico de NASM/MASM a entero."""
    lowered = text.lower()
    if lowered.startswith("0x"):
        return int(lowered[2:], 16)
    # El sufijo "h" va antes que "0b": en "0Bh" la b es un dígito hexadecimal.
    if lowered.endswith("h"):
        return int(lowered[:-1], 16)
    if lowered.startswith("0b"):
        return int(lowered[2:], 2)
    return int(lowered, 10)


def tokenize(source: str) -> list[Token]:
    """Divide ``source`` en tokens. Siempre termina con un token EOF."""
    lines: list[str] = source.splitlines()
    tokens: list[Token] = []

    for line_no, line in enumerate(lines, start=1):
        i = 0
        while i < len(line):
            char = line[i]
            if char.isspace():
                i += 1

            elif char == ";":
                break

            elif char in SYMBOLS:
                tokens.append(Token(SYMBOLS[char], char, line_no, i + 1))
                i += 1

            elif char.isdigit():
                temp_number: str = ""
                col_no = i + 1
                while i < len(line) and line[i].isalnum():
                    temp_number += line[i]
                    i += 1
                try:
                    value = parse_number(temp_number)
                except ValueError:
                    raise TokenizeError(
                        f"número inválido {temp_number!r} (columna {col_no})", line_no
                    ) from None
                tokens.append(Token(TokenType.NUMBER, temp_number, line_no, col_no, value))

            elif char.isalpha() or char == "." or char == "_" or char == "?":
                temp_word: str = ""
                col_no = i + 1
                while i < len(line) and (line[i].isalnum() or line[i] in "._?"):
                    temp_word += line[i]
                    i += 1
                tokens.append(Token(TokenType.IDENTIFIER, temp_word, line_no, col_no))

            else:
                raise TokenizeError(f"carácter inesperado {char!r} (columna {i + 1})", line_no)

        tokens.append(Token(TokenType.NEWLINE, "\n", line_no, len(line) + 1))

    # Con el texto vacío no hay un token previo del cual tomar la posición
    if tokens:
        tokens.append(Token(TokenType.EOF, "", tokens[-1].line, tokens[-1].column + 1))
    else:
        tokens.append(Token(TokenType.EOF, "", 1, 1))
    return tokens
