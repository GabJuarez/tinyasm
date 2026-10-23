import pytest

from tinyasm import evaluator
from tinyasm.evaluator import Flags

pytestmark = pytest.mark.xfail(
    raises=NotImplementedError, strict=True, reason="evaluator pendiente"
)


def test_to_signed():
    assert evaluator.to_signed(0xFFFF_FFFF) == -1


def test_add_sets_carry_and_zero():
    result = evaluator.add(0xFFFF_FFFF, 1)
    assert result.value == 0
    assert result.flags == Flags(cf=True, zf=True, sf=False, of=False)


def test_sub_signed_overflow():
    result = evaluator.sub(0x8000_0000, 1)
    assert result.flags.of


def test_condition_met():
    assert evaluator.condition_met("e", Flags(zf=True))
    assert not evaluator.condition_met("ne", Flags(zf=True))
