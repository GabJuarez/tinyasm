"""Abre la interfaz: ``uv run python -m tinyasm``."""

try:
    from tinyasm.ui import main
except ModuleNotFoundError as error:
    if error.name is None or not error.name.startswith("PyQt6"):
        raise
    raise SystemExit("La interfaz necesita PyQt6. Instálalo con: uv sync --extra ui") from None

main()
