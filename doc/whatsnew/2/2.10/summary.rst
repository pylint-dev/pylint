:Release: 2.10
:Date: 2021-08-20

Summary -- Release highlights
=============================

In 2.10, we added several new default check, like ``unspecified-encoding``, ``forgotten-debug-statement`` or
``use-dict-literal``. There's also a few opinionated optional one. You can now forbid while loop or
profess your exclusive love of ternary expressions publicly. We promise you hours of arguing fun with
your whole team if you add those to your configuration.

We've also fixed some long standing bugs, false positives, or missing options like ``ignore-signature`` that
will now work on inner function's signatures.

A new option to disable the next line, ``disable-next``, has been added. It's also possible to export
colored diagrams, and plantuml diagram using pyreverse. ``PYLINT_HOME`` is now ``XDG_CACHE_HOME`` if not set.

The performance of the similarity checker has been improved, as well as several small performance fixes.

We're going to continue working on improving performance during 2.11. We're also going to finalize
a new ``possible-forgotten-f-prefix`` check that had too much false positives at release time.
Check the `possible-forgotten-f-prefix`_ issue if you want to provide knowledge or use case :)

.. _possible-forgotten-f-prefix: https://github.com/pylint-dev/pylint/pull/4787

New checkers
============

* Added ``unspecified-encoding``: Emitted when open() is called without specifying an encoding

  Closes #3826

* Added ``use-list-literal``: Emitted when ``list()`` is called with no arguments instead of using ``[]``

  Closes #4365

* Added ``use-dict-literal``: Emitted when ``dict()`` is called with no arguments instead of using ``{}``

  Closes #4365

* Added ``forgotten-debug-statement``: Emitted when ``breakpoint``, ``pdb.set_trace`` or ``sys.breakpointhook`` calls are found

  Closes #3692

* Added ``use-sequence-for-iteration``: Emitted when iterating over an in-place defined ``set``.


* Added ``format-string-without-interpolation`` checker: Emitted when formatting is applied to a string without any variables to be replaced

  Closes #4042

* Added ``redundant-u-string-prefix`` checker: Emitted when the u prefix is added to a string

  Closes #4102

Extensions
==========

* ``CodeStyleChecker``

  * Limit ``consider-using-tuple`` to be emitted only for in-place defined ``lists``.

  * Emit ``consider-using-tuple`` even if list contains a ``starred`` expression.

* Added optional extension ``consider-ternary-expression``: Emitted whenever a variable is assigned in both branches of an if/else block.

  Closes # 4366

* Added optional extension ``while-used``: Emitted whenever a ``while`` loop is used.

  Closes # 4367

Other Changes
=============

* pyreverse now permit to produce colored generated diagram by using the ``colorized`` option.

* Pyreverse - add output in PlantUML format

* ``consider-using-with`` is no longer triggered if a context manager is returned from a function.

* pylint does not crash with a traceback anymore when a file is problematic. It
  creates a template text file for opening an issue on the bug tracker instead.
  The linting can go on for other non problematic files instead of being impossible.

* Pyreverse - Show class has-a relationships inferred from type-hints

* Performance of the Similarity checker has been improved.

* Added ``time.clock`` to deprecated functions/methods for python 3.3

* Added ``ignored-parents`` option to the design checker to ignore specific
  classes from the ``too-many-ancestors`` check (R0901).

* Don't emit ``no-member`` error if guarded behind if statement.

  Refs #1162
  Closes #1990
  Closes #4168

* Fix false positives for ``superfluous-parens`` with walrus operator, ternary operator and inside list comprehension.

  Closes #2818
  Closes #3249
  Closes #3608
  Closes #4346

* Refactor of ``--list-msgs`` & ``--list-msgs-enabled``: both options now show whether messages are emittable with the current interpreter.

  Closes #4778

* Fix false negative for ``used-before-assignment`` when the variable is assigned
  in an exception handler, but used outside of the handler.

  Closes #626

* Added ``disable-next`` option: allows using `# pylint: disable-next=msgid` to disable a message for the following line

  Closes #1682

* Fixed ``cell-var-from-loop`` checker: handle cell variables in comprehensions within functions,
  and function default argument expressions. Also handle basic variable shadowing.

  Closes #2846
  Closes #3107

* Fixed bug with ``cell-var-from-loop`` checker: it no longer has false negatives when
  both ``unused-variable`` and ``used-before-assignment`` are disabled.

* Class methods' signatures are now ignored the same way as functions' with similarities "ignore-signatures" option enabled

  Closes #4653
