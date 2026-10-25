"""Cada programa de examples/ debe correr sin errores y terminar con hlt."""

from pathlib import Path

import pytest

from tinyasm.executor import run_source

EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples"

# Registros que cada ejemplo deja al final (los que no aparecen quedan en 0 o no importan).
EXPECTED = {
    "01_jmp": {"eax": 1},
    "02_je_jne": {"ecx": 1, "edx": 1},
    "03_jl_jg_con_signo": {"ecx": 1, "edx": 1},
    "04_jb_ja_sin_signo": {"ecx": 1, "edx": 1},
    "05_jg_vs_ja": {"ecx": 2},
    "06_jc_jo_js": {"ecx": 1, "edx": 1},
    "sum_loop": {"eax": 55},
}


def test_every_example_has_expected_result():
    assert {path.stem for path in EXAMPLES_DIR.glob("*.asm")} == set(EXPECTED)


@pytest.mark.parametrize("name", sorted(EXPECTED))
def test_example_runs_to_hlt(name):
    cpu = run_source((EXAMPLES_DIR / f"{name}.asm").read_text(encoding="utf-8"))
    assert cpu.halted
    for register, value in EXPECTED[name].items():
        assert cpu.registers[register] == value, register
