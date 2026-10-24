import pytest

from tinyasm.errors import TokenizeError
from tinyasm.tokenizer import TokenType, parse_number, tokenize


@pytest.mark.parametrize(
    ("text", "expected"),
    [("10", 10), ("0x1F", 31), ("1Fh", 31), ("0b101", 5), ("0Bh", 11)],
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


def test_memory_operand_columns():
    tokens = tokenize("loop: add eax, [ebx+4]")
    assert [(t.text, t.column) for t in tokens[:-2]] == [
        ("loop", 1),
        (":", 5),
        ("add", 7),
        ("eax", 11),
        (",", 14),
        ("[", 16),
        ("ebx", 17),
        ("+", 20),
        ("4", 21),
        ("]", 22),
    ]


def test_number_keeps_text_and_value():
    number = tokenize("mov al, 0x1F")[3]
    assert (number.type, number.text, number.value) == (TokenType.NUMBER, "0x1F", 31)


def test_empty_and_comment_lines_only_produce_newlines():
    tokens = tokenize("\n; sólo un comentario\nhlt")
    assert [(t.type, t.line) for t in tokens] == [
        (TokenType.NEWLINE, 1),
        (TokenType.NEWLINE, 2),
        (TokenType.IDENTIFIER, 3),
        (TokenType.NEWLINE, 3),
        (TokenType.EOF, 3),
    ]


def test_empty_source():
    assert [t.type for t in tokenize("")] == [TokenType.EOF]


@pytest.mark.parametrize("source", ["mov eax, @", "mov eax, 12zz"])
def test_invalid_input_raises_with_line(source):
    with pytest.raises(TokenizeError) as error:
        tokenize("nop\n" + source)
    assert error.value.line == 2
