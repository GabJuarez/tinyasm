# Roadmap

**Objetivo:** un emulador de un subconjunto de IA-32 (sintaxis Intel) cuyo foco es **evaluar
`cmp`, `jmp` y los saltos condicionales (`jcc`)**, con una interfaz en PyQt para ejecutar el
programa paso a paso y ver cómo cambian los registros, las flags y el flujo.

Plazo: una semana desde la asignación. Por eso el alcance está recortado a lo necesario para
que `cmp` / `jcc` / `jmp` funcionen y se puedan mostrar.

## Fase 0 — Scaffolding ✅
- [x] Proyecto con uv, ruff y pytest
- [x] Estructura Tokenizer → Parser → Evaluator → Executor con interfaces definidas
- [x] Pruebas de contrato (`xfail`) para cada etapa
- [x] Documentación inicial

## Fase 1 — Motor
- [x] Tokenizer: identificadores, números (dec/hex/bin), símbolos, comentarios
- [x] Parser: registros, inmediatos (incluidos negativos) y etiquetas
- [x] Evaluator: `to_signed`, `add`, `sub` con CF/ZF/SF/OF
- [x] Evaluator: `condition_met` con todos los `jcc` de [instructions.md](instructions.md)
- [x] Machine: los 8 registros de 32 bits y las flags
- [x] Executor: `step`, `run` y protección contra ciclos infinitos (`max_steps`)
- [x] Executor: `mov`, `add`, `sub`, `inc`, `dec`
- [x] Executor: `cmp`, `jmp`, `jcc`, `hlt`

## Fase 2 — Interfaz (PyQt)
- [ ] Editor de código con la línea actual resaltada
- [ ] Botones ejecutar / paso a paso / reiniciar
- [ ] Panel de registros (hexadecimal y decimal con signo)
- [ ] Panel de flags (CF, ZF, SF, OF)
- [ ] Indicador de si el último salto se tomó o no, y a qué etiqueta
- [ ] Errores mostrados en la línea correspondiente

## Fase 3 — Entrega
- [ ] Programas de ejemplo en `examples/` que cubran cada familia de `jcc`
- [ ] Ejemplo que muestre la diferencia entre comparación con signo y sin signo (`jg` vs `ja`)
- [ ] README con instrucciones para abrir la interfaz

## Fuera de alcance
Decidido para que entre en el plazo; se puede retomar si sobra tiempo:

- Operandos de memoria (`[ebx + 4]`, `dword ptr`) y memoria en general
- Subregistros de 16 y 8 bits (`ax`, `al`, `ah`)
- Secciones `.data` / `.text` y directivas (`db`, `dw`, `dd`)
- Pila: `push`, `pop`, `call`, `ret`
- `mul`, `div`, lógicas (`and`, `or`, `xor`, `test`) y corrimientos
- Flags PF y AF
