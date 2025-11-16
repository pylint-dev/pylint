Type annotations improve code readability and enable better static analysis. This check
ensures that all function and method parameters have type annotations, making the expected
types clear and allowing type checkers like mypy to verify correct usage.

This check is opt-in (disabled by default) to maintain backward compatibility. Enable it
with ``--enable=missing-param-type-annotation``.

The check automatically skips:

- ``self`` and ``cls`` parameters in methods
- Parameters in abstract methods (``@abstractmethod``, ``@abstractproperty``)
- Parameters in overload stub definitions (``@typing.overload``)

All parameter types are checked, including:

- Regular positional parameters
- Positional-only parameters (before ``/``)
- Keyword-only parameters (after ``*``)
- Variadic positional parameters (``*args``)
- Variadic keyword parameters (``**kwargs``)
