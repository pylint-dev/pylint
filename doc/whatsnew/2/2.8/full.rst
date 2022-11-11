Full changelog
==============

What's New in Pylint 2.8.3?
---------------------------
Release date: 2021-05-31

* Astroid has been pinned to 2.5.6 for the 2.8 branch.

  Refs #4527


What's New in Pylint 2.8.2?
---------------------------
Release date: 2021-04-26

* Keep ``__pkginfo__.numversion`` a tuple to avoid breaking pylint-django.

  Closes #4405

* scm_setuptools has been added to the packaging.

* Pylint's tags are now the standard form ``vX.Y.Z`` and not ``pylint-X.Y.Z`` anymore.

* New warning message ``deprecated-class``. This message is emitted if import or call deprecated class of the
  standard library (like ``collections.Iterable`` that will be removed in Python 3.10).

  Closes #4388


What's New in Pylint 2.8.1?
---------------------------
Release date: 2021-04-25

* Add numversion back (temporarily) in ``__pkginfo__`` because it broke Pylama and revert the unnecessary
  ``pylint.version`` breaking change.

  Closes #4399


What's New in Pylint 2.8.0?
---------------------------
Release date: 2021-04-24

* New refactoring message ``consider-using-with``. This message is emitted if resource-allocating functions or methods of the
  standard library (like ``open()`` or ``threading.Lock.acquire()``) that can be used as a context manager are called without
  a ``with`` block.

  Closes #3413

* Resolve false positives on unused variables in decorator functions

  Closes #4252

* Add new extension ``ConfusingConsecutiveElifChecker``. This optional checker emits a refactoring message (R5601 ``confusing-consecutive-elif``)
  if if/elif statements with different indentation levels follow directly one after the other.

* New option ``--output=<file>`` to output result to a file rather than printing to stdout.

  Closes #1070

* Use a prescriptive message for ``unidiomatic-typecheck``

  Closes #3891

* Apply ``const-naming-style`` to module constants annotated with
  ``typing.Final``

* The packaging is now done via setuptools exclusively. ``doc``, ``tests``, ``man``, ``elisp`` and ``Changelog`` are
  not packaged anymore - reducing the size of the package by 75%.

* Debian packaging is now  (officially) done in https://salsa.debian.org/python-team/packages/pylint.

* The 'doc' extra-require has been removed.

* ``__pkginfo__`` now only contain ``__version__`` (also accessible with ``pylint.__version__``), other meta-information are still
  accessible with ``from importlib import metadata;metadata.metadata('pylint')``.

* COPYING has been renamed to LICENSE for standardization.

* Fix false-positive ``used-before-assignment`` in function returns.

  Closes #4301

* Updated ``astroid`` to 2.5.3

  Closes #2822, #4206, #4284

* Add ``consider-using-min-max-builtin`` check for if statement which could be replaced by Python builtin min or max

  Closes #3406

* Don't auto-enable postponed evaluation of type annotations with Python 3.10

* Update ``astroid`` to 2.5.4

* Add new extension ``TypingChecker``. This optional checker can detect the use of deprecated typing aliases
  and can suggest the use of the alternative union syntax where possible.
  (For example, 'typing.Dict' can be replaced by 'dict', and 'typing.Unions' by '|', etc.)
  Make sure to check the config options if you plan on using it!

* Reactivates old counts in report mode.

  Closes #3819

* During detection of ``inconsistent-return-statements`` consider that ``assert False`` is a return node.

  Closes #4019

* Run will not fail if score exactly equals ``config.fail_under``.

* Functions that never returns may declare ``NoReturn`` as type hints, so that
  ``inconsistent-return-statements`` is not emitted.

  Closes #4122, #4188

* Improved protected access checks to allow access inside class methods

  Closes #1159

* Fix issue with PEP 585 syntax and the use of ``collections.abc.Set``

* Fix issue that caused class variables annotated with ``typing.ClassVar`` to be
  identified as class constants. Now, class variables annotated with
  ``typing.Final`` are identified as such.

  Closes #4277

* Continuous integration with read the doc has been added.

  Closes #3850

* Don't show ``DuplicateBasesError`` for attribute access

* Fix crash when checking ``setup.cfg`` for pylint config when there are non-ascii characters in there

  Closes #4328

* Allow code flanked in backticks to be skipped by spellchecker

  Closes #4319

* Allow Python tool directives (for black, flake8, zimports, isort, mypy, bandit, pycharm) at beginning of comments to be skipped by spellchecker

  Closes #4320

* Fix issue that caused Emacs pylint to fail when used with tramp

* Improve check for invalid PEP 585 syntax inside functions
  if postponed evaluation of type annotations is enabled

* Improve check for invalid PEP 585 syntax as default function arguments
