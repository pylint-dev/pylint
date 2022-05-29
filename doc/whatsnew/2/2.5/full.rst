Full changelog
==============

What's New in Pylint 2.5.3?
---------------------------
Release date: 2020-06-8

* Fix a regression where disable comments that have checker names with numbers in them are not parsed correctly

  Close #3666

* ``property-with-parameters`` properly handles abstract properties

  Close #3600

* ``continue-in-finally`` no longer emitted on Python 3.8 where it's now valid

  Close #3612

* Fix a regression where messages with dash are not fully parsed

  Close #3604

* In a TOML configuration file, it's now possible to use rich (non-string) types, such as list, integer or boolean instead of strings. For example, one can now define a *list* of message identifiers to enable like this::

    enable = [
        "use-symbolic-message-instead",
        "useless-suppression",
    ]

  Close #3538

* Fix a regression where the score was not reported with multiple jobs

  Close #3547

* Protect against ``AttributeError`` when checking ``cell-var-from-loop``

  Close #3646


What's New in Pylint 2.5.2?
---------------------------
Release date: 2020-05-05

* ``pylint.Run`` accepts ``do_exit`` as a deprecated parameter

  Close #3590


What's New in Pylint 2.5.1?
---------------------------
Release date: 2020-05-05

* Fix a crash in ``method-hidden`` lookup for unknown base classes

  Close #3527

* Revert pylint.Run's ``exit`` parameter to ``do_exit``

  This has been inadvertently changed several releases ago to ``do_exit``.

  Close #3533

* ``no-value-for-parameter`` variadic detection has improved for assign statements

  Close #3563

* Allow package files to be properly discovered with multiple jobs

  Close #3524

* Allow linting directories without ``__init__.py`` which was a regression in 2.5.

  Close #3528


What's New in Pylint 2.5.0?
---------------------------
Release date: 2020-04-27

* Fix a false negative for ``undefined-variable`` when using class attribute in comprehension.

  Close #3494

* Fix a false positive for ``undefined-variable`` when using class attribute in decorator or as type hint.

  Close #511
  Close #1976

* Remove HTML quoting of messages in JSON output.

  Close #2769

* Adjust the ``invalid-name`` rule to work with non-ASCII identifiers and add the ``non-ascii-name`` rule.

  Close #2725

* Positional-only arguments are taken in account for ``useless-super-delegation``

* ``unidiomatic-typecheck`` is no longer emitted for ``in`` and ``not in`` operators

  Close #3337

* Positional-only argument annotations are taken in account for ``unused-import``

  Close #3462

* Add a command to list available extensions.

* Allow used variables to be properly consumed when different checks are enabled / disabled

  Close #3445

* Fix dangerous-default-value rule to account for keyword argument defaults

  Close #3373

* Fix a false positive of ``self-assigning-variable`` on tuple unpacking.

  Close #3433

* ``no-self-use`` is no longer emitted for typing stubs.

  Close #3439

* Fix a false positive for ``undefined-variable`` when ``__class__`` is used

  Close #3090

* Emit ``invalid-name`` for variables defined in loops at module level.

  Close #2695

* Add a check for cases where the second argument to ``isinstance`` is not a type.

  Close #3308

* Add 'notes-rgx' option, to be used for fixme check.

  Close #2874

* ``function-redefined`` exempts function redefined on a condition.

  Close #2410

* ``typing.overload`` functions are exempted from docstring checks

  Close #3350

* Emit ``invalid-overridden-method`` for improper async def overrides.

  Close #3355

* Do not allow ``python -m pylint ...`` to import user code

  ``python -m pylint ...`` adds the current working directory as the first element
  of ``sys.path``. This opens up a potential security hole where ``pylint`` will import
  user level code as long as that code resides in modules having the same name as stdlib
  or pylint's own modules.

  Close #3386

* Add ``dummy-variables-rgx`` option for ``_redeclared-assigned-name`` check.

  Close #3341

* Fixed graph creation for relative paths

* Add a check for asserts on string literals.

  Close #3284

* ``not in`` is considered iterating context for some of the Python 3 porting checkers.

* A new check ``inconsistent-quotes`` was added.

* Add a check for non string assignment to __name__ attribute.

  Close #583

* ``__pow__``, ``__imatmul__``, ``__trunc__``, ``__floor__``, and ``__ceil__`` are recognized as special method names.

  Close #3281

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

  Close #560

* ``missing-*-docstring`` can look for ``__doc__`` assignments.

  Close #3301

* ``undefined-variable`` can now find undefined loop iterables

  Close #498

* ``safe_infer`` can infer a value as long as all the paths share the same type.

  Close #2503

* Add a --fail-under <score> flag, also configurable in a .pylintrc file. If the final score is more than the specified score, it's considered a success and pylint exits with exitcode 0. Otherwise, it's considered a failure and pylint exits with its current exitcode based on the messages issued.

  Close #2242

* Don't emit ``line-too-long`` for multilines when ``disable=line-too-long`` comment stands at their end

  Close #2957

* Fixed an ``AttributeError`` caused by improper handling of ``dataclasses`` inference in ``pyreverse``

  Close #3256

* Do not exempt bare except from ``undefined-variable`` and similar checks

  If a node was wrapped in a ``TryExcept``, ``pylint`` was taking a hint
  from the except handler when deciding to emit or not a message.
  We were treating bare except as a fully fledged ignore but only
  the corresponding exceptions should be handled that way (e.g. ``NameError`` or ``ImportError``)

  Close #3235

* No longer emit ``assignment-from-no-return`` when a function only raises an exception

  Close #3218

* Allow import aliases to exempt ``import-error`` when used in type annotations.

  Close #3178

* ``Ellipsis` is exempted from ``multiple-statements`` for function overloads.

  Close #3224

* No longer emit ``invalid-name`` for non-constants found at module level.

  Pylint was taking the following statement from PEP-8 too far, considering
  all module level variables as constants, which is not what the statement is saying:

  `Constants are usually defined on a module level and written in
  all capital letters with underscores separating words.`

  Close #3111
  Close #3132

* Allow ``implicit-str-concat-in-sequence`` to be emitted for string juxtaposition

  Close #3030

* ``implicit-str-concat-in-sequence`` was renamed ``implicit-str-concat``

* The ``json`` reporter no longer bypasses ``redirect_stdout``. Close #3227

* Move ``NoFileError``, ``OutputLine``, ``FunctionalTestReporter``,
  ``FunctionalTestFile``, ``LintModuleTest`` and related methods from
  ``test_functional.py`` to ``pylint.testutils`` to help testing for 3rd
  party pylint plugins.

* Can read config from a setup.cfg or pyproject.toml file.

  Close #617

* Fix exception-escape false positive with generators

  Close #3128

* ``inspect.getargvalues`` is no longer marked as deprecated.

* A new check ``f-string-without-interpolation`` was added

  Close #3190

* Flag mutable ``collections.*`` utilities as dangerous defaults

  Close #3183

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

  Close #1603

* Emit ``unused-argument`` for functions that partially uses their argument list before raising an exception.

  Close #3246

* Fixed ``broad_try_clause`` extension to check try/finally statements and to
  check for nested statements (e.g., inside of an ``if`` statement).

* Recognize classes explicitly inheriting from ``abc.ABC`` or having an
  ``abc.ABCMeta`` metaclass as abstract. This makes them not trigger W0223.

  Closes #3098

* Fix overzealous ``arguments-differ`` when overridden function uses variadics

  No message is emitted if the overriding function provides positional or
  keyword variadics in its signature that can feasibly accept and pass on
  all parameters given by the overridden function.

  Close #1482
  Close #1553

* Multiple types of string formatting are allowed in logging functions.

  The ``logging-fstring-interpolation`` message has been brought back to allow
  multiple types of string formatting to be used.

  Close #3361
