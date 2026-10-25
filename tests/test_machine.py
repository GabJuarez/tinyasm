import pytest

from tinyasm.errors import ExecutionError
from tinyasm.evaluator import Flags
from tinyasm.isa import REGISTERS
from tinyasm.machine import CPU


def test_new_cpu_starts_clean():
    cpu = CPU()
    assert cpu.registers == dict.fromkeys(REGISTERS, 0)
    assert cpu.flags == Flags()
    assert cpu.eip == 0
    assert cpu.halted is False


def test_write_then_read():
    cpu = CPU()
    cpu.write_register("eax", 5)
    assert cpu.read_register("eax") == 5


@pytest.mark.parametrize(
    ("value", "stored"),
    [
        (-1, 0xFFFF_FFFF),  # negativo -> complemento a 2
        (2**32, 0),  # desborda y da la vuelta
        (2**32 + 3, 3),
        (0xFFFF_FFFF, 0xFFFF_FFFF),  # el máximo cabe tal cual
    ],
)
def test_write_truncates_to_32_bits(value, stored):
    cpu = CPU()
    cpu.write_register("ebx", value)
    assert cpu.read_register("ebx") == stored


def test_cpus_do_not_share_registers():
    cpu1, cpu2 = CPU(), CPU()
    cpu1.write_register("eax", 5)
    assert cpu2.read_register("eax") == 0


@pytest.mark.parametrize("name", ["ax", "al", "EAX", "eip"])
def test_unknown_register_raises(name):
    cpu = CPU()
    with pytest.raises(ExecutionError):
        cpu.read_register(name)
    with pytest.raises(ExecutionError):
        cpu.write_register(name, 1)
