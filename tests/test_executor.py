import pytest

from tinyasm import evaluator
from tinyasm.errors import ExecutionError
from tinyasm.evaluator import Flags
from tinyasm.executor import Executor, Jump, run_source
from tinyasm.isa import CONDITIONS
from tinyasm.nodes import Immediate, LabelRef, Program, Register
from tinyasm.parser import parse


@pytest.fixture
def executor():
    return Executor(Program(instructions=(), labels={}))


# --- operandos ------------------------------------------------------------


def test_read_register(executor):
    executor.cpu.write_register("ebx", 7)
    assert executor._read(Register("ebx")) == 7


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (5, 5),
        (-1, 0xFFFF_FFFF),  # negativo -> complemento a 2, igual que en un registro
        (-5, 0xFFFF_FFFB),
    ],
)
def test_read_immediate_is_32_bit_unsigned(executor, value, expected):
    assert executor._read(Immediate(value)) == expected


def test_read_label_raises(executor):
    with pytest.raises(ExecutionError):
        executor._read(LabelRef("loop"))


def test_write_register_truncates(executor):
    executor._write(Register("eax"), -1)
    assert executor.cpu.read_register("eax") == 0xFFFF_FFFF


@pytest.mark.parametrize("operand", [Immediate(5), LabelRef("loop")])
def test_write_to_non_register_raises(executor, operand):
    with pytest.raises(ExecutionError):
        executor._write(operand, 1)


# --- pipeline completo ----------------------------------------------------


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


def test_example_sum_loop():
    with open("examples/sum_loop.asm", encoding="utf-8") as file:
        cpu = run_source(file.read())
    assert cpu.registers["eax"] == 55
    assert cpu.halted


# --- instrucciones --------------------------------------------------------


def test_mov_register_and_negative_immediate():
    cpu = run_source("mov eax, -5\nmov ebx, eax")
    assert cpu.registers["ebx"] == 0xFFFF_FFFB


def test_mov_does_not_touch_flags():
    cpu = run_source("cmp eax, eax\nmov eax, 5")
    assert cpu.flags.zf


def test_add_sets_flags():
    cpu = run_source("mov eax, 0xFFFFFFFF\nadd eax, 1")
    assert cpu.registers["eax"] == 0
    assert cpu.flags == Flags(cf=True, zf=True)


def test_sub_sets_flags():
    cpu = run_source("mov eax, 0\nsub eax, 1")
    assert cpu.registers["eax"] == 0xFFFF_FFFF
    assert cpu.flags == Flags(cf=True, sf=True)


def test_inc_and_dec_keep_carry():
    # add deja CF = 1; inc y dec no deben tocarlo.
    cpu = run_source("mov eax, 0xFFFFFFFF\nadd eax, 1\ninc eax\ndec eax")
    assert cpu.registers["eax"] == 0
    assert cpu.flags.cf
    assert cpu.flags.zf


def test_inc_overflow_sets_of():
    cpu = run_source("mov eax, 0x7FFFFFFF\ninc eax")
    assert cpu.flags.of
    assert cpu.flags.sf


def test_cmp_discards_result():
    cpu = run_source("mov eax, 3\ncmp eax, 5")
    assert cpu.registers["eax"] == 3
    assert cpu.flags == evaluator.sub(3, 5).flags


def test_jmp_skips_instructions():
    cpu = run_source("jmp fin\nmov eax, 1\nfin: mov ebx, 2")
    assert cpu.registers["eax"] == 0
    assert cpu.registers["ebx"] == 2


def test_hlt_stops_execution():
    cpu = run_source("hlt\nmov eax, 1")
    assert cpu.halted
    assert cpu.registers["eax"] == 0


@pytest.mark.parametrize(
    ("jump", "taken"),
    [
        ("jg", False),  # con signo: -1 > 1 es falso
        ("jl", True),
        ("ja", True),  # sin signo: 0xFFFFFFFF > 1
        ("jb", False),
        ("je", False),
        ("jne", True),
    ],
)
def test_jcc_signed_vs_unsigned(jump, taken):
    source = f"""
        mov eax, -1
        cmp eax, 1
        {jump} salto
        mov ebx, 1
    salto:
    """
    cpu = run_source(source)
    assert (cpu.registers["ebx"] == 0) is taken


def test_every_condition_is_known_by_evaluator():
    for condition in CONDITIONS:
        evaluator.condition_met(condition, Flags())


# --- step / run -----------------------------------------------------------


def test_step_by_step():
    executor = Executor(parse("mov eax, 1\nmov ebx, 2"))
    assert executor.step()
    assert executor.cpu.eip == 1
    assert executor.step()
    assert not executor.step()  # ya terminó
    assert not executor.step()  # y sigue sin tronar


def test_empty_program():
    cpu = run_source("")
    assert cpu.eip == 0


def test_program_exactly_max_steps_long():
    cpu = Executor(parse("inc eax\ninc eax")).run(max_steps=2)
    assert cpu.registers["eax"] == 2


def test_infinite_loop_hits_max_steps():
    with pytest.raises(ExecutionError) as error:
        Executor(parse("mov eax, 1\nloop: jmp loop")).run(max_steps=100)
    assert error.value.line == 2


# --- errores --------------------------------------------------------------


@pytest.mark.parametrize(
    "source",
    [
        "push eax",  # instrucción no soportada
        "mov eax",  # faltan operandos
        "add eax, 1, 2",  # sobran operandos
        "hlt eax",
        "jmp noexiste",  # etiqueta inexistente
        "jne noexiste",  # aunque el salto no se tome
        "jmp eax",  # el destino no es etiqueta
        "mov eax, fin\nfin: hlt",  # etiqueta usada como valor
        "mov 5, eax",  # destino inmediato
        "inc 5",
        "cmp 5, eax",  # cmp necesita un registro primero
    ],
)
def test_errors_report_line(source):
    with pytest.raises(ExecutionError) as error:
        run_source("mov ecx, 1\n" + source)
    assert error.value.line == 2


def test_failed_step_keeps_eip_on_instruction():
    executor = Executor(parse("mov eax, 1\njmp noexiste"))
    executor.step()
    with pytest.raises(ExecutionError):
        executor.step()
    assert executor.cpu.eip == 1


# --- información para la interfaz -----------------------------------------


def test_last_jump_records_taken_and_not_taken():
    executor = Executor(parse("mov eax, 1\ncmp eax, 1\njne fin\nje fin\nfin: hlt"))
    assert executor.last_jump is None
    executor.run()
    assert executor.last_jump == Jump(line=4, mnemonic="je", target="fin", taken=True)


def test_last_jump_not_taken():
    executor = Executor(parse("cmp eax, 1\nje fin\nfin: hlt"))
    executor.run()
    assert executor.last_jump == Jump(line=2, mnemonic="je", target="fin", taken=False)


def test_steps_counts_executed_instructions():
    executor = Executor(parse("mov eax, 1\njmp fin\nmov eax, 2\nfin: hlt"))
    executor.run()
    assert executor.steps == 3
