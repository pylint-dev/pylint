Full changelog
==============

What's New in Pylint 2.5.3?
---------------------------
Release date: 2020-06-8

* Fix a regression where disable comments that have checker names with numbers in them are not parsed correctly

  Closes #3666

* ``property-with-parameters`` properly handles abstract properties

  Closes #3600

* ``continue-in-finally`` no longer emitted on Python 3.8 where it's now valid

  Closes #3612

* Fix a regression where messages with dash are not fully parsed

  Closes #3604

* In a TOML configuration file, it's now possible to use rich (non-string) types, such as list, integer or boolean instead of strings. For example, one can now define a *list* of message identifiers to enable like this::

    enable = [
        "use-symbolic-message-instead",
        "useless-suppression",
    ]

  Closes #3538

* Fix a regression where the score was not reported with multiple jobs

  Closes #3547

* Protect against ``AttributeError`` when checking ``cell-var-from-loop``

  Closes #3646


What's New in Pylint 2.5.2?
---------------------------
Release date: 2020-05-05

* ``pylint.Run`` accepts ``do_exit`` as a deprecated parameter

  Closes #3590


What's New in Pylint 2.5.1?
---------------------------
Release date: 2020-05-05

* Fix a crash in ``method-hidden`` lookup for unknown base classes

  Closes #3527

* Revert pylint.Run's ``exit`` parameter to ``do_exit``

  This has been inadvertently changed several releases ago to ``do_exit``.

  Closes #3533

* ``no-value-for-parameter`` variadic detection has improved for assign statements

  Closes #3563

* Allow package files to be properly discovered with multiple jobs

  Closes #3524

* Allow linting directories without ``__init__.py`` which was a regression in 2.5.

  Closes #3528


What's New in Pylint 2.5.0?
---------------------------
Release date: 2020-04-27

* Fix a false negative for ``undefined-variable`` when using class attribute in comprehension.

  Closes #3494

* Fix a false positive for ``undefined-variable`` when using class attribute in decorator or as type hint.

  Closes #511
  Closes #1976

* Remove HTML quoting of messages in JSON output.

  Closes #2769

* Adjust the ``invalid-name`` rule to work with non-ASCII identifiers and add the ``non-ascii-name`` rule.

  Closes #2725

* Positional-only arguments are taken in account for ``useless-super-delegation``

* ``unidiomatic-typecheck`` is no longer emitted for ``in`` and ``not in`` operators

  Closes #3337

* Positional-only argument annotations are taken in account for ``unused-import``

  Closes #3462

* Add a command to list available extensions.

* Allow used variables to be properly consumed when different checks are enabled / disabled

  Closes #3445

* Fix dangerous-default-value rule to account for keyword argument defaults

  Closes #3373

* Fix a false positive of ``self-assigning-variable`` on tuple unpacking.

  Closes #3433

* ``no-self-use`` is no longer emitted for typing stubs.

  Closes #3439

* Fix a false positive for ``undefined-variable`` when ``__class__`` is used

  Closes #3090

* Emit ``invalid-name`` for variables defined in loops at module level.

  Closes #2695

* Add a check for cases where the second argument to ``isinstance`` is not a type.

  Closes #3308

* Add 'notes-rgx' option, to be used for fixme check.

  Closes #2874

* ``function-redefined`` exempts function redefined on a condition.

  Closes #2410

* ``typing.overload`` functions are exempted from docstring checks

  Closes #3350

* Emit ``invalid-overridden-method`` for improper async def overrides.

  Closes #3355

* Do not allow ``python -m pylint ...`` to import user code

  ``python -m pylint ...`` adds the current working directory as the first element
  of ``sys.path``. This opens up a potential security hole where ``pylint`` will import
  user level code as long as that code resides in modules having the same name as stdlib
  or pylint's own modules.

  Closes #3386

* Add ``dummy-variables-rgx`` option for ``_redeclared-assigned-name`` check.

  Closes #3341

* Fixed graph creation for relative paths

* Add a check for asserts on string literals.

  Closes #3284

* ``not in`` is considered iterating context for some of the Python 3 porting checkers.

* A new check ``inconsistent-quotes`` was added.

* Add a check for non string assignment to __name__ attribute.

  Closes #583

* ``__pow__``, ``__imatmul__``, ``__trunc__``, ``__floor__``, and ``__ceil__`` are recognized as special method names.

  Closes #3281

* Added errors for protocol functions when invalid return types are detected.
  E0304 (invalid-bool-returned): __bool__ did not return a bool
  E0305 (invalid-index-returned): __index__ did not return an integer
  E0306 (invalid-repr-returned): __repr__ did not return a string
  E0307 (invalid-str-returned): __str__ did not return a string
  E0308 (invalid-bytes-returned): __bytes__ did not return a string
  E0309 (invalid-hash-returned): __hash__ did not return an integer
  E0310 (invalid-length-hint-returned): __length_hint__ did not return a non-negative integer
  E0311 (invalid-format-returned): __format__ did not return a string
  E0312 (invalid-getnewargs-returned): __getnewargs__ did not return a tuple
  E0313 (invalid-getnewargs-ex-returned): __getnewargs_ex__ did not return a tuple of the form (tuple, dict)

  Closes #560

* ``missing-*-docstring`` can look for ``__doc__`` assignments.

  Closes #3301

* ``undefined-variable`` can now find undefined loop iterables

  Closes #498

* ``safe_infer`` can infer a value as long as all the paths share the same type.

  Closes #2503

* Add a --fail-under <score> flag, also configurable in a .pylintrc file. If the final score is more than the specified score, it's considered a success and pylint exits with exitcode 0. Otherwise, it's considered a failure and pylint exits with its current exitcode based on the messages issued.

  Closes #2242

* Don't emit ``line-too-long`` for multilines when ``disable=line-too-long`` comment stands at their end

  Closes #2957

* Fixed an ``AttributeError`` caused by improper handling of ``dataclasses`` inference in ``pyreverse``

  Closes #3256

* Do not exempt bare except from ``undefined-variable`` and similar checks

  If a node was wrapped in a ``TryExcept``, ``pylint`` was taking a hint
  from the except handler when deciding to emit or not a message.
  We were treating bare except as a fully fledged ignore but only
  the corresponding exceptions should be handled that way (e.g. ``NameError`` or ``ImportError``)

  Closes #3235

* No longer emit ``assignment-from-no-return`` when a function only raises an exception

  Closes #3218

* Allow import aliases to exempt ``import-error`` when used in type annotations.

  Closes #3178

* ``Ellipsis` is exempted from ``multiple-statements`` for function overloads.

  Closes #3224

* No longer emit ``invalid-name`` for non-constants found at module level.

  Pylint was taking the following statement from PEP-8 too far, considering
  all module level variables as constants, which is not what the statement is saying:

  `Constants are usually defined on a module level and written in
  all capital letters with underscores separating words.`

  Closes #3111
  Closes #3132

* Allow ``implicit-str-concat-in-sequence`` to be emitted for string juxtaposition

  Closes #3030

* ``implicit-str-concat-in-sequence`` was renamed ``implicit-str-concat``

* The ``json`` reporter no longer bypasses ``redirect_stdout``.

  Closes #3227

* Move ``NoFileError``, ``OutputLine``, ``FunctionalTestReporter``,
  ``FunctionalTestFile``, ``LintModuleTest`` and related methods from
  ``test_functional.py`` to ``pylint.testutils`` to help testing for 3rd
  party pylint plugins.

* Can read config from a setup.cfg or pyproject.toml file.

  Closes #617

* Fix exception-escape false positive with generators

  Closes #3128

* ``inspect.getargvalues`` is no longer marked as deprecated.

* A new check ``f-string-without-interpolation`` was added

  Closes #3190

* Flag mutable ``collections.*`` utilities as dangerous defaults

  Closes #3183

* ``docparams`` extension supports multiple types in raises sections.

  Multiple types can also be separated by commas in all valid sections.

  Closes #2729

* Allow parallel linting when run under Prospector

* Fixed false positives of ``method-hidden`` when a subclass defines the method that is being hidden.

  Closes #414

* Python 3 porting mode is 30-50% faster on most codebases

* Python 3 porting mode no longer swallows syntax errors

  Closes #2956

* Pass the actual PyLinter object to sub processes to allow using custom
  PyLinter classes.

  PyLinter object (and all its members except reporter) needs to support
  pickling so the PyLinter object can be passed to worker processes.

* Clean up setup.py

  Make pytest-runner a requirement only if running tests, similar to McCabe.

  Clean up the setup.py file, resolving a number of warnings around it.

* Handle SyntaxError in files passed via ``--from-stdin`` option

  Pylint no longer outputs a traceback, if a file, read from stdin,
  contains a syntaxerror.

* Fix uppercase style to disallow 3+ uppercase followed by lowercase.

* Fixed ``undefined-variable`` and ``unused-import`` false positives
  when using a metaclass via an attribute.

  Closes #1603

* Emit ``unused-argument`` for functions that partially uses their argument list before raising an exception.

  Closes #3246

* Fixed ``broad_try_clause`` extension to check try/finally statements and to
  check for nested statements (e.g., inside of an ``if`` statement).

* Recognize classes explicitly inheriting from ``abc.ABC`` or having an
  ``abc.ABCMeta`` metaclass as abstract. This makes them not trigger W0223.

  Closes #3098

* Fix overzealous ``arguments-differ`` when overridden function uses variadics

  No message is emitted if the overriding function provides positional or
  keyword variadics in its signature that can feasibly accept and pass on
  all parameters given by the overridden function.

  Closes #1482
  Closes #1553

* Multiple types of string formatting are allowed in logging functions.

  The ``logging-fstring-interpolation`` message has been brought back to allow
  multiple types of string formatting to be used.

  Closes #3361
