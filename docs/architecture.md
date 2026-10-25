# Arquitectura

```
texto .asm ──► Tokenizer ──► Parser ──► Executor ◄──► Evaluator
                (tokens)   (Program)       │        (funciones puras)
                                           ▼
                                      CPU (estado) ──► UI (PyQt)
```

| Etapa | Módulo | Entrada → Salida | Puede fallar con |
|---|---|---|---|
| Tokenizer | `tokenizer.py` | `str` → `list[Token]` | `TokenizeError` |
| Parser | `parser.py` | `list[Token]` → `Program` | `ParseError` |
| Evaluator | `evaluator.py` | enteros / `Flags` → `AluResult`, `bool`, `int` | — |
| Executor | `executor.py` | `Program` + `CPU` → `CPU` mutada | `ExecutionError` |

Módulos de apoyo:

- `nodes.py`: nodos inmutables del programa (`Instruction`, `Register`, `Immediate`, `LabelRef`, `Program`).
- `machine.py`: `CPU` (registros, flags, EIP), el **único estado mutable**.
- `isa.py`: tablas estáticas de IA-32 (registros).
- `errors.py`: jerarquía de errores; todos llevan número de línea.

## Interfaz

La UI vive en el subpaquete `src/tinyasm/ui/` y PyQt6 es una dependencia opcional (extra `ui`),
para que quien solo trabaje en el motor no tenga que instalarlo. Se abre con
`uv run python -m tinyasm` (`src/tinyasm/__main__.py`).

| Archivo | Qué hace |
|---|---|
| `ui/main_window.py` | `MainWindow`: la única pieza que tiene el `Executor`; parsea, llama a `step()`/`run()` y reparte el estado |
| `ui/editor.py` | `CodeEditor`: números de línea, línea actual (amarillo) y línea con error (rojo); `AsmHighlighter` colorea la sintaxis usando el tokenizer del proyecto |
| `ui/panels.py` | Paneles de sólo lectura: registros, flags y último salto |
| `ui/fonts.py` | Tamaño de letra de la interfaz y fuente monoespaciada |


- La UI **solo consume** el motor: crea un `Executor`, llama a `step()` o `run()` y pinta
  `executor.cpu.registers`, `executor.cpu.flags` y `executor.cpu.eip`.
- El motor **nunca** importa nada de `ui`.
- Un `src/tinyasm/__main__.py` abrirá la ventana con `uv run python -m tinyasm`.

## Frontera Evaluator / Executor

La regla para decidir dónde va algo:

> **¿Es una pregunta con respuesta?** → Evaluator.
> **¿Es una decisión de flujo o una mutación de estado?** → Executor.

| Ejemplo | Dónde | Por qué |
|---|---|---|
| ¿Cuánto da `a - b` en 32 bits y qué flags deja? | Evaluator (`sub`) | cálculo puro |
| ¿Se cumple `jg` con estas flags? | Evaluator (`condition_met`) | pregunta con respuesta booleana |
| Leer el valor de `ebx` para usarlo como operando | Executor | resolver operandos usa el estado |
| Guardar las flags que devolvió `sub` al ejecutar `cmp` | Executor | mutación |
| Cambiar EIP a `loop_start` si `condition_met` es verdadero | Executor | decisión de flujo |

El Evaluator **nunca** recibe tokens, nodos ni la `CPU`: sólo números y `Flags`.
Por eso se puede probar sin parsear nada.

### Ejemplo: cómo se ejecuta `cmp eax, 5` seguido de `jl menor`

1. El executor lee `eax` de la CPU (digamos que vale 3).
2. Llama a `evaluator.sub(3, 5)` → resultado `0xFFFFFFFE` con SF = 1, OF = 0, CF = 1, ZF = 0.
3. Como es `cmp`, descarta el resultado y solo guarda las flags en la CPU.
4. En `jl menor`, llama a `evaluator.condition_met("l", flags)` → SF ≠ OF → `True`.
5. Busca `menor` en `program.labels` y pone ese índice en EIP.

## Decisiones de diseño

- **EIP es un índice de instrucción**, no una dirección en bytes. No ensamblamos a código máquina, así que no conocemos el tamaño real de cada instrucción.
- **Solo registros de 32 bits**, sin memoria: todos los operandos son registros, inmediatos o etiquetas (ver [roadmap.md](roadmap.md#fuera-de-alcance)).
- **Valores sin signo en los registros** (`0 <= v < 2**32`); con signo solo al interpretarlos (`to_signed`).
- **Una instrucción por línea**, con etiquetas opcionales antes.
- **Nodos inmutables** (`frozen=True`): el programa no cambia durante la ejecución, lo que facilita el paso a paso en la UI.
