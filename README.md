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

## Ejemplos

En [`examples/`](examples) hay programas cortos para ver cómo `cmp` y las operaciones cambian
las flags y cómo cada salto las usa. Se abren desde el menú **Ejemplos** de la interfaz.

| Archivo | Qué muestra |
|---|---|
| `01_jmp.asm` | `jmp`: salta siempre, sin mirar flags |
| `02_je_jne.asm` | `je` / `jne` y ZF |
| `03_jl_jg_con_signo.asm` | comparación con signo: `jl` / `jg` con SF y OF |
| `04_jb_ja_sin_signo.asm` | comparación sin signo: `jb` / `ja` con CF y ZF |
| `05_jg_vs_ja.asm` | el mismo `cmp` con `-1` y `1`: `jg` no salta, `ja` sí |
| `06_jc_jo_js.asm` | CF, OF y SF encendidos por `add`, con `jc`, `jo` y `js` |
| `sum_loop.asm` | un ciclo completo: suma de 1 a 10 con `jne` |

## Arquitectura

`Tokenizer → Parser → Executor ⇄ Evaluator`, con la interfaz encima: ver [docs/architecture.md](docs/architecture.md).

## Documentación
- [Arquitectura](docs/architecture.md)
- [Instrucciones](docs/instructions.md)
- [Roadmap y alcance](docs/roadmap.md)
- [Estado actual](docs/status.md)
- [Convenciones](docs/conventions.md)
