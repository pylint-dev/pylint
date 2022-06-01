:Release: 2.2
:Date: 2018-11-25

Summary -- Release highlights
=============================


New checkers
============

* String checker now reports format string type mismatches.

* ``duplicate-string-formatting-argument`` was added for detecting duplicate string
  formatting arguments that should be passed instead as named arguments.

* ``logging-format-style`` is a new option for the logging checker for usage of
  str.format() style format strings in calls to loggers.

  It accepts two options: ``--logging-format-style=old`` for using `%` style formatting,
  which is the assumed default, and ``--logging-format-style=new`` for using `{}` style formatting.

* ``implicit-str-concat-in-sequence`` detects string concatenation inside lists, sets & tuples.

  Example of code that would generate such warning:

  .. code-block:: python

    woops = ('a', 'b' 'c')


Other Changes
=============

* ``try-except-raise`` checker now handles multilevel inheritance hirerachy for exceptions correctly.

  Closes #2484

* Ignore import x.y.z as z cases for checker ``useless-import-alias``.

* ``unnecessary-pass`` is now also emitted when a function or class contains only docstring and pass statement,
  in which case, docstring is enough for empty definition.

* Fix false positive ``undefined-variable`` and ``used-before-assignment`` with nonlocal keyword usage.

* Fix exceptions being raised when one of the params is not a ClassDef for ``checkers.utils.is_subclass_of``.

* ``pylint`` now picks the latest value from the inferred values of the exception that gets
  raised, when looking for ``raising-non-exception``. This helps when reusing a variable name
  for multiple types, since ``pylint`` was picking just the first inferred value, leading
  to spurious false positives.

  Closes #2431

* ``pylint`` used to emit a ``not-an-iterable`` error when looking at coroutines built
  with ``asyncio.coroutine``. This is no longer the case as we handle coroutines explicitly.

  Closes #996

* ``pylint`` used to emit an ``unused-variable`` error if unused import was found in the function. Now instead of
  ``unused-variable``, ``unused-import`` is emitted.

  Closes #2421
