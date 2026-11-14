Module-level dunder names such as ``__version__`` and ``__author__`` should be
placed after the module docstring and any ``__future__`` imports, but before
regular imports. This makes important module metadata easy to find and follows
the ordering recommended by PEP 8.

If a dunder assignment depends on an imported name, it may remain after that
import and this message is not emitted.
