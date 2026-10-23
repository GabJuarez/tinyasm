"""tinyasm: evaluador de un subconjunto de IA-32 (x86 de 32 bits) con sintaxis Intel.

Pipeline: Tokenizer -> Parser -> Executor (que consulta al Evaluator).
"""

from tinyasm.executor import Executor, run_source
from tinyasm.machine import CPU
from tinyasm.parser import parse
from tinyasm.tokenizer import tokenize

__all__ = ["CPU", "Executor", "parse", "run_source", "tokenize"]
__version__ = "0.1.0"
