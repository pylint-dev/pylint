***************************
 What's New in Pylint 2.16
***************************

.. toctree::
   :maxdepth: 2

:Release: 2.16
:Date: 2023-02-01

Summary -- Release highlights
=============================

In 2.16.0 we added aggregation and composition understanding in ``pyreverse``, and a way to clear
the cache in between run in server mode (originally for the VS Code integration). Apart from the bug
fixes there's also a lot of new checks, and new extensions that have been asked for for a long time
that were implemented.

If you want to benefit from all the new checks load the following plugins::

    pylint.extensions.dict_init_mutate,
    pylint.extensions.dunder,
    pylint.extensions.typing,
    pylint.extensions.magic_value,

We still welcome any community effort to help review, integrate, and add good/bad examples to the doc for
<https://github.com/pylint-dev/pylint/issues/5953>`_. This should be doable without any ``pylint`` or ``astroid``
knowledge, so this is the perfect entrypoint if you want to contribute to ``pylint`` or open source without
any experience with our code!

Last but not least @clavedeluna and @nickdrozd became triagers, welcome to the team !

.. towncrier release notes start

What's new in Pylint 2.16.4?
----------------------------
Release date: 2023-03-06


False Positives Fixed
---------------------

- Fix false positive for isinstance-second-argument-not-valid-type with union
  types.

  Closes #8205 (`#8205 <https://github.com/pylint-dev/pylint/issues/8205>`_)


What's new in Pylint 2.16.3?
----------------------------
Release date: 2023-03-03


False Positives Fixed
---------------------

- Fix false positive for ``wrong-spelling-in-comment`` with class names in a
  python 2 type comment.

  Closes #8370 (`#8370 <https://github.com/pylint-dev/pylint/issues/8370>`_)



Other Bug Fixes
---------------

- Prevent emitting ``invalid-name`` for the line on which a ``global``
  statement is declared.

  Closes #8307 (`#8307 <https://github.com/pylint-dev/pylint/issues/8307>`_)


What's new in Pylint 2.16.2?
----------------------------
Release date: 2023-02-13


New Features
------------

- Add `--version` option to `pyreverse`.

  Refs #7851 (`#7851 <https://github.com/pylint-dev/pylint/issues/7851>`_)



False Positives Fixed
---------------------

- Fix false positive for ``used-before-assignment`` when
  ``typing.TYPE_CHECKING`` is used with if/elif/else blocks.

  Closes #7574 (`#7574 <https://github.com/pylint-dev/pylint/issues/7574>`_)

- Fix false positive for ``used-before-assignment`` for named expressions
  appearing after the first element in a list, tuple, or set.

  Closes #8252 (`#8252 <https://github.com/pylint-dev/pylint/issues/8252>`_)



Other Bug Fixes
---------------

- Fix ``used-before-assignment`` false positive when the walrus operator
  is used with a ternary operator in dictionary key/value initialization.

  Closes #8125 (`#8125 <https://github.com/pylint-dev/pylint/issues/8125>`_)

- Fix ``no-name-in-module`` false positive raised when a package defines a
  variable with the
  same name as one of its submodules.

  Closes #8148 (`#8148 <https://github.com/pylint-dev/pylint/issues/8148>`_)

- Fix ``nested-min-max`` suggestion message to indicate it's possible to splat
  iterable objects.

  Closes #8168 (`#8168 <https://github.com/pylint-dev/pylint/issues/8168>`_)

- Fix a crash happening when a class attribute was negated in the start
  argument of an enumerate.

  Closes #8207 (`#8207 <https://github.com/pylint-dev/pylint/issues/8207>`_)


What's new in Pylint 2.16.1?
----------------------------
Release date: 2023-02-02


Other Bug Fixes
---------------

- Fix a crash happening for python interpreter < 3.9 following a failed typing
  update.

  Closes #8161 (`#8161 <https://github.com/pylint-dev/pylint/issues/8161>`_)


What's new in Pylint 2.16.0?
----------------------------
Release date: 2023-02-01


Changes requiring user actions
------------------------------

- The ``accept-no-raise-doc`` option related to ``missing-raises-doc`` will now
  be correctly taken into account all the time.

  Pylint will no longer raise missing-raises-doc (W9006) when no exceptions are
  documented and accept-no-raise-doc is true (issue #7208).
  If you were expecting missing-raises-doc errors to be raised in that case,
  you
  will now have to add ``accept-no-raise-doc=no`` in your configuration to keep
  the same behavior.

  Closes #7208 (`#7208 <https://github.com/pylint-dev/pylint/issues/7208>`_)



New Features
------------

- Added the ``no-header`` output format. If enabled with
  ``--output-format=no-header``, it will not include the module name in the
  output.

  Closes #5362 (`#5362 <https://github.com/pylint-dev/pylint/issues/5362>`_)

- Added configuration option ``clear-cache-post-run`` to support server-like
  usage.
  Use this flag if you expect the linted files to be altered between runs.

  Refs #5401 (`#5401 <https://github.com/pylint-dev/pylint/issues/5401>`_)

- Add ``--allow-reexport-from-package`` option to configure the
  ``useless-import-alias`` check not to emit a warning if a name
  is reexported from a package.

  Closes #6006 (`#6006 <https://github.com/pylint-dev/pylint/issues/6006>`_)

- Update ``pyreverse`` to differentiate between aggregations and compositions.
  ``pyreverse`` checks if it's an Instance or a Call of an object via method
  parameters (via type hints)
  to decide if it's a composition or an aggregation.

  Refs #6543 (`#6543 <https://github.com/pylint-dev/pylint/issues/6543>`_)



New Checks
----------

- Adds a ``pointless-exception-statement`` check that emits a warning when an
  Exception is created and not assigned, raised or returned.

  Refs #3110 (`#3110 <https://github.com/pylint-dev/pylint/issues/3110>`_)

- Add a ``shadowed-import`` message for aliased imports.

  Closes #4836 (`#4836 <https://github.com/pylint-dev/pylint/issues/4836>`_)

- Add new check called ``unbalanced-dict-unpacking`` to check for unbalanced
  dict unpacking
  in assignment and for loops.

  Closes #5797 (`#5797 <https://github.com/pylint-dev/pylint/issues/5797>`_)

- Add new checker ``positional-only-arguments-expected`` to check for cases
  when
  positional-only arguments have been passed as keyword arguments.

  Closes #6489 (`#6489 <https://github.com/pylint-dev/pylint/issues/6489>`_)

- Added ``singledispatch-method`` which informs that ``@singledispatch`` should
  decorate functions and not class/instance methods.
  Added ``singledispatchmethod-function`` which informs that
  ``@singledispatchmethod`` should decorate class/instance methods and not
  functions.

  Closes #6917 (`#6917 <https://github.com/pylint-dev/pylint/issues/6917>`_)

- Rename ``broad-except`` to ``broad-exception-caught`` and add new checker
  ``broad-exception-raised``
  which will warn if general exceptions ``BaseException`` or ``Exception`` are
  raised.

  Closes #7494 (`#7494 <https://github.com/pylint-dev/pylint/issues/7494>`_)

- Added ``nested-min-max`` which flags ``min(1, min(2, 3))`` to simplify to
  ``min(1, 2, 3)``.

  Closes #7546 (`#7546 <https://github.com/pylint-dev/pylint/issues/7546>`_)

- Extended ``use-dict-literal`` to also warn about call to ``dict()`` when
  passing keyword arguments.

  Closes #7690 (`#7690 <https://github.com/pylint-dev/pylint/issues/7690>`_)

- Add ``named-expr-without-context`` check to emit a warning if a named
  expression is used outside a context like ``if``, ``for``, ``while``, or
  a comprehension.

  Refs #7760 (`#7760 <https://github.com/pylint-dev/pylint/issues/7760>`_)

- Add ``invalid-slice-step`` check to warn about a slice step value of ``0``
  for common builtin sequences.

  Refs #7762 (`#7762 <https://github.com/pylint-dev/pylint/issues/7762>`_)

- Add ``consider-refactoring-into-while-condition`` check to recommend
  refactoring when
  a while loop is defined with a constant condition with an immediate ``if``
  statement to check for ``break`` condition as a first statement.

  Closes #8015 (`#8015 <https://github.com/pylint-dev/pylint/issues/8015>`_)



Extensions
----------

- Add new extension checker ``dict-init-mutate`` that flags mutating a
  dictionary immediately
  after the dictionary was created.

  Closes #2876 (`#2876 <https://github.com/pylint-dev/pylint/issues/2876>`_)

- Added ``bad-dunder-name`` extension check, which flags bad or misspelled
  dunder methods.
  You can use the ``good-dunder-names`` option to allow specific dunder names.

  Closes #3038 (`#3038 <https://github.com/pylint-dev/pylint/issues/3038>`_)

- Added ``consider-using-augmented-assign`` check for ``CodeStyle`` extension
  which flags ``x = x + 1`` to simplify to ``x += 1``.
  This check is disabled by default. To use it, load the code style extension
  with ``load-plugins=pylint.extensions.code_style`` and add
  ``consider-using-augmented-assign`` in the ``enable`` option.

  Closes #3391 (`#3391 <https://github.com/pylint-dev/pylint/issues/3391>`_)

- Add ``magic-number`` plugin checker for comparison with constants instead of
  named constants or enums.
  You can use it with ``--load-plugins=pylint.extensions.magic_value``.

  Closes #7281 (`#7281 <https://github.com/pylint-dev/pylint/issues/7281>`_)

- Add ``redundant-typehint-argument`` message for `typing` plugin for duplicate
  assign typehints.
  Enable the plugin to enable the message with:
  ``--load-plugins=pylint.extensions.typing``.

  Closes #7636 (`#7636 <https://github.com/pylint-dev/pylint/issues/7636>`_)



False Positives Fixed
---------------------

- Fix false positive for ``unused-variable`` and ``unused-import`` when a name
  is only used in a string literal type annotation.

  Closes #3299 (`#3299 <https://github.com/pylint-dev/pylint/issues/3299>`_)

- Document a known false positive for ``useless-suppression`` when disabling
  ``line-too-long`` in a module with only comments and no code.

  Closes #3368 (`#3368 <https://github.com/pylint-dev/pylint/issues/3368>`_)

- ``trailing-whitespaces`` is no longer reported within strings.

  Closes #3822 (`#3822 <https://github.com/pylint-dev/pylint/issues/3822>`_)

- Fix false positive for ``global-variable-not-assigned`` when a global
  variable is re-assigned via an ``ImportFrom`` node.

  Closes #4809 (`#4809 <https://github.com/pylint-dev/pylint/issues/4809>`_)

- Fix false positive for ``use-maxsplit-arg`` with custom split method.

  Closes #4857 (`#4857 <https://github.com/pylint-dev/pylint/issues/4857>`_)

- Fix ``logging-fstring-interpolation`` false positive raised when logging and
  f-string with ``%s`` formatting.

  Closes #4984 (`#4984 <https://github.com/pylint-dev/pylint/issues/4984>`_)

- Fix false-positive for ``used-before-assignment`` in pattern matching
  with a guard.

  Closes #5327 (`#5327 <https://github.com/pylint-dev/pylint/issues/5327>`_)

- Fix ``use-sequence-for-iteration`` when unpacking a set with ``*``.

  Closes #5788 (`#5788 <https://github.com/pylint-dev/pylint/issues/5788>`_)

- Fix ``deprecated-method`` false positive when alias for method is similar to
  name of deprecated method.

  Closes #5886 (`#5886 <https://github.com/pylint-dev/pylint/issues/5886>`_)

- Fix false positive ``assigning-non-slot`` when a class attribute is
  re-assigned.

  Closes #6001 (`#6001 <https://github.com/pylint-dev/pylint/issues/6001>`_)

- Fix false positive for ``too-many-function-args`` when a function call is
  assigned to a class attribute inside the class where the function is defined.

  Closes #6592 (`#6592 <https://github.com/pylint-dev/pylint/issues/6592>`_)

- Fixes false positive ``abstract-method`` on Protocol classes.

  Closes #7209 (`#7209 <https://github.com/pylint-dev/pylint/issues/7209>`_)

- Pylint now understands the ``kw_only`` keyword argument for ``dataclass``.

  Closes #7290, closes #6550, closes #5857 (`#7290
  <https://github.com/pylint-dev/pylint/issues/7290>`_)

- Fix false positive for ``undefined-loop-variable`` in ``for-else`` loops that
  use a function
  having a return type annotation of ``NoReturn`` or ``Never``.

  Closes #7311 (`#7311 <https://github.com/pylint-dev/pylint/issues/7311>`_)

- Fix ``used-before-assignment`` for functions/classes defined in type checking
  guard.

  Closes #7368 (`#7368 <https://github.com/pylint-dev/pylint/issues/7368>`_)

- Fix false positive for ``unhashable-member`` when subclassing ``dict`` and
  using the subclass as a dictionary key.

  Closes #7501 (`#7501 <https://github.com/pylint-dev/pylint/issues/7501>`_)

- Fix the message for ``unnecessary-dunder-call`` for ``__aiter__`` and
  ``__aneext__``. Also
  only emit the warning when ``py-version`` >= 3.10.

  Closes #7529 (`#7529 <https://github.com/pylint-dev/pylint/issues/7529>`_)

- Fix ``used-before-assignment`` false positive when else branch calls
  ``sys.exit`` or similar terminating functions.

  Closes #7563 (`#7563 <https://github.com/pylint-dev/pylint/issues/7563>`_)

- Fix a false positive for ``used-before-assignment`` for imports guarded by
  ``typing.TYPE_CHECKING`` later used in variable annotations.

  Closes #7609 (`#7609 <https://github.com/pylint-dev/pylint/issues/7609>`_)

- Fix a false positive for ``simplify-boolean-expression`` when multiple values
  are inferred for a constant.

  Closes #7626 (`#7626 <https://github.com/pylint-dev/pylint/issues/7626>`_)

- ``unnecessary-list-index-lookup`` will not be wrongly emitted if
  ``enumerate`` is called with ``start``.

  Closes #7682 (`#7682 <https://github.com/pylint-dev/pylint/issues/7682>`_)

- Don't warn about ``stop-iteration-return`` when using ``next()`` over
  ``itertools.cycle``.

  Closes #7765 (`#7765 <https://github.com/pylint-dev/pylint/issues/7765>`_)

- Fixes ``used-before-assignment`` false positive when the walrus operator
  is used in a ternary operator.

  Closes #7779 (`#7779 <https://github.com/pylint-dev/pylint/issues/7779>`_)

- Fix ``missing-param-doc`` false positive when function parameter has an
  escaped underscore.

  Closes #7827 (`#7827 <https://github.com/pylint-dev/pylint/issues/7827>`_)

- Fixes ``method-cache-max-size-none`` false positive for methods inheriting
  from ``Enum``.

  Closes #7857 (`#7857 <https://github.com/pylint-dev/pylint/issues/7857>`_)

- ``multiple-statements`` no longer triggers for function stubs using inlined
  ``...``.

  Closes #7860 (`#7860 <https://github.com/pylint-dev/pylint/issues/7860>`_)

- Fix a false positive for ``used-before-assignment`` when a name guarded by
  ``if TYPE_CHECKING:`` is used as a type annotation in a function body and
  later re-imported in the same scope.

  Closes #7882 (`#7882 <https://github.com/pylint-dev/pylint/issues/7882>`_)

- Prevent ``used-before-assignment`` when imports guarded by ``if
  TYPE_CHECKING``
  are guarded again when used.

  Closes #7979 (`#7979 <https://github.com/pylint-dev/pylint/issues/7979>`_)

- Fixes false positive for ``try-except-raise`` with multiple exceptions in one
  except statement if exception are in different namespace.

  Closes #8051 (`#8051 <https://github.com/pylint-dev/pylint/issues/8051>`_)

- Fix ``invalid-name`` errors for ``typing_extension.TypeVar``.

  Refs #8089 (`#8089 <https://github.com/pylint-dev/pylint/issues/8089>`_)

- Fix ``no-kwoa`` false positive for context managers.

  Closes #8100 (`#8100 <https://github.com/pylint-dev/pylint/issues/8100>`_)

- Fix a false positive for ``redefined-variable-type`` when ``async`` methods
  are present.

  Closes #8120 (`#8120 <https://github.com/pylint-dev/pylint/issues/8120>`_)



False Negatives Fixed
---------------------

- Code following a call to  ``quit``,  ``exit``, ``sys.exit`` or ``os._exit``
  will be marked as `unreachable`.

  Refs #519 (`#519 <https://github.com/pylint-dev/pylint/issues/519>`_)

- Emit ``used-before-assignment`` when function arguments are redefined inside
  an inner function and accessed there before assignment.

  Closes #2374 (`#2374 <https://github.com/pylint-dev/pylint/issues/2374>`_)

- Fix a false negative for ``unused-import`` when one module used an import in
  a type annotation that was also used in another module.

  Closes #4150 (`#4150 <https://github.com/pylint-dev/pylint/issues/4150>`_)

- Flag ``superfluous-parens`` if parentheses are used during string
  concatenation.

  Closes #4792 (`#4792 <https://github.com/pylint-dev/pylint/issues/4792>`_)

- Emit ``used-before-assignment`` when relying on names only defined under
  conditions always testing false.

  Closes #4913 (`#4913 <https://github.com/pylint-dev/pylint/issues/4913>`_)

- ``consider-using-join`` can now be emitted for non-empty string separators.

  Closes #6639 (`#6639 <https://github.com/pylint-dev/pylint/issues/6639>`_)

- Emit ``used-before-assignment`` for further imports guarded by
  ``TYPE_CHECKING``

  Previously, this message was only emitted for imports guarded directly under
  ``TYPE_CHECKING``, not guarded two if-branches deep, nor when
  ``TYPE_CHECKING``
  was imported from ``typing`` under an alias.

  Closes #7539 (`#7539 <https://github.com/pylint-dev/pylint/issues/7539>`_)

- Fix a false negative for ``unused-import`` when a constant inside
  ``typing.Annotated`` was treated as a reference to an import.

  Closes #7547 (`#7547 <https://github.com/pylint-dev/pylint/issues/7547>`_)

- ``consider-using-any-or-all`` message will now be raised in cases when
  boolean is initialized, reassigned during loop, and immediately returned.

  Closes #7699 (`#7699 <https://github.com/pylint-dev/pylint/issues/7699>`_)

- Extend ``invalid-slice-index`` to emit an warning for invalid slice indices
  used with string and byte sequences, and range objects.

  Refs #7762 (`#7762 <https://github.com/pylint-dev/pylint/issues/7762>`_)

- Fixes ``unnecessary-list-index-lookup`` false negative when ``enumerate`` is
  called with ``iterable`` as a kwarg.

  Closes #7770 (`#7770 <https://github.com/pylint-dev/pylint/issues/7770>`_)

- ``no-else-return`` or ``no-else-raise`` will be emitted if ``except`` block
  always returns or raises.

  Closes #7788 (`#7788 <https://github.com/pylint-dev/pylint/issues/7788>`_)

- Fix ``dangerous-default-value`` false negative when ``*`` is used.

  Closes #7818 (`#7818 <https://github.com/pylint-dev/pylint/issues/7818>`_)

- ``consider-using-with`` now triggers for ``pathlib.Path.open``.

  Closes #7964 (`#7964 <https://github.com/pylint-dev/pylint/issues/7964>`_)



Other Bug Fixes
---------------

- Fix bug in detecting ``unused-variable`` when iterating on variable.

  Closes #3044 (`#3044 <https://github.com/pylint-dev/pylint/issues/3044>`_)

- Fix bug in scanning of names inside arguments to ``typing.Literal``.
  See https://peps.python.org/pep-0586/#literals-enums-and-forward-references
  for details.

  Refs #3299 (`#3299 <https://github.com/pylint-dev/pylint/issues/3299>`_)

- Update ``disallowed-name`` check to flag module-level variables.

  Closes #3701 (`#3701 <https://github.com/pylint-dev/pylint/issues/3701>`_)

- Pylint will no longer deadlock if a parallel job is killed but fail
  immediately instead.

  Closes #3899 (`#3899 <https://github.com/pylint-dev/pylint/issues/3899>`_)

- Fix ignored files being linted when passed on stdin.

  Closes #4354 (`#4354 <https://github.com/pylint-dev/pylint/issues/4354>`_)

- Fix ``no-member`` false negative when augmented assign is done manually,
  without ``+=``.

  Closes #4562 (`#4562 <https://github.com/pylint-dev/pylint/issues/4562>`_)

- Any assertion on a populated tuple will now receive a ``assert-on-tuple``
  warning.

  Closes #4655 (`#4655 <https://github.com/pylint-dev/pylint/issues/4655>`_)

- ``missing-return-doc``, ``missing-raises-doc`` and ``missing-yields-doc`` now
  respect
  the ``no-docstring-rgx`` option.

  Closes #4743 (`#4743 <https://github.com/pylint-dev/pylint/issues/4743>`_)

- Update ``reimported`` help message for clarity.

  Closes #4836 (`#4836 <https://github.com/pylint-dev/pylint/issues/4836>`_)

- ``consider-iterating-dictionary`` will no longer be raised if bitwise
  operations are used.

  Closes #5478 (`#5478 <https://github.com/pylint-dev/pylint/issues/5478>`_)

- Using custom braces in ``msg-template`` will now work properly.

  Closes #5636 (`#5636 <https://github.com/pylint-dev/pylint/issues/5636>`_)

- Pylint will now filter duplicates given to it before linting. The output
  should
  be the same whether a file is given/discovered multiple times or not.

  Closes #6242, #4053 (`#6242 <https://github.com/pylint-dev/pylint/issues/6242>`_)

- Remove ``__index__`` dunder method call from ``unnecessary-dunder-call``
  check.

  Closes #6795 (`#6795 <https://github.com/pylint-dev/pylint/issues/6795>`_)

- Fixed handling of ``--`` as separator between positional arguments and flags.
  This was not actually fixed in 2.14.5.

  Closes #7003, Refs #7096 (`#7003
  <https://github.com/pylint-dev/pylint/issues/7003>`_)

- Don't crash on ``OSError`` in config file discovery.

  Closes #7169 (`#7169 <https://github.com/pylint-dev/pylint/issues/7169>`_)

- Messages sent to reporter are now copied so a reporter cannot modify the
  message sent to other reporters.

  Closes #7214 (`#7214 <https://github.com/pylint-dev/pylint/issues/7214>`_)

- Fixed a case where custom plugins specified by command line could silently
  fail.

  Specifically, if a plugin relies on the ``init-hook`` option changing
  ``sys.path`` before
  it can be imported, this will now emit a ``bad-plugin-value`` message. Before
  this
  change, it would silently fail to register the plugin for use, but would load
  any configuration, which could have unintended effects.

  Fixes part of #7264. (`#7264 <https://github.com/pylint-dev/pylint/issues/7264>`_)

- Update ``modified_iterating`` checker to fix a crash with ``for`` loops on
  empty list.

  Closes #7380 (`#7380 <https://github.com/pylint-dev/pylint/issues/7380>`_)

- Update wording for ``arguments-differ`` and ``arguments-renamed`` to clarify
  overriding object.

  Closes #7390 (`#7390 <https://github.com/pylint-dev/pylint/issues/7390>`_)

- ``disable-next`` is now correctly scoped to only the succeeding line.

  Closes #7401 (`#7401 <https://github.com/pylint-dev/pylint/issues/7401>`_)

- Fixed a crash in the ``unhashable-member`` checker when using a ``lambda`` as
  a dict key.

  Closes #7453 (`#7453 <https://github.com/pylint-dev/pylint/issues/7453>`_)

- Add ``mailcap`` to deprecated modules list.

  Closes #7457 (`#7457 <https://github.com/pylint-dev/pylint/issues/7457>`_)

- Fix a crash in the ``modified-iterating-dict`` checker involving instance
  attributes.

  Closes #7461 (`#7461 <https://github.com/pylint-dev/pylint/issues/7461>`_)

- ``invalid-class-object`` does not crash anymore when ``__class__`` is
  assigned alongside another variable.

  Closes #7467 (`#7467 <https://github.com/pylint-dev/pylint/issues/7467>`_)

- ``--help-msg`` now accepts a comma-separated list of message IDs again.

  Closes #7471 (`#7471 <https://github.com/pylint-dev/pylint/issues/7471>`_)

- Allow specifying non-builtin exceptions in the ``overgeneral-exception``
  option
  using an exception's qualified name.

  Closes #7495 (`#7495 <https://github.com/pylint-dev/pylint/issues/7495>`_)

- Report ``no-self-argument`` rather than ``no-method-argument`` for methods
  with variadic arguments.

  Closes #7507 (`#7507 <https://github.com/pylint-dev/pylint/issues/7507>`_)

- Fixed an issue where ``syntax-error`` couldn't be raised on files with
  invalid encodings.

  Closes #7522 (`#7522 <https://github.com/pylint-dev/pylint/issues/7522>`_)

- Fix false positive for ``redefined-outer-name`` when aliasing ``typing``
  e.g. as ``t`` and guarding imports under ``t.TYPE_CHECKING``.

  Closes #7524 (`#7524 <https://github.com/pylint-dev/pylint/issues/7524>`_)

- Fixed a crash of the ``modified_iterating`` checker when iterating on a set
  defined as a class attribute.

  Closes #7528 (`#7528 <https://github.com/pylint-dev/pylint/issues/7528>`_)

- Use ``py-version`` to determine if a message should be emitted for messages
  defined with ``max-version`` or ``min-version``.

  Closes #7569 (`#7569 <https://github.com/pylint-dev/pylint/issues/7569>`_)

- Improve ``bad-thread-instantiation`` check to warn if ``target`` is not
  passed in as a keyword argument
  or as a second argument.

  Closes #7570 (`#7570 <https://github.com/pylint-dev/pylint/issues/7570>`_)

- Fixes edge case of custom method named ``next`` raised an astroid error.

  Closes #7610 (`#7610 <https://github.com/pylint-dev/pylint/issues/7610>`_)

- Fixed a multi-processing crash that prevents using any more than 1 thread on
  MacOS.

  The returned module objects and errors that were cached by the linter plugin
  loader
  cannot be reliably pickled. This means that ``dill`` would throw an error
  when
  attempting to serialise the linter object for multi-processing use.

  Closes #7635. (`#7635 <https://github.com/pylint-dev/pylint/issues/7635>`_)

- Fix crash that happened when parsing files with unexpected encoding starting
  with 'utf' like ``utf13``.

  Closes #7661 (`#7661 <https://github.com/pylint-dev/pylint/issues/7661>`_)

- Fix a crash when a child class with an ``__init__`` method inherits from a
  parent class with an ``__init__`` class attribute.

  Closes #7742 (`#7742 <https://github.com/pylint-dev/pylint/issues/7742>`_)

- Fix ``valid-metaclass-classmethod-first-arg`` default config value from "cls"
  to "mcs"
  which would cause both a false-positive and false-negative.

  Closes #7782 (`#7782 <https://github.com/pylint-dev/pylint/issues/7782>`_)

- Fixes a crash in the ``unnecessary_list_index_lookup`` check when using
  ``enumerate`` with ``start`` and a class attribute.

  Closes #7821 (`#7821 <https://github.com/pylint-dev/pylint/issues/7821>`_)

- Fixes a crash in ``stop-iteration-return`` when the ``next`` builtin is
  called without arguments.

  Closes #7828 (`#7828 <https://github.com/pylint-dev/pylint/issues/7828>`_)

- When pylint exit due to bad arguments being provided the exit code will now
  be the expected ``32``.

  Refs #7931 (`#7931 <https://github.com/pylint-dev/pylint/issues/7931>`_)

- Fixes a ``ModuleNotFound`` exception when running pylint on a Django project
  with the ``pylint_django`` plugin enabled.

  Closes #7938 (`#7938 <https://github.com/pylint-dev/pylint/issues/7938>`_)

- Fixed a crash when inferring a value and using its qname on a slice that was
  being incorrectly called.

  Closes #8067 (`#8067 <https://github.com/pylint-dev/pylint/issues/8067>`_)

- Use better regex to check for private attributes.

  Refs #8081 (`#8081 <https://github.com/pylint-dev/pylint/issues/8081>`_)

- Fix issue with new typing Union syntax in runtime context for Python 3.10+.

  Closes #8119 (`#8119 <https://github.com/pylint-dev/pylint/issues/8119>`_)



Other Changes
-------------

- Pylint now provides basic support for Python 3.11.

  Closes #5920 (`#5920 <https://github.com/pylint-dev/pylint/issues/5920>`_)

- Update message for ``abstract-method`` to include child class name.

  Closes #7124 (`#7124 <https://github.com/pylint-dev/pylint/issues/7124>`_)

- Update Pyreverse's dot and plantuml printers to detect when class methods are
  abstract and show them with italic font.
  For the dot printer update the label to use html-like syntax.

  Closes #7346 (`#7346 <https://github.com/pylint-dev/pylint/issues/7346>`_)

- The ``docparams`` extension now considers typing in Numpy style docstrings
  as "documentation" for the ``missing-param-doc`` message.

  Refs #7398 (`#7398 <https://github.com/pylint-dev/pylint/issues/7398>`_)

- Relevant ``DeprecationWarnings`` are now raised with ``stacklevel=2``, so
  they have the callsite attached in the message.

  Closes #7463 (`#7463 <https://github.com/pylint-dev/pylint/issues/7463>`_)

- Add a ``minimal`` option to ``pylint-config`` and its toml generator.

  Closes #7485 (`#7485 <https://github.com/pylint-dev/pylint/issues/7485>`_)

- Add method name to the error messages of ``no-method-argument`` and
  ``no-self-argument``.

  Closes #7507 (`#7507 <https://github.com/pylint-dev/pylint/issues/7507>`_)

- Prevent leaving the pip install cache in the Docker image.

  Refs #7544 (`#7544 <https://github.com/pylint-dev/pylint/issues/7544>`_)

- Add a keyword-only ``compare_constants`` argument to ``safe_infer``.

  Refs #7626 (`#7626 <https://github.com/pylint-dev/pylint/issues/7626>`_)

- Add ``default_enabled`` option to optional message dict. Provides an option
  to disable a checker message by default.
  To use a disabled message, the user must enable it explicitly by adding the
  message to the ``enable`` option.

  Refs #7629 (`#7629 <https://github.com/pylint-dev/pylint/issues/7629>`_)

- Sort ``--generated-rcfile`` output.

  Refs #7655 (`#7655 <https://github.com/pylint-dev/pylint/issues/7655>`_)

- epylint is now deprecated and will be removed in pylint 3.0.0. All emacs and
  flymake related
  files were removed and their support will now happen in an external
  repository :
  https://github.com/emacsorphanage/pylint.

  Closes #7737 (`#7737 <https://github.com/pylint-dev/pylint/issues/7737>`_)

- Adds test for existing preferred-modules configuration functionality.

  Refs #7957 (`#7957 <https://github.com/pylint-dev/pylint/issues/7957>`_)



Internal Changes
----------------

- Add and fix regression tests for plugin loading.

  This shores up the tests that cover the loading of custom plugins as affected
  by any changes made to the ``sys.path`` during execution of an ``init-hook``.
  Given the existing contract of allowing plugins to be loaded by fiddling with
  the path in this way, this is now the last bit of work needed to close Github
  issue #7264.

  Closes #7264 (`#7264 <https://github.com/pylint-dev/pylint/issues/7264>`_)
