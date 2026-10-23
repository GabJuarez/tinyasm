# Cómo contribuir

## Configuración inicial (una sola vez)

```bash
brew install uv            # o: curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/GabJuarez/tinyasm.git
cd tinyasm
uv sync
```

No hace falta activar el entorno virtual: `uv run <comando>` lo usa automáticamente.

## Flujo de trabajo

1. Elige una tarea de [docs/roadmap.md](docs/roadmap.md) (o un issue) y avisa al equipo para no duplicar trabajo.
2. Crea una rama desde `main` actualizado:
   ```bash
   git switch main && git pull
   git switch -c feat/tokenizer-numbers
   ```
3. Programa y agrega pruebas.
4. Antes de hacer commit:
   ```bash
   uv run ruff format .
   uv run ruff check --fix .
   uv run pytest
   ```
5. Haz push y abre un Pull Request. Otro integrante lo revisa antes del merge.

## Comandos de uv útiles

| Quiero... | Comando |
|---|---|
| Instalar o actualizar el entorno según `uv.lock` | `uv sync` |
| Agregar una dependencia | `uv add <paquete>` |
| Agregar una dependencia de desarrollo | `uv add --dev <paquete>` |
| Correr algo dentro del entorno | `uv run <comando>` |

Si cambias dependencias, incluye `pyproject.toml` **y** `uv.lock` en el commit.

Lee también [docs/conventions.md](docs/conventions.md) (idioma, estilo y cómo agregar instrucciones).
