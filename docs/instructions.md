# Instrucciones

Referencia de lo que tinyasm debe soportar. Operandos posibles: `reg` (uno de los 8
registros de 32 bits), `imm` (inmediato) y `label` (etiqueta).

## Instrucciones

| Instrucción | Operandos | Efecto | Flags |
|---|---|---|---|
| `mov dst, src` | `reg, reg` · `reg, imm` | `dst = src` | no cambia ninguna |
| `add dst, src` | `reg, reg` · `reg, imm` | `dst = dst + src` | CF, ZF, SF, OF |
| `sub dst, src` | `reg, reg` · `reg, imm` | `dst = dst - src` | CF, ZF, SF, OF |
| `inc dst` | `reg` | `dst = dst + 1` | ZF, SF, OF — **CF no cambia** |
| `dec dst` | `reg` | `dst = dst - 1` | ZF, SF, OF — **CF no cambia** |
| `cmp a, b` | `reg, reg` · `reg, imm` | calcula `a - b` y **descarta el resultado** | CF, ZF, SF, OF (igual que `sub`) |
| `jmp label` | `label` | salta siempre | no cambia ninguna |
| `jcc label` | `label` | salta si se cumple la condición (tabla de abajo) | no cambia ninguna |
| `hlt` | — | detiene la ejecución | — |

El programa también termina si EIP pasa la última instrucción.

## Flags

| Flag | Se enciende cuando... |
|---|---|
| **CF** (carry) | la operación **sin signo** se desborda: en `add`, el resultado no cabe en 32 bits; en `sub`/`cmp`, `a < b` sin signo (hubo préstamo) |
| **ZF** (zero) | el resultado es 0 |
| **SF** (sign) | el bit 31 del resultado es 1 (negativo si se interpreta con signo) |
| **OF** (overflow) | la operación **con signo** se desborda, p. ej. `0x7FFFFFFF + 1` |

## Saltos condicionales

| Instrucción | Alias | Salta si | Uso típico después de `cmp a, b` |
|---|---|---|---|
| `je` | `jz` | ZF = 1 | `a == b` |
| `jne` | `jnz` | ZF = 0 | `a != b` |
| `jg` | `jnle` | ZF = 0 y SF = OF | `a > b` con signo |
| `jge` | `jnl` | SF = OF | `a >= b` con signo |
| `jl` | `jnge` | SF ≠ OF | `a < b` con signo |
| `jle` | `jng` | ZF = 1 o SF ≠ OF | `a <= b` con signo |
| `ja` | `jnbe` | CF = 0 y ZF = 0 | `a > b` sin signo |
| `jae` | `jnb`, `jnc` | CF = 0 | `a >= b` sin signo |
| `jb` | `jnae`, `jc` | CF = 1 | `a < b` sin signo |
| `jbe` | `jna` | CF = 1 o ZF = 1 | `a <= b` sin signo |
| `js` | — | SF = 1 | resultado negativo |
| `jns` | — | SF = 0 | resultado no negativo |
| `jo` | — | OF = 1 | hubo overflow con signo |
| `jno` | — | OF = 0 | no hubo overflow con signo |

En `evaluator.condition_met(condition, flags)`, `condition` es el sufijo sin la `j`
(`"e"`, `"nz"`, `"ge"`...). Los alias deben dar el mismo resultado que su instrucción principal.

### Con signo vs. sin signo

Con `eax = -1` (`0xFFFFFFFF`) y `ebx = 1`, después de `cmp eax, ebx`:

- `jg` **no** salta: con signo, `-1 > 1` es falso.
- `ja` **sí** salta: sin signo, `0xFFFFFFFF > 1` es verdadero.
