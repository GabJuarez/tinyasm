# tinyasm

Evaluador de un subconjunto de **x86 de 32 bits (IA-32)** con sintaxis Intel, escrito en Python.
Proyecto de Arquitectura de Computadoras.

```asm
        mov ecx, 10
        mov eax, 0
loop_start:
        add eax, ecx
        sub ecx, 1
        cmp ecx, 0
        jne loop_start
```

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

Desde Python:

```python
from tinyasm import run_source

cpu = run_source(open("examples/sum_loop.asm").read())
print(cpu.registers["eax"])
```

## Arquitectura

`Tokenizer → Parser → Executor ⇄ Evaluator`: ver [docs/architecture.md](docs/architecture.md).

## Documentación
- [Arquitectura](docs/architecture.md)
- [Roadmap](docs/roadmap.md)
- [Estado actual](docs/status.md)
- [Convenciones](docs/conventions.md)
- [Cómo contribuir](CONTRIBUTING.md)
