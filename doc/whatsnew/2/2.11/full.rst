Full changelog
==============

What's New in Pylint 2.11.1?
----------------------------
Release date: 2021-09-16

* ``unspecified-encoding`` now checks the encoding of ``pathlib.Path()`` correctly

  Closes #5017


What's New in Pylint 2.11.0?
----------------------------
Release date: 2021-09-16

* The python3 porting mode checker and its ``py3k`` option were removed. You can still find it in older pylint
  versions.

* ``raising-bad-type`` is now properly emitted when  raising a string

* Added new extension ``SetMembershipChecker`` with ``use-set-for-membership`` check:
  Emitted when using an in-place defined ``list`` or ``tuple`` to do a membership test. ``sets`` are better optimized for that.

  Closes #4776

* Added ``py-version`` config key (if ``[MASTER]`` section). Used for version dependent checks.
  Will default to whatever Python version pylint is executed with.

* ``CodeStyleChecker``: Added ``consider-using-assignment-expr``: Emitted when an assignment is directly followed by an if statement
  and both can be combined by using an assignment expression ``:=``. Requires Python 3.8

  Closes #4862

* Added ``consider-using-f-string``: Emitted when .format() or '%' is being used to format a string.

  Closes #3592

* Fix false positive for ``consider-using-with`` if a context manager is assigned to a
  variable in different paths of control flow (e. g. if-else clause).

  Closes #4751

* https is now preferred in the documentation and http://pylint.pycqa.org correctly redirect to https://pylint.pycqa.org

  Closes #3802

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

* Fix false positive ``unused-private-member`` for private staticmethods accessed in classmethods.

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

* Fix false positives for invalid-all-format that are lists or tuples at runtime

  Closes #4711

* Fix ``no-self-use`` and ``docparams extension`` for async functions and methods.

* Add documentation for ``pyreverse`` and ``symilar``

  Closes #4616

* Non symbolic messages with the wrong capitalisation now correctly trigger ``use-symbolic-message-instead``

  Closes #5000

* The ``consider-iterating-dictionary`` checker now also considers membership checks

  Closes #4069

* The ``invalid-name`` message is now more detailed when using multiple naming style regexes.
