# Convenciones

## Idioma
- **Código en inglés:** nombres de módulos, clases, funciones y variables.
- **Comentarios y docstrings en español.**
- **Mensajes al usuario en español** (errores).
- ruff **no** revisa ortografía. Las reglas `RUF001-003` (caracteres "ambiguos" como acentos) están desactivadas en `pyproject.toml`. Si usan la extensión *Code Spell Checker* de VS Code, desactívenla para este proyecto o agreguen el diccionario de español.

## Estilo
- Formato y lint con **ruff** (`uv run ruff format .` y `uv run ruff check .`); línea máxima de 100.
- Anotaciones de tipo en todas las funciones públicas; sintaxis moderna (`int | None`, `list[int]`).
- Datos inmutables con `@dataclass(frozen=True, slots=True)`.
- Registros y mnemónicos se normalizan a **minúsculas** en el parser.
- Valores de registros y memoria se guardan **sin signo** (`0 <= v < 2**bits`). Para interpretarlos con signo, usar `evaluator.to_signed`.

## Reglas de arquitectura
- El **Evaluator** es puro: no importa `machine`, `executor`, `nodes` ni `tokenizer`.
- Sólo el **Executor** modifica la `CPU`.
- Cada etapa lanza su propio error (`TokenizeError`, `ParseError`, `ExecutionError`) **con número de línea**.

## Cómo agregar una instrucción
1. Si necesita un cálculo, agrega una función pura en `evaluator.py` con sus pruebas en `tests/test_evaluator.py`.
2. Agrega `_op_<mnemonic>(self, instruction)` en `Executor` y regístralo en `_handlers`.
3. Agrega una prueba de extremo a extremo en `tests/test_executor.py`.
4. Actualiza la tabla de instrucciones en [`status.md`](status.md) y marca la casilla en [`roadmap.md`](roadmap.md).

## Pruebas
- Cada función pública lleva pruebas.
- Las pruebas de etapas pendientes están marcadas con `xfail(strict=True)`. Cuando implementes la etapa, **quita el `pytestmark`** del archivo: si no lo quitas, pytest falla precisamente para recordártelo.

## Git
- Rama `main` protegida por convención: todo entra por Pull Request con al menos una revisión.
- Ramas: `feat/<tema>`, `fix/<tema>`, `docs/<tema>`, `refactor/<tema>`, `test/<tema>`.
- Commits con [Conventional Commits](https://www.conventionalcommits.org/es/): `feat(parser): soportar operandos de memoria`.
- Antes de abrir el PR, `uv run ruff check .` y `uv run pytest` deben pasar en local.
