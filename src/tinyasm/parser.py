"""Etapa 2 — Parser: tokens -> Program (instrucciones + tabla de etiquetas).

Gramática propuesta (una instrucción por línea, descendente recursivo):

    line     := (IDENT ':')* [IDENT [operand (',' operand)*]] NEWLINE
    operand  := ['-'] NUMBER | IDENT

Responsabilidades:
- Clasificar identificadores: registro (``isa.is_register``) o etiqueta (``LabelRef``).
- Construir la tabla ``etiqueta -> índice de instrucción``.
- Validar la forma (etiquetas duplicadas, tokens sobrantes...) y lanzar ``ParseError``.
- NO valida si el mnemónico existe ni si los operandos tienen sentido: eso es del executor.
"""

from tinyasm.nodes import Program
from tinyasm.tokenizer import Token, tokenize


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens
        self._pos = 0

    def parse_program(self) -> Program:
        raise NotImplementedError


def parse(source: str) -> Program:
    """Atajo: tokeniza y parsea ``source``."""
    return Parser(tokenize(source)).parse_program()
