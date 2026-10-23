import pytest

from tinyasm.executor import run_source

pytestmark = pytest.mark.xfail(raises=NotImplementedError, strict=True, reason="pipeline pendiente")


def test_mov_and_add():
    cpu = run_source("mov eax, 2\nadd eax, 3")
    assert cpu.registers["eax"] == 5


def test_loop_with_conditional_jump():
    source = """
        mov ecx, 3
        mov eax, 0
    loop_start:
        add eax, 2
        sub ecx, 1
        cmp ecx, 0
        jne loop_start
    """
    assert run_source(source).registers["eax"] == 6
