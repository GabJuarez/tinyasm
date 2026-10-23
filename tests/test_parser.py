import pytest

from tinyasm.nodes import Immediate, Instruction, Memory, Register
from tinyasm.parser import parse

pytestmark = pytest.mark.xfail(raises=NotImplementedError, strict=True, reason="parser pendiente")


def test_register_and_immediate():
    program = parse("mov eax, 5")
    assert program.instructions == (Instruction("mov", (Register("eax"), Immediate(5)), 1),)


def test_memory_operand():
    (instruction,) = parse("mov eax, dword ptr [ebx + ecx*4 - 8]").instructions
    assert instruction.operands[1] == Memory("ebx", "ecx", 4, -8, 32)


def test_labels_point_to_next_instruction():
    program = parse("start:\n  mov eax, 1\nend: hlt")
    assert program.labels == {"start": 0, "end": 1}
