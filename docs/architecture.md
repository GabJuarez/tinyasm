# Arquitectura

```
texto .asm ──► Tokenizer ──► Parser ──► Executor ◄──► Evaluator
                (tokens)   (Program)       │        (funciones puras)
                                           ▼
                                      CPU (estado)
```

| Etapa | Módulo | Entrada → Salida | Puede fallar con |
|---|---|---|---|
| Tokenizer | `tokenizer.py` | `str` → `list[Token]` | `TokenizeError` |
| Parser | `parser.py` | `list[Token]` → `Program` | `ParseError` |
| Evaluator | `evaluator.py` | enteros / `Flags` → `AluResult`, `bool`, `int` | — |
| Executor | `executor.py` | `Program` + `CPU` → `CPU` mutada | `ExecutionError` |

Módulos de apoyo:

- `nodes.py`: nodos inmutables del programa (`Instruction`, `Register`, `Immediate`, `Memory`, `LabelRef`, `Program`).
- `machine.py`: `CPU` y `Memory`, el **único estado mutable**.
- `isa.py`: tablas estáticas de IA-32 (registros, subregistros, tamaños).
- `errors.py`: jerarquía de errores; todos llevan número de línea.

La interfaz de usuario (PyQt) consumirá directamente `run_source` / `Executor` (ver roadmap).

## Frontera Evaluator / Executor

La regla para decidir dónde va algo:

> **¿Es una pregunta con respuesta?** → Evaluator.
> **¿Es una decisión de flujo o una mutación de estado?** → Executor.

| Ejemplo | Dónde | Por qué |
|---|---|---|
| ¿Cuánto da `a + b` en 32 bits y qué flags deja? | Evaluator (`add`) | cálculo puro |
| ¿Se cumple `jg` con estas flags? | Evaluator (`condition_met`) | pregunta con respuesta booleana |
| Leer `ebx`, calcular `[ebx+4]`, leer memoria | Executor | resolver operandos usa el estado |
| Escribir el resultado en `eax` y actualizar flags | Executor | mutación |
| Saltar a `loop_start` si `condition_met` es verdadero | Executor | decisión de flujo |

El Evaluator **nunca** recibe tokens, nodos ni la `CPU`: sólo números y `Flags`.
Por eso se puede probar sin parsear nada.

## Decisiones de diseño

- **EIP es un índice de instrucción**, no una dirección en bytes. No ensamblamos a código máquina, así que no conocemos el tamaño real de cada instrucción.
- **Memoria dispersa** (`dict[int, int]` por byte, little-endian): sólo existe lo que se escribe.
- **Una instrucción por línea**, con etiquetas opcionales antes.
- **Nodos inmutables** (`frozen=True`): el programa no cambia durante la ejecución, lo que facilita el "paso a paso" en la futura UI.
- **Sin dependencias en tiempo de ejecución** por ahora; PyQt se agregará como dependencia opcional cuando empiece la UI.
