Full changelog
==============

What's New in Pylint 2.7.4?
---------------------------
Release date: 2021-03-30


* Fix a problem with disabled msgid not being ignored

  Closes #4265

* Fix issue with annotated class constants

  Closes #4264


What's New in Pylint 2.7.3?
---------------------------
Release date: 2021-03-29

* Introduce logic for checking deprecated attributes in DeprecationMixin.

* Reduce usage of blacklist/whitelist terminology. Notably, ``extension-pkg-allow-list`` is an
  alternative to ``extension-pkg-whitelist`` and the message ``blacklisted-name`` is now emitted as
  ``disallowed-name``. The previous names are accepted to maintain backward compatibility.

* Move deprecated checker to ``DeprecatedMixin``

  Closes #4086

* Bump ``astroid`` version to ``2.5.2``

* Fix false positive for ``method-hidden`` when using private attribute and method

  Closes #3936

* ``use-symbolic-message-instead`` now also works on legacy messages like ``C0111`` (``missing-docstring``).

* Remove unwanted print to stdout from ``_emit_no_member``

* Introduce a command-line option to specify pyreverse output directory

  Closes #4159

* Fix issue with Enums and ``class-attribute-naming-style=snake_case``

  Closes #4149

* Add ``allowed-redefined-builtins`` option for fine tuning ``redefined-builtin`` check.

  Closes #3263

* Fix issue when executing with ``python -m pylint``

  Closes #4161

* Exempt ``typing.TypedDict`` from ``too-few-public-methods`` check.

  Closes #4180

* Fix false-positive ``no-member`` for typed annotations without default value.

  Closes #3167

* Add ``--class-const-naming-style`` for Enum constants and class variables annotated
  with ``typing.ClassVar``

  Closes #4181

* Fix astroid.Inference error for undefined-variables with ``len()```

  Closes #4215

* Fix column index on FIXME warning messages

  Closes #4218

* Improve handling of assignment expressions, better edge case handling

  Closes #3763, #4238

* Improve check if class is subscriptable PEP585

* Fix documentation and filename handling of --import-graph

* Fix false-positive for ``unused-import`` on class keyword arguments

  Closes #3202

* Fix regression with plugins on PYTHONPATH if latter is cwd

  Closes #4252


What's New in Pylint 2.7.2?
---------------------------
Release date: 2021-02-28

* Fix False Positive on ``Enum.__members__.items()``, ``Enum.__members__.values``, and ``Enum.__members__.keys``

  Closes #4123

* Properly strip dangerous sys.path entries (not just the first one)

  Closes #3636

* Workflow and packaging improvements


What's New in Pylint 2.7.1?
---------------------------
Release date: 2021-02-23

* Expose ``UnittestLinter`` in pylint.testutils

* Don't check directories starting with '.' when using register_plugins

  Closes #4119


What's New in Pylint 2.7.0?
---------------------------
Release date: 2021-02-21

* Introduce DeprecationMixin for reusable deprecation checks.

  Closes #4049

* Fix false positive for ``builtin-not-iterating`` when ``map`` receives iterable

  Closes #4078

* Python 3.6+ is now required.

* Fix false positive for ``builtin-not-iterating`` when ``zip`` receives iterable

* Add ``nan-comparison`` check for NaN comparisons

* Bug fix for empty-comment message line number.

  Closes #4009

* Only emit ``bad-reversed-sequence`` on dictionaries if below py3.8

  Closes #3940

* Handle class decorators applied to function.

  Closes #3882

* Add check for empty comments

* Fix minor documentation issue in contribute.rst

* Enums are now required to be named in UPPER_CASE by ``invalid-name``.

  Closes #3834

* Add missing checks for deprecated functions.

* Postponed evaluation of annotations are now recognized by default if python version is above 3.10

  Closes #3992

* Fix column metadata for anomalous backslash lints

* Drop support for Python 3.5

* Add support for pep585 with postponed evaluation

  Closes #3320

* Check alternative union syntax - PEP 604

  Closes #4065

* Fix multiple false positives with assignment expressions

  Closes #3347, #3953, #3865, #3275

* Fix TypedDict inherit-non-class false-positive Python 3.9+

  Closes #1927

* Fix issue with nested PEP 585 syntax

* Fix issue with nested PEP 604 syntax

* Fix a crash in ``undefined-variable`` caused by chained attributes in metaclass

  Closes #3742

* Fix false positive for ``not-async-context-manager`` when ``contextlib.asynccontextmanager`` is used

  Closes #3862

* Fix linter multiprocessing pool shutdown (triggered warnings when ran in parallels with other pytest plugins)

  Closes #3779

* Fix a false-positive emission of ``no-self-use`` and ``unused-argument`` for methods
  of generic structural types (`Protocol[T]`)

  Closes #3885

* Fix bug that lead to duplicate messages when using ``--jobs 2`` or more.

  Closes #3584

* Adds option ``check-protected-access-in-special-methods`` in the ClassChecker to activate/deactivate
  ``protected-access`` message emission for single underscore prefixed attribute in special methods.

  Closes #3120

* Fix vulnerable regular expressions in ``pyreverse``

  Closes #3811

* ``inconsistent-return-statements`` message is now emitted if one of ``try/except`` statement
  is not returning explicitly while the other do.

  Closes #3468

* Fix ``useless-super-delegation`` false positive when default keyword argument is a dictionary.

  Closes #3773

* Fix a crash when a specified config file does not exist

* Add support to ``ignored-argument-names`` in DocstringParameterChecker and adds ``useless-param-doc`` and ``useless-type-doc`` messages.

  Closes #3800

* Enforce docparams consistently when docstring is not present

  Closes #2738

* Fix ``duplicate-code`` false positive when lines only contain whitespace and non-alphanumeric characters (e.g. parentheses, bracket, comma, etc.)

* Improve lint message for ``singleton-comparison`` with bools

* Fix spell-checker crash on indented docstring lines that look like # comments

  Closes #3786

* Fix AttributeError in checkers/refactoring.py

* Improve sphinx directives spelling filter

* Fix a bug with postponed evaluation when using aliases for annotations.

  Closes #3798

* Fix minor documentation issues

* Improve the performance of the line length check.

* Removed incorrect deprecation of ``inspect.getfullargspec``

* Fix ``signature-differs`` false positive for functions with variadics

  Closes #3737

* Fix a crash in ``consider-using-enumerate`` when encountering ``range()`` without arguments

  Closes #3735

* ``len-as-conditions`` is now triggered only for classes that are inheriting directly from list, dict, or set and not implementing the ``__bool__`` function, or from generators like range or list/dict/set comprehension. This should reduce the false positives for other classes, like pandas's DataFrame or numpy's Array.

  Closes #1879

* Fixes duplicate-errors not working with -j2+

  Closes #3314

* ``generated-members`` now matches the qualified name of members

  Closes #2498

* Add check for bool function to ``len-as-condition``

* Add ``simplifiable-condition`` check for extraneous constants in conditionals using and/or.

* Add ``condition-evals-to-constant`` check for conditionals using and/or that evaluate to a constant.

  Closes #3407

* Changed setup.py to work with `distlib <https://pypi.org/project/distlib>`_

  Closes #3555

* New check: ``consider-using-generator``

  This check warns when a comprehension is used inside an ``any`` or ``all`` function,
  since it is unnecessary and should be replaced by a generator instead.
  Using a generator would be less code and way faster.

  Closes #3165

* Add Github Actions to replace Travis and AppVeyor in the future
