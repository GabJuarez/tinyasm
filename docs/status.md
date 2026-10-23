# Estado actual

> Actualiza este archivo en el mismo PR en que cambies el estado de algo.

**Última actualización:** 2026-10-22 — Fase 0 (scaffolding) terminada.

| Componente | Estado | Notas |
|---|---|---|
| `tokenizer.py` | 🔲 Pendiente | `Token`/`TokenType` definidos; faltan `tokenize` y `parse_number` |
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
