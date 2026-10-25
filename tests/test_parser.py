import pytest

from tinyasm.errors import ParseError
from tinyasm.nodes import Immediate, Instruction, LabelRef, Register
from tinyasm.parser import parse


def test_register_and_immediate():
    program = parse("mov eax, 5")
    assert program.instructions == (Instruction("mov", (Register("eax"), Immediate(5)), 1),)


def test_negative_immediate_and_label_ref():
    mov, jmp = parse("mov eax, -5\njg loop_start").instructions
    assert mov.operands[1] == Immediate(-5)
    assert jmp.operands == (LabelRef("loop_start"),)


def test_labels_point_to_next_instruction():
    program = parse("start:\n  mov eax, 1\nend: hlt")
    assert program.labels == {"start": 0, "end": 1}


def test_full_program():
    source = """
        mov ecx, 3        ; línea 2
loop_start:
        dec ecx

        cmp ecx, -1
fin:    jg loop_start
    """
    program = parse(source)
    assert program.instructions == (
        Instruction("mov", (Register("ecx"), Immediate(3)), 2),
        Instruction("dec", (Register("ecx"),), 4),
        Instruction("cmp", (Register("ecx"), Immediate(-1)), 6),
        Instruction("jg", (LabelRef("loop_start"),), 7),
    )
    assert program.labels == {"loop_start": 1, "fin": 3}


def test_instruction_without_operands():
    (hlt,) = parse("hlt").instructions
    assert hlt.operands == ()


def test_empty_program():
    program = parse("")
    assert program.instructions == ()
    assert program.labels == {}


def test_several_labels_on_one_line():
    program = parse("a: b: inc eax")
    assert program.labels == {"a": 0, "b": 0}


def test_names_are_lowercased():
    program = parse("Loop: MOV EAX, 1\njmp LOOP")
    assert program.instructions[0] == Instruction("mov", (Register("eax"), Immediate(1)), 1)
    assert program.instructions[1].operands == (LabelRef("loop"),)
    assert program.labels == {"loop": 0}


@pytest.mark.parametrize(
    "source",
    [
        "a: nop\na: nop",  # etiqueta duplicada
        "mov eax, 5 6",  # token sobrante
        "mov eax,",  # falta un operando
        "mov , eax",  # operando vacío
        "mov eax, -ebx",  # '-' sin número
        "5: mov eax, 1",  # la línea empieza con un número
        "mov eax, [ebx]",  # memoria fuera de alcance
    ],
)
def test_invalid_syntax_raises_with_line(source):
    with pytest.raises(ParseError) as error:
        parse("nop\n" + source)
    assert error.value.line in (2, 3)
