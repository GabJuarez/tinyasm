# tinyasm

Emulador de un subconjunto de **x86 de 32 bits (IA-32)** con sintaxis Intel, escrito en Python.
Proyecto de Arquitectura de Computadoras.

El foco es **evaluar `cmp`, `jmp` y los saltos condicionales (`jcc`)**: ejecutar el programa
paso a paso en una interfaz de escritorio (PyQt) y ver cómo cambian los registros, las flags
y el flujo del programa.

```asm
; Suma 10 + 9 + ... + 1 en EAX.
        mov ecx, 10
        mov eax, 0
loop_start:
        add eax, ecx
        dec ecx
        cmp ecx, 0
        jg loop_start
        hlt
```

## Qué soporta

- Los 8 registros de 32 bits (`eax`, `ebx`, `ecx`, `edx`, `esi`, `edi`, `esp`, `ebp`) y las flags CF, ZF, SF, OF.
- `mov`, `add`, `sub`, `inc`, `dec`, `cmp`, `jmp`, `hlt`.
- Todos los saltos condicionales: `je`, `jne`, `jg`, `jge`, `jl`, `jle`, `ja`, `jae`, `jb`, `jbe`, `js`, `jns`, `jo`, `jno` y sus alias.
- Etiquetas, comentarios con `;` y números en decimal, hexadecimal (`0x1F`, `1Fh`) y binario (`0b101`).

Detalle de cada instrucción y de qué flags revisa cada salto: [docs/instructions.md](docs/instructions.md).
Lo que queda fuera (memoria, pila, directivas...): [docs/roadmap.md](docs/roadmap.md#fuera-de-alcance).

## Requisitos
- [uv](https://docs.astral.sh/uv/) (`brew install uv` o `curl -LsSf https://astral.sh/uv/install.sh | sh`)

uv instala por su cuenta la versión de Python correcta (3.12+).

## Uso rápido

```bash
git clone https://github.com/GabJuarez/tinyasm.git
cd tinyasm
uv sync          # crea .venv e instala todo
uv run pytest    # pruebas
```

La interfaz está en desarrollo (ver [estado](docs/status.md)). Mientras tanto, el motor se
puede usar desde Python:

```python
from tinyasm import run_source

cpu = run_source(open("examples/sum_loop.asm").read())
print(cpu.registers["eax"], cpu.flags)
```

## Arquitectura

`Tokenizer → Parser → Executor ⇄ Evaluator`, con la interfaz encima: ver [docs/architecture.md](docs/architecture.md).

## Documentación
- [Arquitectura](docs/architecture.md)
- [Instrucciones](docs/instructions.md)
- [Roadmap y alcance](docs/roadmap.md)
- [Estado actual](docs/status.md)
- [Convenciones](docs/conventions.md)
- [Cómo contribuir](CONTRIBUTING.md)
