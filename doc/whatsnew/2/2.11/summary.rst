:Release: 2.11
:Date: 2021-09-16

Summary -- Release highlights
=============================

In 2.11, we added a new default checker to advise using f-string as it's
the most efficient way of formatting strings right now. You can use
`pyupgrade`_, `ruff`_ or `flynt`_ to migrate your old ``%`` and ``format()`` automatically.

We added a new extension ``SetMembershipChecker`` that will advise the
use of set for membership test, as it's more performant than lists or tuples.
The ``CodeStyleChecker`` also got some love, check it out if you're not already
using it.

We fixed some long standing bugs, false positives, or false negatives and
we added small quality of life options like ``min-similarity-lines`` that
disable the duplication check when set to 0.

Under the hood the code for both pylint and astroid is progressively more typed,
which could be helpful to you if you're using them as libraries. In order for
this new typing to make more sense and stay simple, we deprecated some functions
or type that will be removed in the next major version. This is an ongoing effort.

The future ``possible-forgotten-f-prefix`` check still had too much false positives,
and is delayed again. Check the `possible-forgotten-f-prefix`_ issue if you want
to provide knowledge or use case :)

.. _possible-forgotten-f-prefix: https://github.com/pylint-dev/pylint/pull/4787
.. _pyupgrade: https://github.com/asottile/pyupgrade
.. _flynt: https://github.com/ikamensh/flynt
.. _ruff: https://docs.astral.sh/ruff/

New checkers
============

* Added ``consider-using-f-string``: Emitted when .format() or '%' is being used to format a string.

  Closes #3592

Removed checkers
================

* The python3 porting mode checker and its ``py3k`` option were removed. You can still find it in older pylint
  versions.

Extensions
==========

* Added new extension ``SetMembershipChecker`` with ``use-set-for-membership`` check:
  Emitted when using an in-place defined ``list`` or ``tuple`` to do a membership test. ``sets`` are better optimized for that.

  Closes #4776

CodeStyleChecker
----------------

* Added ``consider-using-assignment-expr``: Emitted when an assignment is directly followed by an if statement
  and both can be combined by using an assignment expression ``:=``. Requires Python 3.8

  Closes #4862


Other Changes
=============

* Added ``py-version`` config key (if ``[MAIN]`` section). Used for version dependent checks.
  Will default to whatever Python version pylint is executed with.

* The ``invalid-name`` message is now more detailed when using multiple naming style regexes.

* Fix false positive for ``consider-using-with`` if a context manager is assigned to a
  variable in different paths of control flow (e. g. if-else clause).

  Closes #4751

* Fix false positive for ``function-redefined`` for simple type annotations

  Closes #4936

* Fix false positive for ``protected-access`` if a protected member is used in type hints of function definitions

* Fix false positive ``dict-iter-missing-items`` for dictionaries only using tuples as keys

  Closes #3282

* The ``unspecified-encoding`` checker now also checks calls to ``pathlib.Path().read_text()``
  and ``pathlib.Path().write_text()``

  Closes #4945

* Fix false positive ``superfluous-parens`` for tuples created with inner tuples

  Closes #4907

* Fix false positive ``unused-private-member`` for accessing attributes in a class using ``cls``

  Closes #4849

* Extended ``consider-using-in`` check to work for attribute access.

* Setting ``min-similarity-lines`` to 0 now makes the similarty checker stop checking for duplicate code

  Closes #4901

* Fix a bug where pylint complained if the cache's parent directory does not exist

  Closes #4900

* The ``global-variable-not-assigned`` checker now catches global variables that are never reassigned in a
  local scope and catches (reassigned) functions

  Closes #1375
  Closes #330

* The ``consider-iterating-dictionary`` checker now also considers membership checks

  Closes #4069
