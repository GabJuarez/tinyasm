# Roadmap

**Objetivo final:** cargar un programa en un subconjunto de IA-32 con sintaxis Intel,
ejecutarlo paso a paso y visualizar registros, flags y memoria en una UI de escritorio (PyQt).

## Fase 0 — Scaffolding ✅
- [x] Proyecto con uv, ruff y pytest
- [x] Estructura Tokenizer → Parser → Evaluator → Executor con interfaces definidas
- [x] Pruebas de contrato (`xfail`) para cada etapa
- [x] Documentación inicial

## Fase 1 — Pipeline mínimo (`mov`, `add`, `sub`)
- [ ] Tokenizer: identificadores, números (dec/hex/bin), símbolos, comentarios
- [ ] Parser: registros, inmediatos, etiquetas
- [ ] Parser: operandos de memoria `[base + index*escala ± desplazamiento]` y `dword ptr`
- [ ] Evaluator: `to_signed`, `add`, `sub` con CF/ZF/SF/OF
- [ ] Machine: lectura/escritura de subregistros (`ax`, `al`, `ah`) y memoria little-endian
- [ ] Executor: `step`, `run`, resolución de operandos, `mov`, `add`, `sub`
- [ ] Prueba que ejecute los programas de `examples/`

## Fase 2 — Control de flujo
- [ ] `cmp`, `jmp`
- [ ] Saltos condicionales: `je/jz`, `jne/jnz`, `jg`, `jge`, `jl`, `jle`, `ja`, `jae`, `jb`, `jbe`
- [ ] `hlt` y fin de programa
- [ ] Protección contra ciclos infinitos (`max_steps`)

## Fase 3 — Más instrucciones
- [ ] Lógicas: `and`, `or`, `xor`, `not`, `test`
- [ ] `inc`, `dec`, `neg`
- [ ] Corrimientos: `shl`, `shr`, `sar`, `rol`, `ror`
- [ ] `mul`, `imul`, `div`, `idiv` (con `edx:eax`)
- [ ] Pila: `push`, `pop`, `call`, `ret`
- [ ] Flags PF y AF

## Fase 4 — UI en PyQt
- [ ] Editor de código con resaltado de la línea actual
- [ ] Botones ejecutar / paso a paso / reiniciar
- [ ] Paneles de registros, flags y memoria
- [ ] Errores mostrados en la línea correspondiente

## Ideas a futuro
- Secciones `.data` / `.text` y directivas `db`, `dw`, `dd`
- Etiquetas como direcciones de memoria (`mov eax, [var]`)
- Historial para "deshacer paso"
