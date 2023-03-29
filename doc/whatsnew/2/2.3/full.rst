Full changelog
==============

What's New in Pylint 2.3.0?
---------------------------
Release date: 2019-02-27

* Protect against ``NonDeducibleTypeHierarchy`` when calling semi-private ``is_subtype``

  ``astroid.helpers.is_subtype`` raises ``NonDeducibleTypeHierarchy`` when it cannot infer
  the base classes of the given types, but that makes sense in its context given that
  the method is mostly used to inform the inference process about the hierarchy of classes.
  Doesn't make that much sense for ``pylint`` itself, which is why we're handling the
  exception here, rather than in ``astroid``

  Closes pylint-dev/astroid#644

* Added a new command line option ``list-groups`` for listing all the check groups ``pylint`` knows about.

* Allow ``BaseException`` for emitting ``broad-except``, just like ``Exception``.

  Closes #2741

* Fixed a crash that occurred for ``bad-str-strip-call`` when ``strip()`` received ``None``

  Closes #2743

* Don't emit ``*-not-iterating`` checks for builtins consumed by ``itertools``

  Closes #2731

* Fix a crash caused by iterating over ``Uninferable`` in a string formatting check.

  Closes #2727

* Fixed false positives for ``no-self-argument`` and ``unsubscriptable-object`` when using ``__class_getitem__`` (new in Python 3.7)

  Closes #2416

* Support ``Ellipsis`` as a synonym for ``pass`` statements.

  Closes #2718

* ``fixme`` gets triggered only on comments.

  Closes #2321

* Fixed a false positive for ``unused-variable`` and ``nonlocal`` assignments

  Closes #2671

* Added ``load_configuration()`` hook for plugins

  New optional hook for plugins is added: ``load_configuration()``.
  This hook is executed after configuration is loaded to prevent
  overwriting plugin specific configuration via user-based
  configuration.

  Closes #2635

* Fix missing-raises-doc false positive (W9006)

  Closes #1502

* Exempt starred unpacking from ``*-not-iterating`` Python 3 checks

  Closes #2651

* Make ``compare-to-zero`` less zealous by checking against equality and identity

  Closes #2645

* Add ``no-else-raise`` warning (R1720)

  Closes #2558

* Exempt ``yield from`` from ``*-not-iterating`` Python 3 checks.

  Closes #2643

* Fix incorrect generation of ``no-else-return`` warnings (R1705)

  Fixed issue where ``if`` statements with nested ``if`` statements
  were incorrectly being flagged as ``no-else-return`` in some cases and
  not being flagged as ``no-else-return`` in other cases.  Added tests
  for verification and updated pylint source files to eliminate newly
  exposed warnings.

* Fix false positive with ``not-async-context-manager`` caused by not understanding ``contextlib.asynccontextmanager``

  Closes #2440

* Refactor ``bad-reversed-sequence`` to account for more objects that can define ``__reversed__``

  One such object would be an enum class, for which ``__reversed__`` yields each individual enum.
  As such, the check for ``bad-reversed-sequence`` needs to not differentiate between classes
  and instances when it comes for checking of ``__reversed__`` presence.

  Closes #2598

* Added ``wrong-exception-operation``

  Used when an operation is done against an exception, but the operation
  is not valid for the exception in question. Usually emitted when having
  binary operations between exceptions in except handlers.

  Closes #2494

* ``no-member`` is emitted for enums when they lack a member

  Previously we weren't doing this because we detected a
  ``__getattr__`` implementation on the ``Enum`` class
  (and this check is skipped for classes with ``__getattr__``),
  but that is fine for Enums, given that they are inferred in a customised
  way in astroid.

  Closes #2565

* Generalize ``chained-comparison``

  Previous version incorrectly detects `a < b < c and b < d` and fails to
  detect `a < b < c and c < d`.

* Avoid popping __main__ when using multiple jobs

  Closes #2689

* Add a new option 'check-str-concat-over-line-jumps' to check 'implicit-str-concat-in-sequence'

* Fixes for the new style logging format linter.

  The number of arguments was not handled properly, leading to an always
  successful check.

* Fix false positive ``not-callable`` for uninferable properties.

* Fix false positive ``useless-else-on-loop`` if the break is deep in the else
  of an inner loop.

* Minor improvements to the help text for a few options.
