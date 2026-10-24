# Estado actual

> Actualiza este archivo en el mismo PR en que cambies el estado de algo.

**Última actualización:** 2026-10-24 — Tokenizer terminado (Fase 1 en progreso).

| Componente | Estado | Notas |
|---|---|---|
| `tokenizer.py` | ✅ Listo | Identificadores, números (`10`, `0x1F`, `1Fh`, `0b101`), símbolos y comentarios, con línea y columna |
| `parser.py` | 🔲 Pendiente | Gramática documentada en el docstring del módulo |
| `nodes.py` | ✅ Listo | Puede crecer según se necesite |
| `evaluator.py` | 🔲 Pendiente | `Flags` y `AluResult` definidos |
| `machine.py` | 🔲 Pendiente | Faltan subregistros y memoria |
| `executor.py` | 🔲 Pendiente | Falta el ciclo `step`/`run` y los handlers |
| `isa.py` | ✅ Listo | Tabla de registros de 32/16/8 bits |

## Instrucciones soportadas

Ninguna todavía. Agrega aquí cada instrucción conforme se implemente:

| Instrucción | Operandos | Flags que afecta |
|---|---|---|
| — | — | — |

Leyenda: ✅ listo · 🚧 en progreso · 🔲 pendiente
