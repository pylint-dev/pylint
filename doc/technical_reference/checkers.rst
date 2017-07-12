Checkers
--------
All of the default pylint checkers exist in ``pylint.checkers``.
This is where most of pylint's brains exist.
Most checkers are AST based and so use :mod:`astroid`.
``pylint.checkers.utils`` provides a large number of utility methods for
dealing with :mod:`astroid`.
