import pytest

from tinyasm import evaluator
from tinyasm.evaluator import Flags


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


def test_signed_vs_unsigned_after_cmp():
    # cmp eax, ebx con eax = -1 (0xFFFFFFFF) y ebx = 1
    flags = evaluator.sub(0xFFFF_FFFF, 1).flags
    assert not evaluator.condition_met("g", flags)  # con signo: -1 > 1 es falso
    assert evaluator.condition_met("a", flags)  # sin signo: 0xFFFFFFFF > 1


@pytest.mark.parametrize(
    ("alias", "main"),
    [
        ("z", "e"),
        ("nz", "ne"),
        ("nle", "g"),
        ("nl", "ge"),
        ("nge", "l"),
        ("ng", "le"),
        ("nbe", "a"),
        ("nb", "ae"),
        ("nc", "ae"),
        ("nae", "b"),
        ("c", "b"),
        ("na", "be"),
    ],
)
def test_aliases_match_main_condition(alias, main):
    for flags in (Flags(), Flags(cf=True), Flags(zf=True), Flags(sf=True), Flags(of=True)):
        assert evaluator.condition_met(alias, flags) == evaluator.condition_met(main, flags)
