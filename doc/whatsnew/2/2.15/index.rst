***************************
 What's New in Pylint 2.15
***************************

.. toctree::
   :maxdepth: 2

:Release: 2.15
:Date: 2022-08-26

Summary -- Release highlights
=============================

In pylint 2.15.0, we added a new check ``missing-timeout`` to warn of
default timeout values that could cause a program to be hanging indefinitely.

We improved ``pylint``'s handling of namespace packages. More packages should
be linted without resorting to using the ``--recursive=y`` option.

We still welcome any community effort to help review, integrate, and add good/bad examples to the doc for
<https://github.com/PyCQA/pylint/issues/5953>`_. This should be doable without any ``pylint`` or ``astroid``
knowledge, so this is the perfect entrypoint if you want to contribute to ``pylint`` or open source without
any experience with our code!

Internally, we changed the way we generate the release notes, thanks to DudeNr33.
There will be no more conflict resolution to do in the changelog, and every contributor rejoice.

Marc Byrne became a maintainer, welcome to the team !

.. towncrier release notes start

New Checks
----------

- Added new checker ``missing-timeout`` to warn of default timeout values that could cause
  a program to be hanging indefinitely.

  Refs #6780 (`#6780 <https://github.com/PyCQA/pylint/issues/6780>`_)


False Positives Fixed
---------------------

- Don't report ``super-init-not-called`` for abstract ``__init__`` methods.

  Closes #3975 (`#3975 <https://github.com/PyCQA/pylint/issues/3975>`_)
- Don't report ``unsupported-binary-operation`` on Python <= 3.9 when using the ``|`` operator
  with types, if one has a metaclass that overloads ``__or__`` or ``__ror__`` as appropriate.

  Closes #4951 (`#4951 <https://github.com/PyCQA/pylint/issues/4951>`_)
- Don't report ``no-value-for-parameter`` for dataclasses fields annotated with ``KW_ONLY``.

  Closes #5767 (`#5767 <https://github.com/PyCQA/pylint/issues/5767>`_)
- Fixed inference of ``Enums`` when they are imported under an alias.

  Closes #5776 (`#5776 <https://github.com/PyCQA/pylint/issues/5776>`_)
- Prevent false positives when accessing ``PurePath.parents`` by index (not slice) on Python 3.10+.

  Closes #5832 (`#5832 <https://github.com/PyCQA/pylint/issues/5832>`_)
- ``unnecessary-list-index-lookup`` is now more conservative to avoid potential false positives.

  Closes #6896 (`#6896 <https://github.com/PyCQA/pylint/issues/6896>`_)
- Fix double emitting ``trailing-whitespace`` for multi-line docstrings.

  Closes #6936 (`#6936 <https://github.com/PyCQA/pylint/issues/6936>`_)
- ``import-error`` now correctly checks for ``contextlib.suppress`` guards on import statements.

  Closes #7270 (`#7270 <https://github.com/PyCQA/pylint/issues/7270>`_)
- Fix false positive for `no-self-argument`/`no-method-argument` when a staticmethod is applied to a function but uses a different name.

  Closes #7300 (`#7300 <https://github.com/PyCQA/pylint/issues/7300>`_)
- Fix `undefined-loop-variable` with `break` and `continue` statements in `else` blocks.

  Refs #7311 (`#7311 <https://github.com/PyCQA/pylint/issues/7311>`_)
- Improve default TypeVar name regex. Disallow names prefixed with ``T``.
  E.g. use ``AnyStrT`` instead of ``TAnyStr``.

  Refs #7322 (`#7322 <https://github.com/PyCQA/pylint/issues/7322>`_`)


False Negatives Fixed
---------------------

- Emit ``used-before-assignment`` when relying on a name that is reimported later in a function.

  Closes #4624 (`#4624 <https://github.com/PyCQA/pylint/issues/4624>`_)
- Emit ``used-before-assignment`` for self-referencing named expressions (``:=``) lacking
  prior assignments.

  Closes #5653 (`#5653 <https://github.com/PyCQA/pylint/issues/5653>`_)
- Emit ``used-before-assignment`` for self-referencing assignments under if conditions.

  Closes #6643 (`#6643 <https://github.com/PyCQA/pylint/issues/6643>`_)
- Emit ``modified-iterating-list`` and analogous messages for dicts and sets when iterating
  literals, or when using the ``del`` keyword.

  Closes #6648 (`#6648 <https://github.com/PyCQA/pylint/issues/6648>`_)
- Emit ``used-before-assignment`` when calling nested functions before assignment.

  Closes #6812 (`#6812 <https://github.com/PyCQA/pylint/issues/6812>`_)
- Emit ``nonlocal-without-binding`` when a nonlocal name has been assigned at a later point in the same scope.

  Closes #6883 (`#6883 <https://github.com/PyCQA/pylint/issues/6883>`_)
- Emit ``using-constant-test`` when testing the truth value of a variable or call result
  holding a generator.

  Closes #6909 (`#6909 <https://github.com/PyCQA/pylint/issues/6909>`_)
- Rename ``unhashable-dict-key`` to ``unhashable-member`` and emit when creating sets and dicts,
  not just when accessing dicts.

  Closes #7034, Closes #7055 (`#7034 <https://github.com/PyCQA/pylint/issues/7034>`_)


Other Bug Fixes
---------------

- Fix a failure to lint packages with ``__init__.py`` contained in directories lacking ``__init__.py``.

  Closes #1667 (`#1667 <https://github.com/PyCQA/pylint/issues/1667>`_)
- Fixed a syntax-error crash that was not handled properly when the declared encoding of a file
  was ``utf-9``.

  Closes #3860 (`#3860 <https://github.com/PyCQA/pylint/issues/3860>`_)
- Fix a crash in the ``not-callable`` check when there is ambiguity whether an instance is being incorrectly provided to ``__new__()``.

  Closes #7109 (`#7109 <https://github.com/PyCQA/pylint/issues/7109>`_)
- Fix crash when regex option raises a `re.error` exception.

  Closes #7202 (`#7202 <https://github.com/PyCQA/pylint/issues/7202>`_)
- Fix `undefined-loop-variable` from walrus in comprehension test.

  Closes #7222 (`#7222 <https://github.com/PyCQA/pylint/issues/7222>`_)
- Check for `<cwd>` before removing first item from `sys.path` in `modify_sys_path`.

  Closes #7231 (`#7231 <https://github.com/PyCQA/pylint/issues/7231>`_)
- Fix sys.path pollution in parallel mode.

  Closes #7246 (`#7246 <https://github.com/PyCQA/pylint/issues/7246>`_)
- Prevent `useless-parent-delegation` for delegating to a builtin
  written in C (e.g. `Exception.__init__`) with non-self arguments.

  Closes #7319 (`#7319 <https://github.com/PyCQA/pylint/issues/7319>`_)


Other Changes
-------------

- ``bad-exception-context`` has been renamed to ``bad-exception-cause`` as it is about the cause and not the context.

  Closes #3694 (`#3694 <https://github.com/PyCQA/pylint/issues/3694>`_)
- The message for ``literal-comparison`` is now more explicit about the problem and the
  solution.

  Closes #5237 (`#5237 <https://github.com/PyCQA/pylint/issues/5237>`_)
- ``useless-super-delegation`` has been renamed to ``useless-parent-delegation`` in order to be more generic.

  Closes #6953 (`#6953 <https://github.com/PyCQA/pylint/issues/6953>`_)
- Pylint now uses ``towncrier`` for changelog generation.

  Refs #6974 (`#6974 <https://github.com/PyCQA/pylint/issues/6974>`_)
- Update ``astroid`` to 2.12.

  Refs #7153 (`#7153 <https://github.com/PyCQA/pylint/issues/7153>`_)
- Fix crash when a type-annotated `__slots__` with no value is declared.

  Closes #7280 (`#7280 <https://github.com/PyCQA/pylint/issues/7280>`_)


Internal Changes
----------------

- Fixed an issue where it was impossible to update functional tests output when the existing
  output was impossible to parse. Instead of raising an error we raise a warning message and
  let the functional test fail with a default value.

  Refs #6891 (`#6891 <https://github.com/PyCQA/pylint/issues/6891>`_)
- ``pylint.testutils.primer`` is now a private API.

  Refs #6905 (`#6905 <https://github.com/PyCQA/pylint/issues/6905>`_)
- We changed the way we handle the changelog internally by using towncrier.
  If you're a contributor you won't have to fix merge conflicts in the
  changelog anymore.

  Closes #6974 (`#6974 <https://github.com/PyCQA/pylint/issues/6974>`_)
- Pylint is now using Scorecards to implement security recommendations from the
  `OpenSSF <https://openssf.org/>`_. This is done in order to secure our supply chains using a combination
  of automated tooling and best practices, most of which were already implemented before.

  Refs #7267 (`#7267 <https://github.com/PyCQA/pylint/issues/7267>`_)
