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

What's new in Pylint 2.17.1?
----------------------------
Release date: 2023-03-22


False Positives Fixed
---------------------

- Adds ``asyncSetUp`` to the default ``defining-attr-methods`` list to silence
  ``attribute-defined-outside-init`` warning when using
  ``unittest.IsolatedAsyncioTestCase``.

  Refs #8403 (`#8403 <https://github.com/PyCQA/pylint/issues/8403>`_)



Other Bug Fixes
---------------

- ``--clear-cache-post-run`` now also clears LRU caches for pylint utilities
  holding references to AST nodes.

  Closes #8361 (`#8361 <https://github.com/PyCQA/pylint/issues/8361>`_)

- Fix a crash when ``TYPE_CHECKING`` is used without importing it.

  Closes #8434 (`#8434 <https://github.com/PyCQA/pylint/issues/8434>`_)

- Fix a regression of ``preferred-modules`` where a partial match was used
  instead of the required full match.

  Closes #8453 (`#8453 <https://github.com/PyCQA/pylint/issues/8453>`_)



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

  Refs #8433 (`#8433 <https://github.com/PyCQA/pylint/issues/8433>`_)


What's new in Pylint 2.17.0?
----------------------------
Release date: 2023-03-08


New Features
------------

- `pyreverse` now supports custom color palettes with the `--color-palette`
  option.

  Closes #6738 (`#6738 <https://github.com/PyCQA/pylint/issues/6738>`_)

- Add ``invalid-name`` check for ``TypeAlias`` names.

  Closes #7081. (`#7081 <https://github.com/PyCQA/pylint/issues/7081>`_)

- Accept values of the form ``<class name>.<attribute name>`` for the
  ``exclude-protected`` list.

  Closes #7343 (`#7343 <https://github.com/PyCQA/pylint/issues/7343>`_)

- Add `--version` option to `pyreverse`.

  Refs #7851 (`#7851 <https://github.com/PyCQA/pylint/issues/7851>`_)

- Adds new functionality with preferred-modules configuration to detect
  submodules.

  Refs #7957 (`#7957 <https://github.com/PyCQA/pylint/issues/7957>`_)

- Support implicit namespace packages (PEP 420).

  Closes #8154 (`#8154 <https://github.com/PyCQA/pylint/issues/8154>`_)

- Add globbing pattern support for ``--source-roots``.

  Closes #8290 (`#8290 <https://github.com/PyCQA/pylint/issues/8290>`_)

- Support globbing pattern when defining which file/directory/module to lint.

  Closes #8310 (`#8310 <https://github.com/PyCQA/pylint/issues/8310>`_)

- pylint now supports ``TryStar`` nodes from Python 3.11 and should be fully
  compatible with Python 3.11.

  Closes #8387 (`#8387 <https://github.com/PyCQA/pylint/issues/8387>`_)



New Checks
----------

- Add a ``bad-chained-comparison`` check that emits a warning when
  there is a chained comparison where one expression is semantically
  incompatible with the other.

  Closes #6559 (`#6559 <https://github.com/PyCQA/pylint/issues/6559>`_)

- Adds an ``implicit-flag-alias`` check that emits a warning when a class
  derived from ``enum.IntFlag`` assigns distinct integer values that share
  common bit positions.

  Refs #8102 (`#8102 <https://github.com/PyCQA/pylint/issues/8102>`_)



False Positives Fixed
---------------------

- Fix various false positives for functions that return directly from
  structural pattern matching cases.

  Closes #5288 (`#5288 <https://github.com/PyCQA/pylint/issues/5288>`_)

- Fix false positive for ``used-before-assignment`` when
  ``typing.TYPE_CHECKING`` is used with if/elif/else blocks.

  Closes #7574 (`#7574 <https://github.com/PyCQA/pylint/issues/7574>`_)

- Fix false positive for isinstance-second-argument-not-valid-type with union
  types.

  Closes #8205 (`#8205 <https://github.com/PyCQA/pylint/issues/8205>`_)

- Fix false positive for ``used-before-assignment`` for named expressions
  appearing after the first element in a list, tuple, or set.

  Closes #8252 (`#8252 <https://github.com/PyCQA/pylint/issues/8252>`_)

- Fix false positive for ``wrong-spelling-in-comment`` with class names in a
  python 2 type comment.

  Closes #8370 (`#8370 <https://github.com/PyCQA/pylint/issues/8370>`_)



False Negatives Fixed
---------------------

- Fix a false negative for 'missing-parentheses-for-call-in-test' when
  inference
  failed for the internal of the call as we did not need that information to
  raise
  correctly.

  Refs #8185 (`#8185 <https://github.com/PyCQA/pylint/issues/8185>`_)

- Fix false negative for inconsistent-returns with while-loops.

  Closes #8280 (`#8280 <https://github.com/PyCQA/pylint/issues/8280>`_)



Other Bug Fixes
---------------

- Fix ``used-before-assignment`` false positive when the walrus operator
  is used with a ternary operator in dictionary key/value initialization.

  Closes #8125 (`#8125 <https://github.com/PyCQA/pylint/issues/8125>`_)

- Fix ``no-name-in-module`` false positive raised when a package defines a
  variable with the
  same name as one of its submodules.

  Closes #8148 (`#8148 <https://github.com/PyCQA/pylint/issues/8148>`_)

- Fix a crash happening for python interpreter < 3.9 following a failed typing
  update.

  Closes #8161 (`#8161 <https://github.com/PyCQA/pylint/issues/8161>`_)

- Fix ``nested-min-max`` suggestion message to indicate it's possible to splat
  iterable objects.

  Closes #8168 (`#8168 <https://github.com/PyCQA/pylint/issues/8168>`_)

- Fix a crash happening when a class attribute was negated in the start
  argument of an enumerate.

  Closes #8207 (`#8207 <https://github.com/PyCQA/pylint/issues/8207>`_)

- Prevent emitting ``invalid-name`` for the line on which a ``global``
  statement is declared.

  Closes #8307 (`#8307 <https://github.com/PyCQA/pylint/issues/8307>`_)



Other Changes
-------------

- Update explanation for ``global-variable-not-assigned`` and add confidence.

  Closes #5073 (`#5073 <https://github.com/PyCQA/pylint/issues/5073>`_)

- The governance model and the path to become a maintainer have been documented
  as
  part of our effort to guarantee that the software supply chain in which
  pylint is
  included is secure.

  Refs #8329 (`#8329 <https://github.com/PyCQA/pylint/issues/8329>`_)
