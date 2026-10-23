"""Jerarquía de errores del proyecto.

Cada etapa del pipeline lanza su propia subclase para que la UI
pueda mostrar en qué etapa y en qué línea falló el programa.
"""


class TinyAsmError(Exception):
    """Error base de tinyasm."""

    def __init__(self, message: str, line: int | None = None) -> None:
        self.message = message
        self.line = line
        prefix = f"línea {line}: " if line is not None else ""
        super().__init__(f"{prefix}{message}")


class TokenizeError(TinyAsmError):
    """El texto fuente contiene un carácter o literal inválido."""


class ParseError(TinyAsmError):
    """Los tokens no forman una instrucción válida."""


class ExecutionError(TinyAsmError):
    """Error en tiempo de ejecución (instrucción no soportada, etiqueta inexistente, etc.)."""
