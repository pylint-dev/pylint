:Release: 2.6
:Date: 2020-08-20

Summary -- Release highlights
=============================

* ``bad-continuation`` and ``bad-whitespace`` have been removed. ``black`` or another formatter can help you with this better than Pylint
* Added support for isort 5

New checkers
============

* Add ``super-with-arguments`` check for flagging instances of Python 2 style super calls.

* Add ``raise-missing-from`` check for exceptions that should have a cause.

Other Changes
=============

* ``bad-continuation`` and ``bad-whitespace`` have been removed. ``black`` or another formatter can help you with this better than Pylint

* The ``no-space-check`` option has been removed, it's no longer possible to consider empty line like a ``trailing-whitespace`` by using clever options.

* ``mixed-indentation`` has been removed, it is no longer useful since TabError is included directly in python3

* Fix superfluous-parens false-positive for the walrus operator

* Add support for both isort 4 and isort 5. If you have pinned isort 4 in your project requirements, nothing changes. If you use isort 5, though, note that the ``known-standard-library`` option is not interpreted the same in isort 4 and isort 5 (see `the migration guide in isort documentation` (no longer available) for further details). For compatibility's sake for most pylint users, the ``known-standard-library`` option in pylint now maps to ``extra-standard-library`` in isort 5. If you really want what ``known-standard-library`` now means in isort 5, you must disable the ``wrong-import-order`` check in pylint and run isort manually with a proper isort configuration file.
