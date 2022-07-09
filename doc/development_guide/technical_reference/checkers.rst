Checkers
--------
All of the default Pylint checkers exist in ``pylint.checkers``.
This is where most of Pylint's brains exist.
Most checkers are AST based and so use ``astroid``.
``pylint.checkers.utils`` provides a large number of utility methods for
dealing with ``astroid``.
