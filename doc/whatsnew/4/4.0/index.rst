
***************************
 What's New in Pylint 4.0
***************************

.. toctree::
   :maxdepth: 2

:Release:4.0
:Date: 2025-10-12

Summary -- Release highlights
=============================

- Pylint now supports Python 3.14.

- Pylint's inference engine (``astroid``) is now much more precise,
  understanding implicit booleanness and ternary expressions. (Thanks @zenlyj!)

Consider this example:

.. code-block:: python

    class Result:
        errors: dict | None = None

    result = Result()
    if result.errors:
        result.errors[field_key]
        # inference engine understands result.errors cannot be None
        # pylint no longer raises unsubscriptable-object

The required ``astroid`` version is now 4.0.0. See the
`astroid changelog <https://pylint.readthedocs.io/projects/astroid/en/latest/changelog.html#what-s-new-in-astroid-4-0-0>`_
for additional fixes, features, and performance improvements applicable to pylint.

- Handling of ``invalid-name`` at the module level was patchy. Now,
  module-level constants that are reassigned are treated as variables and checked
  against ``--variable-rgx`` rather than ``--const-rgx``. Module-level lists,
  sets, and objects can pass against either regex.

Here, ``LIMIT`` is reassigned, so pylint only uses ``--variable-rgx``:

.. code-block:: python

    LIMIT = 500  # [invalid-name]
    if sometimes:
        LIMIT = 1  # [invalid-name]

If this is undesired, refactor using *exclusive* assignment so that it is
evident that this assignment happens only once:

.. code-block:: python

    if sometimes:
        LIMIT = 1
    else:
        LIMIT = 500  # exclusive assignment: uses const regex, no warning

Lists, sets, and objects still pass against either ``const-rgx`` or ``variable-rgx``
even if reassigned, but are no longer completely skipped:

.. code-block:: python

    MY_LIST = []
    my_list = []
    My_List = []  # [invalid-name]

Remember to adjust the
`regexes <https://pylint.readthedocs.io/en/latest/user_guide/messages/convention/invalid-name.html>`_
and
`allow lists <https://pylint.readthedocs.io/en/latest/user_guide/configuration/all-options.html#good-names>`_
to your liking.

.. towncrier release notes start

What's new in Pylint 4.0.1?
---------------------------
Release date: 2025-10-14


False Positives Fixed
---------------------

- Exclude ``__all__`` and ``__future__.annotations`` from ``unused-variable``.

  Closes #10019 (`#10019 <https://github.com/pylint-dev/pylint/issues/10019>`_)

- Fix false-positive for ``bare-name-capture-pattern`` if a case guard is used.

  Closes #10647 (`#10647 <https://github.com/pylint-dev/pylint/issues/10647>`_)

- Check enums created with the ``Enum()`` functional syntax to pass against the
  ``--class-rgx`` for the :ref:`invalid-name` check, like other enums.

  Closes #10660 (`#10660 <https://github.com/pylint-dev/pylint/issues/10660>`_)



What's new in Pylint 4.0.0?
---------------------------
Release date: 2025-10-12


Breaking Changes
----------------

- ``invalid-name`` now distinguishes module-level constants that are assigned only once
  from those that are reassigned and now applies ``--variable-rgx`` to the latter. Values
  other than literals (lists, sets, objects) can pass against either the constant or
  variable regexes (e.g. "LOGGER" or "logger" but not "LoGgEr").

  Remember that ``--good-names`` or ``--good-names-rgxs`` can be provided to explicitly
  allow good names.

  Closes #3585 (`#3585 <https://github.com/pylint-dev/pylint/issues/3585>`_)

- The unused ``pylintrc`` argument to ``PyLinter.__init__()`` is deprecated
  and will be removed.

  Refs #6052 (`#6052 <https://github.com/pylint-dev/pylint/issues/6052>`_)

- Commented out code blocks such as ``#    bar() # TODO: remove dead code`` will no longer emit ``fixme``.

  Refs #9255 (`#9255 <https://github.com/pylint-dev/pylint/issues/9255>`_)

- ``pyreverse`` ``Run`` was changed to no longer call ``sys.exit()`` in its ``__init__``.
  You should now call ``Run(args).run()`` which will return the exit code instead.
  Having a class that always raised a ``SystemExit`` exception was considered a bug.

  Normal usage of pyreverse through the CLI will not be affected by this change.

  Refs #9689 (`#9689 <https://github.com/pylint-dev/pylint/issues/9689>`_)

- The ``suggestion-mode`` option was removed, as pylint now always emits user-friendly hints instead
  of false-positive error messages. You should remove it from your conf if it's defined.

  Refs #9962 (`#9962 <https://github.com/pylint-dev/pylint/issues/9962>`_)

- The ``async.py`` checker module has been renamed to ``async_checker.py`` since ``async`` is a Python keyword
  and cannot be imported directly. This allows for better testing and extensibility of the async checker functionality.

  Refs #10071 (`#10071 <https://github.com/pylint-dev/pylint/issues/10071>`_)

- The message-id of ``continue-in-finally`` was changed from ``E0116`` to ``W0136``. The warning is
  now emitted for every Python version since it will raise a syntax warning in Python 3.14.
  See `PEP 765 - Disallow return/break/continue that exit a finally block <https://peps.python.org/pep-0765/>`_.

  Refs #10480 (`#10480 <https://github.com/pylint-dev/pylint/issues/10480>`_)

- Removed support for ``nmp.NaN`` alias for ``numpy.NaN`` being recognized in ':ref:`nan-comparison`'. Use ``np`` or ``numpy`` instead.

  Refs #10583 (`#10583 <https://github.com/pylint-dev/pylint/issues/10583>`_)

- Version requirement for ``isort`` has been bumped to >=5.0.0.
  The internal compatibility for older ``isort`` versions exposed via ``pylint.utils.IsortDriver`` has
  been removed.

  Refs #10637 (`#10637 <https://github.com/pylint-dev/pylint/issues/10637>`_)



New Features
------------

- ``comparison-of-constants`` now uses the unicode from the ast instead of reformatting from
   the node's values preventing some bad formatting due to ``utf-8`` limitation. The message now uses
   ``"`` instead of ``'`` to better work with what the python ast returns.

  Refs #8736 (`#8736 <https://github.com/pylint-dev/pylint/issues/8736>`_)

- Enhanced pyreverse to properly distinguish between UML relationship types (association, aggregation, composition) based on object ownership semantics. Type annotations without assignment are now treated as associations, parameter assignments as aggregations, and object instantiation as compositions.

  Closes #9045
  Closes #9267 (`#9045 <https://github.com/pylint-dev/pylint/issues/9045>`_)

- The ``fixme`` check can now search through docstrings as well as comments, by using
  ``check-fixme-in-docstring = true`` in the ``[tool.pylint.miscellaneous]`` section.

  Closes #9255 (`#9255 <https://github.com/pylint-dev/pylint/issues/9255>`_)

- The ``use-implicit-booleaness-not-x`` checks now distinguish between comparisons
  used in boolean contexts and those that are not, enabling them to provide more accurate refactoring suggestions.

  Closes #9353 (`#9353 <https://github.com/pylint-dev/pylint/issues/9353>`_)

- The verbose option now outputs the filenames of the files that have been checked.
  Previously, it only included the number of checked and skipped files.

  Closes #9357 (`#9357 <https://github.com/pylint-dev/pylint/issues/9357>`_)

- colorized reporter now colorizes messages/categories that have been configured as ``fail-on`` in red inverse.
  This makes it easier to quickly find the errors that are causing pylint CI job failures.

  Closes #9898 (`#9898 <https://github.com/pylint-dev/pylint/issues/9898>`_)

- Enhanced support for @property decorator in pyreverse to correctly display return types of annotated properties when generating class diagrams.

  Closes #10057 (`#10057 <https://github.com/pylint-dev/pylint/issues/10057>`_)

- Add --max-depth option to pyreverse to control diagram complexity. A depth of 0 shows only top-level packages, 1 shows one level of subpackages, etc.
  This helps manage visualization of large codebases by limiting the depth of displayed packages and classes.

  Refs #10077 (`#10077 <https://github.com/pylint-dev/pylint/issues/10077>`_)

- Handle deferred evaluation of annotations in Python 3.14.

  Closes #10149 (`#10149 <https://github.com/pylint-dev/pylint/issues/10149>`_)

- Enhanced pyreverse to properly detect aggregations for comprehensions (list, dict, set, generator).

  Closes #10236 (`#10236 <https://github.com/pylint-dev/pylint/issues/10236>`_)

- ``pyreverse``: add support for colorized output when using output format ``mmd`` (MermaidJS) and ``html``.

  Closes #10242 (`#10242 <https://github.com/pylint-dev/pylint/issues/10242>`_)

- pypy 3.11 is now officially supported.

  Refs #10287 (`#10287 <https://github.com/pylint-dev/pylint/issues/10287>`_)

- Add support for Python 3.14.

  Refs #10467 (`#10467 <https://github.com/pylint-dev/pylint/issues/10467>`_)

- Add naming styles for ``ParamSpec`` and ``TypeVarTuple`` that align with the ``TypeVar`` style.

  Refs #10541 (`#10541 <https://github.com/pylint-dev/pylint/issues/10541>`_)



New Checks
----------

- Add ``match-statements`` checker and the following message:
  ``bare-name-capture-pattern``.
  This will emit an error message when a name capture pattern is used in a match statement which would make the remaining patterns unreachable.
  This code is a SyntaxError at runtime.

  Closes #7128 (`#7128 <https://github.com/pylint-dev/pylint/issues/7128>`_)

- Add new check ``async-context-manager-with-regular-with`` to detect async context managers used with regular ``with`` statements instead of ``async with``.

  Refs #10408 (`#10408 <https://github.com/pylint-dev/pylint/issues/10408>`_)

- Add ``break-in-finally`` warning. Using ``break`` inside the ``finally`` clause
  will raise a syntax warning in Python 3.14.
  See `PEP 765 - Disallow return/break/continue that exit a finally block <https://peps.python.org/pep-0765/>`_.

  Refs #10480 (`#10480 <https://github.com/pylint-dev/pylint/issues/10480>`_)

- Add new checks for invalid uses of class patterns in :keyword:`match`.

  * :ref:`invalid-match-args-definition` is emitted if :py:data:`object.__match_args__` isn't a tuple of strings.
  * :ref:`too-many-positional-sub-patterns` if there are more positional sub-patterns than specified in :py:data:`object.__match_args__`.
  * :ref:`multiple-class-sub-patterns` if there are multiple sub-patterns for the same attribute.

  Refs #10559 (`#10559 <https://github.com/pylint-dev/pylint/issues/10559>`_)

- Add additional checks for suboptimal uses of class patterns in :keyword:`match`.

  * :ref:`match-class-bind-self` is emitted if a name is bound to ``self`` instead of
    using an ``as`` pattern.
  * :ref:`match-class-positional-attributes` is emitted if a class pattern has positional
    attributes when keywords could be used.

  Refs #10587 (`#10587 <https://github.com/pylint-dev/pylint/issues/10587>`_)

- Add a ``consider-math-not-float`` message. ``float("nan")`` and ``float("inf")`` are slower
  than their counterpart ``math.inf`` and ``math.nan`` by a factor of 4 (notwithstanding
  the initial import of math) and they are also not well typed when using mypy.
  This check also catches typos in float calls as a side effect.

  The :ref:`pylint.extensions.code_style` need to be activated for this check to work.

  Refs #10621 (`#10621 <https://github.com/pylint-dev/pylint/issues/10621>`_)



False Positives Fixed
---------------------

- Fix a false positive for ``used-before-assignment`` when a variable defined under
  an ``if`` and via a named expression (walrus operator) is used later when guarded
  under the same ``if`` test.

  Closes #10061 (`#10061 <https://github.com/pylint-dev/pylint/issues/10061>`_)

- Fix :ref:`no-name-in-module` for members of ``concurrent.futures`` with Python 3.14.

  Closes #10632 (`#10632 <https://github.com/pylint-dev/pylint/issues/10632>`_)



False Negatives Fixed
---------------------

- Fix false negative for ``used-before-assignment`` when a ``TYPE_CHECKING`` import is used as a type annotation prior to erroneous usage.

  Refs #8893 (`#8893 <https://github.com/pylint-dev/pylint/issues/8893>`_)

- Match cases are now counted as edges in the McCabe graph and will increase the complexity accordingly.

  Refs #9667 (`#9667 <https://github.com/pylint-dev/pylint/issues/9667>`_)

- Check module-level constants with type annotations for ``invalid-name``.
  Remember to adjust ``const-naming-style`` or ``const-rgx`` to your liking.

  Closes #9770 (`#9770 <https://github.com/pylint-dev/pylint/issues/9770>`_)

- Fix false negative where function-redefined (E0102) was not reported for functions with a leading underscore.

  Closes #9894 (`#9894 <https://github.com/pylint-dev/pylint/issues/9894>`_)

- We now raise a ``logging-too-few-args`` for format string with no
  interpolation arguments at all (i.e. for something like ``logging.debug("Awaiting process %s")``
  or ``logging.debug("Awaiting process {pid}")``). Previously we did not raise for such case.

  Closes #9999 (`#9999 <https://github.com/pylint-dev/pylint/issues/9999>`_)

- Fix false negative for ``used-before-assignment`` when a function is defined inside a ``TYPE_CHECKING`` guard block and used later.

  Closes #10028 (`#10028 <https://github.com/pylint-dev/pylint/issues/10028>`_)

- Fix a false negative for ``possibly-used-before-assignment`` when a variable is conditionally defined
  and later assigned to a type-annotated variable.

  Closes #10421 (`#10421 <https://github.com/pylint-dev/pylint/issues/10421>`_)

- Fix false negative for ``deprecated-module`` when a ``__import__`` method is used instead of ``import`` sentence.

  Refs #10453 (`#10453 <https://github.com/pylint-dev/pylint/issues/10453>`_)

- Count match cases for ``too-many-branches`` check.

  Refs #10542 (`#10542 <https://github.com/pylint-dev/pylint/issues/10542>`_)

- Fix false-negative where :ref:`unused-import` was not reported for names referenced in a preceding ``global`` statement.

  Refs #10633 (`#10633 <https://github.com/pylint-dev/pylint/issues/10633>`_)



Other Bug Fixes
---------------

- When displaying unicode with surrogates (or other potential ``UnicodeEncodeError``),
  pylint will now display a '?' character (using ``encode(encoding="utf-8", errors="replace")``)
  instead of crashing. The functional tests classes are also updated to handle this case.

  Closes #8736. (`#8736 <https://github.com/pylint-dev/pylint/issues/8736>`_)

- Fixed unidiomatic-typecheck only checking left-hand side.

  Closes #10217 (`#10217 <https://github.com/pylint-dev/pylint/issues/10217>`_)

- Fix a crash caused by malformed format strings when using ``.format`` with keyword arguments.

  Closes #10282 (`#10282 <https://github.com/pylint-dev/pylint/issues/10282>`_)

- Fix false positive ``inconsistent-return-statements`` when using ``quit()`` or ``exit()`` functions.

  Closes #10508 (`#10508 <https://github.com/pylint-dev/pylint/issues/10508>`_)

- Fix a crash in :ref:`nested-min-max` when using ``builtins.min`` or ``builtins.max``
  instead of ``min`` or ``max`` directly.

  Closes #10626 (`#10626 <https://github.com/pylint-dev/pylint/issues/10626>`_)

- Fixed a crash in :ref:`unnecessary-dict-index-lookup` when the index of an enumerated list
  was deleted inside a for loop.

  Closes #10627 (`#10627 <https://github.com/pylint-dev/pylint/issues/10627>`_)



Other Changes
-------------

- Remove support for launching pylint with Python 3.9.
  Code that supports Python 3.9 can still be linted with the ``--py-version=3.9`` setting.

  Refs #10405 (`#10405 <https://github.com/pylint-dev/pylint/issues/10405>`_)



Internal Changes
----------------

- Modified test framework to allow for different test output for different Python versions.

  Refs #10382 (`#10382 <https://github.com/pylint-dev/pylint/issues/10382>`_)
