import pytest

from tinyasm.tokenizer import TokenType, parse_number, tokenize

# Quita esta marca cuando el tokenizer esté implementado (strict=True hará que falle si ya pasa).
pytestmark = pytest.mark.xfail(
    raises=NotImplementedError, strict=True, reason="tokenizer pendiente"
)


@pytest.mark.parametrize(
    ("text", "expected"), [("10", 10), ("0x1F", 31), ("1Fh", 31), ("0b101", 5)]
)
def test_parse_number(text, expected):
    assert parse_number(text) == expected


def test_simple_instruction():
    types = [t.type for t in tokenize("mov eax, 5 ; comentario")]
    assert types == [
        TokenType.IDENTIFIER,
        TokenType.IDENTIFIER,
        TokenType.COMMA,
        TokenType.NUMBER,
        TokenType.NEWLINE,
        TokenType.EOF,
    ]
