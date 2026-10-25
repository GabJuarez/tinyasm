# Estado actual

> Actualiza este archivo en el mismo PR en que cambies el estado de algo.

**Última actualización:** 2026-10-24 — Motor completo: executor terminado.

| Componente | Estado | Notas |
|---|---|---|
| `tokenizer.py` | ✅ Listo | Identificadores, números (`10`, `0x1F`, `1Fh`, `0b101`), símbolos y comentarios, con línea y columna |
| `parser.py` | ✅ Listo | Registros, inmediatos (incluidos negativos) y etiquetas; gramática en el docstring del módulo |
| `nodes.py` | ✅ Listo | |
| `evaluator.py` | ✅ Listo | `to_signed`, `add`, `sub` (también para `cmp`) con CF/ZF/SF/OF y `condition_met` con todos los `jcc` y sus alias |
| `machine.py` | ✅ Listo | 8 registros de 32 bits (se truncan a 32 bits sin signo), flags y EIP |
| `executor.py` | ✅ Listo | `step`/`run` con `max_steps`, todas las instrucciones y errores con número de línea |
| `isa.py` | ✅ Listo | Tabla de registros y sufijos de condición de los `jcc` |
| Interfaz (PyQt) | 🔲 Pendiente | Irá en `src/tinyasm/ui/` |

## Instrucciones

La referencia completa está en [instructions.md](instructions.md).

| Instrucción | Estado |
|---|---|
| `mov` | ✅ |
| `add`, `sub` | ✅ |
| `inc`, `dec` | ✅ |
| `cmp` | ✅ |
| `jmp` | ✅ |
| `je`/`jz`, `jne`/`jnz` | ✅ |
| `jg`, `jge`, `jl`, `jle` | ✅ |
| `ja`, `jae`, `jb`, `jbe` | ✅ |
| `js`, `jns`, `jo`, `jno`, `jc`, `jnc` | ✅ |
| `hlt` | ✅ |

Leyenda: ✅ listo · 🚧 en progreso · 🔲 pendiente
