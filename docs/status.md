# Estado actual

> Actualiza este archivo en el mismo PR en que cambies el estado de algo.

**Última actualización:** 2026-10-24 — Tokenizer y parser terminados.

| Componente | Estado | Notas |
|---|---|---|
| `tokenizer.py` | ✅ Listo | Identificadores, números (`10`, `0x1F`, `1Fh`, `0b101`), símbolos y comentarios, con línea y columna |
| `parser.py` | ✅ Listo | Registros, inmediatos (incluidos negativos) y etiquetas; gramática en el docstring del módulo |
| `nodes.py` | ✅ Listo | |
| `evaluator.py` | 🔲 Pendiente | `Flags` y `AluResult` definidos |
| `machine.py` | 🔲 Pendiente | 8 registros de 32 bits y flags |
| `executor.py` | 🔲 Pendiente | Falta el ciclo `step`/`run` y los handlers |
| `isa.py` | ✅ Listo | Tabla de registros |
| Interfaz (PyQt) | 🔲 Pendiente | Irá en `src/tinyasm/ui/` |

## Instrucciones

La referencia completa está en [instructions.md](instructions.md).

| Instrucción | Estado |
|---|---|
| `mov` | 🔲 |
| `add`, `sub` | 🔲 |
| `inc`, `dec` | 🔲 |
| `cmp` | 🔲 |
| `jmp` | 🔲 |
| `je`/`jz`, `jne`/`jnz` | 🔲 |
| `jg`, `jge`, `jl`, `jle` | 🔲 |
| `ja`, `jae`, `jb`, `jbe` | 🔲 |
| `js`, `jns`, `jo`, `jno`, `jc`, `jnc` | 🔲 |
| `hlt` | 🔲 |

Leyenda: ✅ listo · 🚧 en progreso · 🔲 pendiente
