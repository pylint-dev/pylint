
***************************
 What's New in Pylint 3.2
***************************

.. toctree::
   :maxdepth: 2

:Release: 3.2
:Date: TBA

Summary -- Release highlights
=============================

.. towncrier release notes start

What's new in Pylint 3.2.7?
---------------------------
Release date: 2024-08-31


False Positives Fixed
---------------------

- Fixed a false positive `unreachable` for `NoReturn` coroutine functions.

  Closes #9840. (`#9840 <https://github.com/pylint-dev/pylint/issues/9840>`_)



Other Bug Fixes
---------------

- Fix crash in refactoring checker when calling a lambda bound as a method.

  Closes #9865 (`#9865 <https://github.com/pylint-dev/pylint/issues/9865>`_)

- Fix a crash in ``undefined-loop-variable`` when providing the ``iterable`` argument to ``enumerate()``.

  Closes #9875 (`#9875 <https://github.com/pylint-dev/pylint/issues/9875>`_)

- Fix to address indeterminacy of error message in case a module name is same as another in a separate namespace.

  Refs #9883 (`#9883 <https://github.com/pylint-dev/pylint/issues/9883>`_)



What's new in Pylint 3.2.6?
---------------------------
Release date: 2024-07-21


False Positives Fixed
---------------------

- Quiet false positives for `unexpected-keyword-arg` when pylint cannot
  determine which of two or more dynamically defined classes is being instantiated.

  Closes #9672 (`#9672 <https://github.com/pylint-dev/pylint/issues/9672>`_)

- Fix a false positive for ``missing-param-doc`` where a method which is decorated with ``typing.overload`` was expected to have a docstring specifying its parameters.

  Closes #9739 (`#9739 <https://github.com/pylint-dev/pylint/issues/9739>`_)

- Fix a regression that raised ``invalid-name`` on class attributes merely
  overriding invalid names from an ancestor.

  Closes #9765 (`#9765 <https://github.com/pylint-dev/pylint/issues/9765>`_)

- Treat `assert_never()` the same way when imported from `typing_extensions`.

  Closes #9780 (`#9780 <https://github.com/pylint-dev/pylint/issues/9780>`_)

- Fix a false positive for `consider-using-min-max-builtin` when the assignment target is an attribute.

  Refs #9800 (`#9800 <https://github.com/pylint-dev/pylint/issues/9800>`_)



Other Bug Fixes
---------------

- Fix an `AssertionError` arising from properties that return partial functions.

  Closes #9214 (`#9214 <https://github.com/pylint-dev/pylint/issues/9214>`_)

- Fix a crash when a subclass extends ``__slots__``.

  Closes #9814 (`#9814 <https://github.com/pylint-dev/pylint/issues/9814>`_)



What's new in Pylint 3.2.5?
---------------------------
Release date: 2024-06-28


Other Bug Fixes
---------------

- Fixed a false positive ``unreachable-code`` when using ``typing.Any`` as return type in python
  3.8, the ``typing.NoReturn`` are not taken into account anymore for python 3.8 however.

  Closes #9751 (`#9751 <https://github.com/pylint-dev/pylint/issues/9751>`_)



What's new in Pylint 3.2.4?
---------------------------
Release date: 2024-06-26


False Positives Fixed
---------------------

- Prevent emitting ``possibly-used-before-assignment`` when relying on names
  only potentially not defined in conditional blocks guarded by functions
  annotated with ``typing.Never`` or ``typing.NoReturn``.

  Closes #9674 (`#9674 <https://github.com/pylint-dev/pylint/issues/9674>`_)



Other Bug Fixes
---------------

- Fixed a crash when the lineno of a variable used as an annotation wasn't available for ``undefined-variable``.

  Closes #8866 (`#8866 <https://github.com/pylint-dev/pylint/issues/8866>`_)

- Fixed a crash when the ``start`` value in an ``enumerate`` was non-constant and impossible to infer
  (like in``enumerate(apples, start=int(random_apple_index)``) for ``unnecessary-list-index-lookup``.

  Closes #9078 (`#9078 <https://github.com/pylint-dev/pylint/issues/9078>`_)

- Fixed a crash in ``symilar`` when the ``-d`` or ``-i`` short option were not properly recognized.
  It's still impossible to do ``-d=1`` (you must do ``-d 1``).

  Closes #9343 (`#9343 <https://github.com/pylint-dev/pylint/issues/9343>`_)



What's new in Pylint 3.2.3?
---------------------------
Release date: 2024-06-06


False Positives Fixed
---------------------

- Classes with only an Ellipsis (``...``) in their body do not trigger 'multiple-statements'
  anymore if they are inlined (in accordance with black's 2024 style).

  Closes #9398 (`#9398 <https://github.com/pylint-dev/pylint/issues/9398>`_)

- Fix a false positive for ``redefined-outer-name`` when there is a name defined in an exception-handling block which shares the same name as a local variable that has been defined in a function body.

  Closes #9671 (`#9671 <https://github.com/pylint-dev/pylint/issues/9671>`_)

- Fix a false positive for ``use-yield-from`` when using the return value from the ``yield`` atom.

  Closes #9696 (`#9696 <https://github.com/pylint-dev/pylint/issues/9696>`_)



What's new in Pylint 3.2.2?
---------------------------
Release date: 2024-05-20


False Positives Fixed
---------------------

- Fix multiple false positives for generic class syntax added in Python 3.12 (PEP 695).

  Closes #9406 (`#9406 <https://github.com/pylint-dev/pylint/issues/9406>`_)

- Exclude context manager without cleanup from
  ``contextmanager-generator-missing-cleanup`` checks.

  Closes #9625 (`#9625 <https://github.com/pylint-dev/pylint/issues/9625>`_)



What's new in Pylint 3.2.1?
---------------------------
Release date: 2024-05-18


False Positives Fixed
---------------------

- Exclude if/else branches containing terminating functions (e.g. `sys.exit()`)
  from `possibly-used-before-assignment` checks.

  Closes #9627 (`#9627 <https://github.com/pylint-dev/pylint/issues/9627>`_)

- Don't emit ``typevar-name-incorrect-variance`` warnings for PEP 695 style TypeVars.
  The variance is inferred automatically by the type checker.
  Adding ``_co`` or ``_contra`` suffix can help to reason about TypeVar.

  Refs #9638 (`#9638 <https://github.com/pylint-dev/pylint/issues/9638>`_)

- Fix a false positive for `possibly-used-before-assignment` when using
  `typing.assert_never()` (3.11+) to indicate exhaustiveness.

  Closes #9643 (`#9643 <https://github.com/pylint-dev/pylint/issues/9643>`_)



Other Bug Fixes
---------------

- Fix a false negative for ``--ignore-patterns`` when the directory to be linted is specified using a dot(``.``) and all files are ignored instead of only the files whose name begin with a dot.

  Closes #9273 (`#9273 <https://github.com/pylint-dev/pylint/issues/9273>`_)

- Restore "errors / warnings by module" section to report output (with `-ry`).

  Closes #9145 (`#9145 <https://github.com/pylint-dev/pylint/issues/9145>`_)

- ``trailing-comma-tuple`` should now be correctly emitted when it was disabled globally
  but enabled via local message control, after removal of an over-optimisation.

  Refs #9608. (`#9608 <https://github.com/pylint-dev/pylint/issues/9608>`_)

- Add `--prefer-stubs=yes` option to opt-in to the astroid 3.2 feature
  that prefers `.pyi` stubs over same-named `.py` files. This has the
  potential to reduce `no-member` errors but at the cost of more errors
  such as `not-an-iterable` from function bodies appearing as `...`.

  Defaults to `no`.

  Closes #9626
  Closes #9623 (`#9626 <https://github.com/pylint-dev/pylint/issues/9626>`_)



Internal Changes
----------------

- Update astroid version to 3.2.1. This solves some reports of ``RecursionError``
  and also makes the *prefer .pyi stubs* feature in astroid 3.2.0 *opt-in*
  with the aforementioned ``--prefer-stubs=y`` option.

  Refs #9139 (`#9139 <https://github.com/pylint-dev/pylint/issues/9139>`_)



What's new in Pylint 3.2.0?
---------------------------
Release date: 2024-05-14


New Features
------------

- Understand `six.PY2` and `six.PY3` for conditional imports.

  Closes #3501 (`#3501 <https://github.com/pylint-dev/pylint/issues/3501>`_)

- A new `github` reporter has been added. This reporter  returns the output of `pylint` in a format that
  Github can use to automatically annotate code. Use it with `pylint --output-format=github` on your Github Workflows.

  Closes #9443. (`#9443 <https://github.com/pylint-dev/pylint/issues/9443>`_)



New Checks
----------

- Add check ``possibly-used-before-assignment`` when relying on names after an ``if/else``
  switch when one branch failed to define the name, raise, or return.

  Closes #1727 (`#1727 <https://github.com/pylint-dev/pylint/issues/1727>`_)

- Checks for generators that use contextmanagers that don't handle cleanup properly.
  Is meant to raise visibility on the case that a generator is not fully exhausted and the contextmanager is not cleaned up properly.
  A contextmanager must yield a non-constant value and not handle cleanup for GeneratorExit.
  The using generator must attempt to use the yielded context value `with x() as y` and not just `with x()`.

  Closes #2832 (`#2832 <https://github.com/pylint-dev/pylint/issues/2832>`_)



False Negatives Fixed
---------------------

- If and Try nodes are now checked for useless return statements as well.

  Closes #9449. (`#9449 <https://github.com/pylint-dev/pylint/issues/9449>`_)

- Fix false negative for ``property-with-parameters`` in the case of parameters which are ``positional-only``, ``keyword-only``, ``variadic positional`` or ``variadic keyword``.

  Closes #9584 (`#9584 <https://github.com/pylint-dev/pylint/issues/9584>`_)

False Positives Fixed
---------------------

pylint now understands the ``@overload`` decorator return values better.

Closes #4696 (`#4696 <https://github.com/pylint-dev/pylint/issues/4696>`_)
Refs #9606 (`#9606 <https://github.com/pylint-dev/pylint/issues/9606>`_)

Performance Improvements
------------------------


- Ignored modules are now not checked at all, instead of being checked and then
  ignored. This should speed up the analysis of large codebases which have
  ignored modules.

  Closes #9442 (`#9442 <https://github.com/pylint-dev/pylint/issues/9442>`_) (`#9442 <https://github.com/pylint-dev/pylint/issues/9442>`_)


- ImportChecker's logic has been modified to avoid context files when possible. This makes it possible
  to cache module searches on astroid and reduce execution times.

  Refs #9310. (`#9310 <https://github.com/pylint-dev/pylint/issues/9310>`_)

- An internal check for ``trailing-comma-tuple`` being enabled for a file or not is now
  done once per file instead of once for each token.

  Refs #9608. (`#9608 <https://github.com/pylint-dev/pylint/issues/9608>`_)
