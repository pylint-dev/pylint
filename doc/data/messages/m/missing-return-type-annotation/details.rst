Type annotations improve code readability and enable better static analysis. This check
ensures that all functions and methods have return type annotations, making the code's
intent clearer and allowing type checkers like mypy to verify correctness.

This check is opt-in (disabled by default) to maintain backward compatibility. Enable it
with ``--enable=missing-return-type-annotation``.

The check automatically skips:

- ``__init__`` methods (which implicitly return None)
- Abstract methods (``@abstractmethod``, ``@abstractproperty``)
- Properties and their setters/deleters
- Overload stub definitions (``@typing.overload``)
