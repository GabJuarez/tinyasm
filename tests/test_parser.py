import pytest

from tinyasm.nodes import Immediate, Instruction, LabelRef, Register
from tinyasm.parser import parse

pytestmark = pytest.mark.xfail(raises=NotImplementedError, strict=True, reason="parser pendiente")


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
