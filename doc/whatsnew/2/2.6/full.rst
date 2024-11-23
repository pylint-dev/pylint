Full changelog
==============

What's New in Pylint 2.6.1?
---------------------------
Release date: 2021-02-16

* Astroid version has been set as < 2.5

  Closes #4093


What's New in Pylint 2.6.0?
---------------------------
Release date: 2020-08-20

* Fix various scope-related bugs in ``undefined-variable`` checker

  Closes #1082, #3434, #3461

* bad-continuation and bad-whitespace have been removed, black or another formatter can help you with this better than Pylint

  Closes #246, #289, #638, #747, #1148, #1179, #1943, #2041, #2301, #2304, #2944, #3565

* The no-space-check option has been removed. It's no longer possible to consider empty line like a ``trailing-whitespace`` by using clever options

  Closes #1368

* ``missing-kwoa`` is no longer emitted when dealing with overload functions

  Closes #3655

* mixed-indentation has been removed, it is no longer useful since TabError is included directly in python3

  Closes #2984 #3573

* Add ``super-with-arguments`` check for flagging instances of Python 2 style super calls.

* Add an faq detailing which messages to disable to avoid duplicates w/ other popular linters

* Fix superfluous-parens false-positive for the walrus operator

  Closes #3383

* Fix ``fail-under`` not accepting floats

* Fix a bug with ``ignore-docstrings`` ignoring all lines in a module

* Fix ``pre-commit`` config that could lead to undetected duplicate lines of code

* Fix a crash in parallel mode when the module's filepath is not set

  Closes #3564

* Add ``raise-missing-from`` check for exceptions that should have a cause.

* Support both isort 4 and isort 5. If you have pinned isort 4 in your project requirements, nothing changes. If you use isort 5, though, note that the ``known-standard-library`` option is not interpreted the same in isort 4 and isort 5 (see the migration guide in isort documentation for further details). For compatibility's sake for most pylint users, the ``known-standard-library`` option in pylint now maps to ``extra-standard-library`` in isort 5. If you really want what ``known-standard-library`` now means in isort 5, you must disable the ``wrong-import-order`` check in pylint and run isort manually with a proper isort configuration file.

  Closes #3722

* Fix a crash caused by not guarding against ``InferenceError`` when calling ``infer_call_result``

  Closes #3690

* Fix a crash in parallel mode when the module's filepath is not set

  Closes #3564
