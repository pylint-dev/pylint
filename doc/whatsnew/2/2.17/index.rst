***************************
 What's New in Pylint 2.17
***************************

.. toctree::
   :maxdepth: 2

:Release: 2.17
:Date: 2023-03-08

Summary -- Release highlights
=============================

2.17 is a small release that is the first to support python 3.11
officially with the addition of TryStar nodes.

There's still two new default checks: ``bad-chained-comparison`` and
``implicit-flag-alias``, one of them already fixed a previously
undetected bug in sentry.

Thanks to the community effort our documentation is almost complete,
and every messages should have a proper documentation now. A big thank
you to everyone who participated !

The next release is going to be ``3.0.0``, bring breaking changes and enact long
announced deprecations. There's going to be frequent beta releases,
before the official releases, everyone is welcome to try the betas
so we find problems before the actual release.

.. towncrier release notes start

What's new in Pylint 2.17.7?
----------------------------
Release date: 2023-09-30


False Positives Fixed
---------------------

- Fix a regression in pylint 2.17.6 / astroid 2.15.7 causing various
  messages for code involving ``TypeVar``.

  Closes #9069 (`#9069 <https://github.com/pylint-dev/pylint/issues/9069>`_)



Other Bug Fixes
---------------

- Fix crash in refactoring checker when unary operand used with variable in for
  loop.

  Closes #9074 (`#9074 <https://github.com/pylint-dev/pylint/issues/9074>`_)


What's new in Pylint 2.17.6?
----------------------------
Release date: 2023-09-24


Other Bug Fixes
---------------

- When parsing comma-separated lists of regular expressions in the config,
  ignore
  commas that are inside braces since those indicate quantifiers, not
  delineation
  between expressions.

  Closes #7229 (`#7229 <https://github.com/pylint-dev/pylint/issues/7229>`_)

- ``sys.argv`` is now always correctly considered as impossible to infer
  (instead of
  using the actual values given to pylint).

  Closes #7710 (`#7710 <https://github.com/pylint-dev/pylint/issues/7710>`_)

- Don't show class fields more than once in Pyreverse diagrams.

  Closes #8189 (`#8189 <https://github.com/pylint-dev/pylint/issues/8189>`_)

- Don't show arrows more than once in Pyreverse diagrams.

  Closes #8522 (`#8522 <https://github.com/pylint-dev/pylint/issues/8522>`_)

- Don't show duplicate type annotations in Pyreverse diagrams.

  Closes #8888 (`#8888 <https://github.com/pylint-dev/pylint/issues/8888>`_)

- Don't add `Optional` to `|` annotations with `None` in Pyreverse diagrams.

  Closes #9014 (`#9014 <https://github.com/pylint-dev/pylint/issues/9014>`_)


What's new in Pylint 2.17.5?
----------------------------
Release date: 2023-07-26


False Positives Fixed
---------------------

- Fix a false positive for ``unused-variable`` when there is an import in a
  ``if TYPE_CHECKING:`` block and ``allow-global-unused-variables`` is set to
  ``no`` in the configuration.

  Closes #8696 (`#8696 <https://github.com/pylint-dev/pylint/issues/8696>`_)

- Fix false positives generated when supplying arguments as ``**kwargs`` to IO
  calls like open().

  Closes #8719 (`#8719 <https://github.com/pylint-dev/pylint/issues/8719>`_)

- Fix a false positive where pylint was ignoring method calls annotated as
  ``NoReturn`` during the ``inconsistent-return-statements`` check.

  Closes #8747 (`#8747 <https://github.com/pylint-dev/pylint/issues/8747>`_)

- Exempt parents with only type annotations from the ``invalid-enum-extension``
  message.

  Closes #8830 (`#8830 <https://github.com/pylint-dev/pylint/issues/8830>`_)



Other Bug Fixes
---------------

- Fixed crash when a call to ``super()`` was placed after an operator (e.g.
  ``not``).

  Closes #8554 (`#8554 <https://github.com/pylint-dev/pylint/issues/8554>`_)

- Fix crash for ``modified-while-iterating`` checker when deleting
  members of a dict returned from a call.

  Closes #8598 (`#8598 <https://github.com/pylint-dev/pylint/issues/8598>`_)

- Fix crash in ``invalid-metaclass`` check when a metaclass had duplicate
  bases.

  Closes #8698 (`#8698 <https://github.com/pylint-dev/pylint/issues/8698>`_)

- Avoid ``consider-using-f-string`` on modulos with brackets in template.

  Closes #8720. (`#8720 <https://github.com/pylint-dev/pylint/issues/8720>`_)

- Fix a crash when ``__all__`` exists but cannot be inferred.

  Closes #8740 (`#8740 <https://github.com/pylint-dev/pylint/issues/8740>`_)

- Fix crash when a variable is assigned to a class attribute of identical name.

  Closes #8754 (`#8754 <https://github.com/pylint-dev/pylint/issues/8754>`_)

- Fixed a crash when calling ``copy.copy()`` without arguments.

  Closes #8774 (`#8774 <https://github.com/pylint-dev/pylint/issues/8774>`_)



Other Changes
-------------

- Fix a crash when a ``nonlocal`` is defined at module-level.

  Closes #8735 (`#8735 <https://github.com/pylint-dev/pylint/issues/8735>`_)


What's new in Pylint 2.17.4?
----------------------------
Release date: 2023-05-06


False Positives Fixed
---------------------

- Fix a false positive for ``bad-dunder-name`` when there is a user-defined
  ``__index__`` method.

  Closes #8613 (`#8613 <https://github.com/pylint-dev/pylint/issues/8613>`_)



Other Bug Fixes
---------------

- ``pyreverse``: added escaping of vertical bar character in annotation labels
  produced by DOT printer to ensure it is not treated as field separator of
  record-based nodes.

  Closes #8603 (`#8603 <https://github.com/pylint-dev/pylint/issues/8603>`_)

- Fixed a crash when generating a configuration file:
  ``tomlkit.exceptions.TOMLKitError: Can't add a table to a dotted key``
  caused by tomlkit ``v0.11.8``.

  Closes #8632 (`#8632 <https://github.com/pylint-dev/pylint/issues/8632>`_)


What's new in Pylint 2.17.3?
----------------------------
Release date: 2023-04-24


False Positives Fixed
---------------------

- Fix `unused-argument` false positive when `__new__` does not use all the
  arguments of `__init__`.

  Closes #3670 (`#3670 <https://github.com/pylint-dev/pylint/issues/3670>`_)

- Fix ``unused-import`` false positive for usage of ``six.with_metaclass``.

  Closes #7506 (`#7506 <https://github.com/pylint-dev/pylint/issues/7506>`_)

- `logging-not-lazy` is not longer emitted for explicitly concatenated string
  arguments.

  Closes #8410 (`#8410 <https://github.com/pylint-dev/pylint/issues/8410>`_)

- Fix false positive for isinstance-second-argument-not-valid-type when union
  types contains None.

  Closes #8424 (`#8424 <https://github.com/pylint-dev/pylint/issues/8424>`_)

- Fixed `unused-import` so that it observes the `dummy-variables-rgx` option.

  Closes #8500 (`#8500 <https://github.com/pylint-dev/pylint/issues/8500>`_)

- `Union` typed variables without assignment are no longer treated as
  `TypeAlias`.

  Closes #8540 (`#8540 <https://github.com/pylint-dev/pylint/issues/8540>`_)

- Fix false positive for ``positional-only-arguments-expected`` when a function
  contains both a positional-only parameter that has a default value, and
  ``**kwargs``.

  Closes #8555 (`#8555 <https://github.com/pylint-dev/pylint/issues/8555>`_)

- Fix false positive for ``keyword-arg-before-vararg`` when a positional-only
  parameter with a default value precedes ``*args``.

  Closes #8570 (`#8570 <https://github.com/pylint-dev/pylint/issues/8570>`_)



Other Bug Fixes
---------------

- Improve output of ``consider-using-generator`` message for ``min()`` calls
  with ``default`` keyword.

  Closes #8563 (`#8563 <https://github.com/pylint-dev/pylint/issues/8563>`_)


What's new in Pylint 2.17.2?
----------------------------
Release date: 2023-04-03


False Positives Fixed
---------------------

- ``invalid-name`` now allows for integers in ``typealias`` names:
  - now valid: ``Good2Name``, ``GoodName2``.
  - still invalid: ``_1BadName``.

  Closes #8485 (`#8485 <https://github.com/pylint-dev/pylint/issues/8485>`_)

- No longer consider ``Union`` as type annotation as type alias for naming
  checks.

  Closes #8487 (`#8487 <https://github.com/pylint-dev/pylint/issues/8487>`_)

- ``unnecessary-lambda`` no longer warns on lambdas which use its parameters in
  their body (other than the final arguments), e.g.
  ``lambda foo: (bar if foo else baz)(foo)``.

  Closes #8496 (`#8496 <https://github.com/pylint-dev/pylint/issues/8496>`_)



Other Bug Fixes
---------------

- Fix a crash in pyreverse when "/" characters are used in the output filename
  e.g pyreverse -o png -p name/ path/to/project.

  Closes #8504 (`#8504 <https://github.com/pylint-dev/pylint/issues/8504>`_)


What's new in Pylint 2.17.1?
----------------------------
Release date: 2023-03-22


False Positives Fixed
---------------------

- Adds ``asyncSetUp`` to the default ``defining-attr-methods`` list to silence
  ``attribute-defined-outside-init`` warning when using
  ``unittest.IsolatedAsyncioTestCase``.

  Refs #8403 (`#8403 <https://github.com/pylint-dev/pylint/issues/8403>`_)



Other Bug Fixes
---------------

- ``--clear-cache-post-run`` now also clears LRU caches for pylint utilities
  holding references to AST nodes.

  Closes #8361 (`#8361 <https://github.com/pylint-dev/pylint/issues/8361>`_)

- Fix a crash when ``TYPE_CHECKING`` is used without importing it.

  Closes #8434 (`#8434 <https://github.com/pylint-dev/pylint/issues/8434>`_)

- Fix a regression of ``preferred-modules`` where a partial match was used
  instead of the required full match.

  Closes #8453 (`#8453 <https://github.com/pylint-dev/pylint/issues/8453>`_)



Internal Changes
----------------

- The following utilities are deprecated in favor of the more robust
  ``in_type_checking_block``
  and will be removed in pylint 3.0:

    - ``is_node_in_guarded_import_block``
    - ``is_node_in_typing_guarded_import_block``
    - ``is_typing_guard``

  ``is_sys_guard`` is still available, which was part of
  ``is_node_in_guarded_import_block``.

  Refs #8433 (`#8433 <https://github.com/pylint-dev/pylint/issues/8433>`_)


What's new in Pylint 2.17.0?
----------------------------
Release date: 2023-03-08


New Features
------------

- `pyreverse` now supports custom color palettes with the `--color-palette`
  option.

  Closes #6738 (`#6738 <https://github.com/pylint-dev/pylint/issues/6738>`_)

- Add ``invalid-name`` check for ``TypeAlias`` names.

  Closes #7081. (`#7081 <https://github.com/pylint-dev/pylint/issues/7081>`_)

- Accept values of the form ``<class name>.<attribute name>`` for the
  ``exclude-protected`` list.

  Closes #7343 (`#7343 <https://github.com/pylint-dev/pylint/issues/7343>`_)

- Add `--version` option to `pyreverse`.

  Refs #7851 (`#7851 <https://github.com/pylint-dev/pylint/issues/7851>`_)

- Adds new functionality with preferred-modules configuration to detect
  submodules.

  Refs #7957 (`#7957 <https://github.com/pylint-dev/pylint/issues/7957>`_)

- Support implicit namespace packages (PEP 420).

  Closes #8154 (`#8154 <https://github.com/pylint-dev/pylint/issues/8154>`_)

- Add globbing pattern support for ``--source-roots``.

  Closes #8290 (`#8290 <https://github.com/pylint-dev/pylint/issues/8290>`_)

- Support globbing pattern when defining which file/directory/module to lint.

  Closes #8310 (`#8310 <https://github.com/pylint-dev/pylint/issues/8310>`_)

- pylint now supports ``TryStar`` nodes from Python 3.11 and should be fully
  compatible with Python 3.11.

  Closes #8387 (`#8387 <https://github.com/pylint-dev/pylint/issues/8387>`_)



New Checks
----------

- Add a ``bad-chained-comparison`` check that emits a warning when
  there is a chained comparison where one expression is semantically
  incompatible with the other.

  Closes #6559 (`#6559 <https://github.com/pylint-dev/pylint/issues/6559>`_)

- Adds an ``implicit-flag-alias`` check that emits a warning when a class
  derived from ``enum.IntFlag`` assigns distinct integer values that share
  common bit positions.

  Refs #8102 (`#8102 <https://github.com/pylint-dev/pylint/issues/8102>`_)



False Positives Fixed
---------------------

- Fix various false positives for functions that return directly from
  structural pattern matching cases.

  Closes #5288 (`#5288 <https://github.com/pylint-dev/pylint/issues/5288>`_)

- Fix false positive for ``used-before-assignment`` when
  ``typing.TYPE_CHECKING`` is used with if/elif/else blocks.

  Closes #7574 (`#7574 <https://github.com/pylint-dev/pylint/issues/7574>`_)

- Fix false positive for isinstance-second-argument-not-valid-type with union
  types.

  Closes #8205 (`#8205 <https://github.com/pylint-dev/pylint/issues/8205>`_)

- Fix false positive for ``used-before-assignment`` for named expressions
  appearing after the first element in a list, tuple, or set.

  Closes #8252 (`#8252 <https://github.com/pylint-dev/pylint/issues/8252>`_)

- Fix false positive for ``wrong-spelling-in-comment`` with class names in a
  python 2 type comment.

  Closes #8370 (`#8370 <https://github.com/pylint-dev/pylint/issues/8370>`_)



False Negatives Fixed
---------------------

- Fix a false negative for 'missing-parentheses-for-call-in-test' when
  inference
  failed for the internal of the call as we did not need that information to
  raise
  correctly.

  Refs #8185 (`#8185 <https://github.com/pylint-dev/pylint/issues/8185>`_)

- Fix false negative for inconsistent-returns with while-loops.

  Closes #8280 (`#8280 <https://github.com/pylint-dev/pylint/issues/8280>`_)



Other Bug Fixes
---------------

- Fix ``used-before-assignment`` false positive when the walrus operator
  is used with a ternary operator in dictionary key/value initialization.

  Closes #8125 (`#8125 <https://github.com/pylint-dev/pylint/issues/8125>`_)

- Fix ``no-name-in-module`` false positive raised when a package defines a
  variable with the
  same name as one of its submodules.

  Closes #8148 (`#8148 <https://github.com/pylint-dev/pylint/issues/8148>`_)

- Fix a crash happening for python interpreter < 3.9 following a failed typing
  update.

  Closes #8161 (`#8161 <https://github.com/pylint-dev/pylint/issues/8161>`_)

- Fix ``nested-min-max`` suggestion message to indicate it's possible to splat
  iterable objects.

  Closes #8168 (`#8168 <https://github.com/pylint-dev/pylint/issues/8168>`_)

- Fix a crash happening when a class attribute was negated in the start
  argument of an enumerate.

  Closes #8207 (`#8207 <https://github.com/pylint-dev/pylint/issues/8207>`_)

- Prevent emitting ``invalid-name`` for the line on which a ``global``
  statement is declared.

  Closes #8307 (`#8307 <https://github.com/pylint-dev/pylint/issues/8307>`_)



Other Changes
-------------

- Update explanation for ``global-variable-not-assigned`` and add confidence.

  Closes #5073 (`#5073 <https://github.com/pylint-dev/pylint/issues/5073>`_)

- The governance model and the path to become a maintainer have been documented
  as
  part of our effort to guarantee that the software supply chain in which
  pylint is
  included is secure.

  Refs #8329 (`#8329 <https://github.com/pylint-dev/pylint/issues/8329>`_)
