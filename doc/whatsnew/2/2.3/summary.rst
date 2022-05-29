:Release: 2.3
:Date: 2019-02-27


Summary -- Release highlights
=============================

* This release improves the performance of the 2.X series after it was affected by a performance regression a couple of releases ago.

New checkers
============

* We added a new check message ``wrong-exception-operation``.
  This is emitted when an operation is done against an exception, but the operation
  is not valid for the exception in question. Usually emitted when having
  binary operations between exceptions in except handlers.

  Closes #2494

* We added a new ``no-else-raise`` warning similar to ``no-else-return``

  Closes #2558

* We added a new option ``check-str-concat-over-line-jumps`` to check
  ``implicit-str-concat-in-sequence`` over multiple lines.


Other Changes
=============

Quite a lot of bug fixes and improvements went into this release, here's a handful of them.
For the full changes, check the full changelog.

* We no longer emit ``*-not-iterating`` checks for builtins consumed by ``itertools``

* We fixed some false positives for ``no-self-argument`` and ``unsubscriptable-object``
  when using ``__class_getitem__`` (new in Python 3.7)

* ``pylint`` now supports ``Ellipsis`` as a synonym for ``pass`` statements.

* ``fixme`` gets triggered only on comments.

* ``pylint`` exempts starred unpacking from ``*-not-iterating`` Python 3 checks.

* ``compare-to-zero`` is now less zealous by checking against equality and identity.

*``yield from`` is exempted from ``*-not-iterating`` Python 3 checks.

* A false positive with ``not-async-context-manager`` caused by not understanding
  ``contextlib.asynccontextmanager`` was fixed.

* We refactored ``bad-reversed-sequence`` to account for more objects that can define ``__reversed__``.

* ``no-member`` is now emitted for enums when they lack a member.

* Plugins can now use the ``load_configuration()`` hook.
  This hook is executed after configuration is loaded to prevent overwriting plugin
  specific configuration via user-based configuration.

* There's a new command line option ``list-groups`` for listing all the check groups
  ``pylint`` knows about. This is useful to know what groups you can disable or enable
  individually.
