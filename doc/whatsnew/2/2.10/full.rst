Full changelog
==============

What's New in Pylint 2.10.2?
----------------------------
Release date: 2021-08-21

* We now use platformdirs instead of appdirs since the latter is not maintained.

  Closes #4886

* Fix a crash in the checker raising ``shallow-copy-environ`` when failing to infer
  on ``copy.copy``

  Closes #4891



What's New in Pylint 2.10.1?
----------------------------
Release date: 2021-08-20

* pylint does not crash when PYLINT_HOME does not exist.

  Closes #4883


What's New in Pylint 2.10.0?
----------------------------
Release date: 2021-08-20

* pyreverse: add option to produce colored output.

  Closes #4488

* pyreverse: add output in PlantUML format.

  Closes #4498

* ``consider-using-with`` is no longer triggered if a context manager is returned from a function.

  Closes #4748

* pylint does not crash with a traceback anymore when a file is problematic. It
  creates a template text file for opening an issue on the bug tracker instead.
  The linting can go on for other non problematic files instead of being impossible.

* pyreverse: Show class has-a relationships inferred from the type-hint

  Closes #4744

* Fixed a crash when importing beyond the top level package during ``import-error``
  message creation

  Closes #4775

* Added ``ignored-parents`` option to the design checker to ignore specific
  classes from the ``too-many-ancestors`` check (R0901).

  Fixes part of #3057

* Added ``unspecified-encoding``: Emitted when open() is called without specifying an encoding

  Closes #3826

* Improved the Similarity checker performance. Fix issue with ``--min-similarity-lines`` used with ``--jobs``.

  Closes #4120
  Closes #4118

* Don't emit ``no-member`` error if guarded behind if statement.

  Refs #1162
  Closes #1990
  Closes #4168

* The default for ``PYLINTHOME`` is now the standard ``XDG_CACHE_HOME``, and pylint now uses ``appdirs``.

  Closes #3878

* Added ``use-list-literal``: Emitted when ``list()`` is called with no arguments instead of using ``[]``

  Closes #4365

* Added ``use-dict-literal``: Emitted when ``dict()`` is called with no arguments instead of using ``{}``

  Closes #4365

* Added optional extension ``consider-ternary-expression``: Emitted whenever a variable is assigned in both branches of an if/else block.

  Closes # 4366

* Added optional extension ``while-used``: Emitted whenever a ``while`` loop is used.

  Closes # 4367

* Added ``forgotten-debug-statement``: Emitted when ``breakpoint``, ``pdb.set_trace`` or ``sys.breakpointhook`` calls are found

  Closes #3692

* Fix false-positive of ``unused-private-member`` when using nested functions in a class

  Closes #4673

* Fix crash for ``unused-private-member`` that occurred with nested attributes.

  Closes #4755

* Fix a false positive for ``unused-private-member`` with class names

  Closes #4681

* Fix false positives for ``superfluous-parens`` with walrus operator, ternary operator and inside list comprehension.

  Closes #2818
  Closes #3249
  Closes #3608
  Closes #4346

* Added ``format-string-without-interpolation`` checker: Emitted when formatting is applied to a string without any variables to be replaced

  Closes #4042

* Refactor of ``--list-msgs`` & ``--list-msgs-enabled``: both options now show whether messages are emittable with the current interpreter.

  Closes #4778

* Fix false negative for ``used-before-assignment`` when the variable is assigned
  in an exception handler, but used outside of the handler.

  Closes #626

* Added ``disable-next`` option: allows using `# pylint: disable-next=msgid` to disable a message for the following line

  Closes #1682

* Added ``redundant-u-string-prefix`` checker: Emitted when the u prefix is added to a string

  Closes #4102

* Fixed ``cell-var-from-loop`` checker: handle cell variables in comprehensions within functions,
  and function default argument expressions. Also handle basic variable shadowing.

  Closes #2846
  Closes #3107

* Fixed bug with ``cell-var-from-loop`` checker: it no longer has false negatives when
  both ``unused-variable`` and ``used-before-assignment`` are disabled.

* Fix false positive for ``invalid-all-format`` if the list or tuple builtin functions are used

  Closes #4711

* Config files can now contain environment variables

  Closes #3839

* Fix false-positive ``used-before-assignment`` with an assignment expression in a ``Return`` node

  Closes #4828

* Added ``use-sequence-for-iteration``: Emitted when iterating over an in-place defined ``set``.

* ``CodeStyleChecker``

  * Limit ``consider-using-tuple`` to be emitted only for in-place defined ``lists``.

  * Emit ``consider-using-tuple`` even if list contains a ``starred`` expression.

* Ignore decorators lines by similarities checker when ignore signatures flag enabled

  Closes #4839

* Allow ``true`` and ``false`` values in ``pylintrc`` for better compatibility with ``toml`` config.

* Class methods' signatures are ignored the same way as functions' with similarities "ignore-signatures" option enabled

  Closes #4653

* Improve performance when inferring ``Call`` nodes, by utilizing caching.

* Improve error message for invalid-metaclass when the node is an Instance.
