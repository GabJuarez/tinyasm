"""Etapa 2 — Parser: tokens -> Program (instrucciones + tabla de etiquetas).

Gramática (una instrucción por línea):

    line     := (IDENT ':')* [IDENT [operand (',' operand)*]] NEWLINE
    operand  := ['-'] NUMBER | IDENT

Responsabilidades:
- Clasificar identificadores: registro (``isa.is_register``) o etiqueta (``LabelRef``).
- Construir la tabla ``etiqueta -> índice de instrucción``.
- Validar la forma (etiquetas duplicadas, tokens sobrantes...) y lanzar ``ParseError``.
- NO valida si el mnemónico existe ni si los operandos tienen sentido: eso es del executor.
"""

from tinyasm.errors import ParseError
from tinyasm.isa import is_register
from tinyasm.nodes import Immediate, Instruction, LabelRef, Operand, Program, Register
from tinyasm.tokenizer import Token, TokenType, tokenize


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens

    def _split_lines(self) -> list[list[Token]]:
        """Agrupa los tokens por línea, sin incluir NEWLINE ni EOF."""
        lines: list[list[Token]] = []
        current: list[Token] = []

        for token in self._tokens:
            if token.type in (TokenType.NEWLINE, TokenType.EOF):
                lines.append(current)
                current = []
            else:
                current.append(token)
        return lines

    def parse_program(self) -> Program:
        instructions: list[Instruction] = []
        labels: dict[str, int] = {}

        for line in self._split_lines():
            i = 0

            while (
                i + 1 < len(line)
                and line[i].type is TokenType.IDENTIFIER
                and line[i + 1].type is TokenType.COLON
            ):
                name = line[i].text.lower()
                if name in labels:
                    raise ParseError(f"etiqueta duplicada {line[i].text!r}", line[i].line)
                labels[name] = len(instructions)
                i += 2

            # Línea vacía o con solo etiquetas
            if i == len(line):
                continue

            mnemonic_token = line[i]
            if mnemonic_token.type is not TokenType.IDENTIFIER:
                raise ParseError(
                    f"se esperaba una instrucción, se encontró {mnemonic_token.text!r}",
                    mnemonic_token.line,
                )

            operands = [
                self._parse_operand(group, mnemonic_token.line)
                for group in self._split_operands(line[i + 1 :])
            ]
            instructions.append(
                Instruction(mnemonic_token.text.lower(), tuple(operands), mnemonic_token.line)
            )

        return Program(tuple(instructions), labels)

    def _split_operands(self, tokens: list[Token]) -> list[list[Token]]:
        """Parte los tokens de los operandos en grupos separados por comas."""
        if not tokens:
            return []

        groups: list[list[Token]] = []
        current: list[Token] = []
        for token in tokens:
            if token.type is TokenType.COMMA:
                groups.append(current)
                current = []
            else:
                current.append(token)
        groups.append(current)
        return groups

    def _parse_operand(self, group: list[Token], line: int) -> Operand:
        """Convierte los tokens de UN operando en su nodo."""
        match group:
            case [Token(type=TokenType.IDENTIFIER, text=text)]:
                if is_register(text):
                    return Register(text.lower())
                return LabelRef(text.lower())
            case [Token(type=TokenType.NUMBER, value=int(value))]:
                return Immediate(value)
            case [Token(type=TokenType.MINUS), Token(type=TokenType.NUMBER, value=int(value))]:
                return Immediate(-value)
            case []:
                raise ParseError("se esperaba un operando", line)
            case [Token(type=TokenType.LBRACKET), *_]:
                raise ParseError("los operandos de memoria no están soportados", line)
            case _:
                text = " ".join(token.text for token in group)
                raise ParseError(f"operando inválido {text!r}", line)


def parse(source: str) -> Program:
    """Atajo: tokeniza y parsea ``source``."""
    return Parser(tokenize(source)).parse_program()
