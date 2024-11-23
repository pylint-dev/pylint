*************************
 What's New in Pylint 3.0
*************************

.. toctree::
   :maxdepth: 2

:Release: 3.0.0
:Date: 2023-10-02


Summary -- Release highlights
=============================

Pylint now support python 3.12 officially.

This long anticipated major version also provides some important usability
and performance improvements, along with enacting necessary breaking changes
and long-announced deprecations. The documentation of each message with an
example is very close too.

The required ``astroid`` version is now 3.0.0. See the
`astroid changelog <https://pylint.readthedocs.io/projects/astroid/en/latest/changelog.html#what-s-new-in-astroid-3-0-0>`_
for additional fixes, features, and performance improvements applicable to pylint.

Our code is now fully typed. The ``invalid-name`` message no longer checks for a minimum length of 3 characters by default. Dependencies
like wrapt or setuptools were removed.

A new ``json2`` reporter has been added. It features an enriched output that is
easier to parse and provides more info, here's a sample output.

.. code-block:: json

    {
        "messages": [
            {
                "type": "convention",
                "symbol": "line-too-long",
                "message": "Line too long (1/2)",
                "messageId": "C0301",
                "confidence": "HIGH",
                "module": "0123",
                "obj": "",
                "line": 1,
                "column": 0,
                "endLine": 1,
                "endColumn": 4,
                "path": "0123",
                "absolutePath": "0123"
            }
        ],
        "statistics": {
            "messageTypeCount": {
                "fatal": 0,
                "error": 0,
                "warning": 0,
                "refactor": 0,
                "convention": 1,
                "info": 0
            },
            "modulesLinted": 1,
            "score": 5.0
        }
    }

.. towncrier release notes start

What's new in Pylint 3.0.4?
---------------------------
Release date: 2024-02-23


False Positives Fixed
---------------------

- ``used-before-assignment`` is no longer emitted when using a name in a loop and
  depending on an earlier name assignment in an ``except`` block paired with
  ``else: continue``.

  Closes #6804 (`#6804 <https://github.com/pylint-dev/pylint/issues/6804>`_)

- Avoid false positives for ``no-member`` involving function
  attributes supplied by decorators.

  Closes #9246 (`#9246 <https://github.com/pylint-dev/pylint/issues/9246>`_)

- Fixed false positive nested-min-max for nested lists.

  Closes #9307 (`#9307 <https://github.com/pylint-dev/pylint/issues/9307>`_)

- Fix false positive for ``used-before-assignment`` in a ``finally`` block
  when assignments took place in both the ``try`` block and each exception handler.

  Closes #9451 (`#9451 <https://github.com/pylint-dev/pylint/issues/9451>`_)



Other Bug Fixes
---------------

- Catch incorrect ValueError ``"generator already executing"`` for Python 3.12.0 - 3.12.2.
  This is fixed upstream in Python 3.12.3.

  Closes #9138 (`#9138 <https://github.com/pylint-dev/pylint/issues/9138>`_)



What's new in Pylint 3.0.3?
---------------------------
Release date: 2023-12-11


False Positives Fixed
---------------------

- Fixed false positive for ``unnecessary-lambda`` when the call has keyword arguments but not the lambda.

  Closes #9148 (`#9148 <https://github.com/pylint-dev/pylint/issues/9148>`_)

- Fixed incorrect suggestion for shallow copy in unnecessary-comprehension

  Example of the suggestion:
  #pylint: disable=missing-module-docstring
  a = [1, 2, 3]
  b = [x for x in a]
  b[0] = 0
  print(a) # [1, 2, 3]

  After changing b = [x for x in a] to b = a based on the suggestion, the script now prints [0, 2, 3]. The correct suggestion should be use list(a) to preserve the original behavior.

  Closes #9172 (`#9172 <https://github.com/pylint-dev/pylint/issues/9172>`_)

- Fix false positives for ``undefined-variable`` and ``unused-argument`` for
  classes and functions using Python 3.12 generic type syntax.

  Closes #9193 (`#9193 <https://github.com/pylint-dev/pylint/issues/9193>`_)

- Fixed ``pointless-string-statement`` false positive for docstrings
  on Python 3.12 type aliases.

  Closes #9268 (`#9268 <https://github.com/pylint-dev/pylint/issues/9268>`_)

- Fix false positive for ``invalid-exception-operation`` when concatenating tuples
  of exception types.

  Closes #9288 (`#9288 <https://github.com/pylint-dev/pylint/issues/9288>`_)



Other Bug Fixes
---------------

- Fix a bug where pylint was unable to walk recursively through a directory if the
  directory has an `__init__.py` file.

  Closes #9210 (`#9210 <https://github.com/pylint-dev/pylint/issues/9210>`_)



What's new in Pylint 3.0.2?
---------------------------
Release date: 2023-10-22


False Positives Fixed
---------------------

- Fix ``used-before-assignment`` false positive for generic type syntax (PEP 695, Python 3.12).

  Closes #9110 (`#9110 <https://github.com/pylint-dev/pylint/issues/9110>`_)



Other Bug Fixes
---------------

- Escape special symbols and newlines in messages.

  Closes #7874 (`#7874 <https://github.com/pylint-dev/pylint/issues/7874>`_)

- Fixes suggestion for ``nested-min-max`` for expressions with additive operators, list and dict comprehensions.

  Closes #8524 (`#8524 <https://github.com/pylint-dev/pylint/issues/8524>`_)

- Fixes ignoring conditional imports with ``ignore-imports=y``.

  Closes #8914 (`#8914 <https://github.com/pylint-dev/pylint/issues/8914>`_)

- Emit ``inconsistent-quotes`` for f-strings with 3.12 interpreter only if targeting pre-3.12 versions.

  Closes #9113 (`#9113 <https://github.com/pylint-dev/pylint/issues/9113>`_)


What's new in Pylint 3.0.1?
---------------------------
Release date: 2023-10-05


False Positives Fixed
---------------------

- Fixed false positive for ``inherit-non-class`` for generic Protocols.

  Closes #9106 (`#9106 <https://github.com/pylint-dev/pylint/issues/9106>`_)



Other Changes
-------------

- Fix a crash when an enum class which is also decorated with a ``dataclasses.dataclass`` decorator is defined.

  Closes #9100 (`#9100 <https://github.com/pylint-dev/pylint/issues/9100>`_)


What's new in Pylint 3.0.0?
---------------------------
Release date: 2023-10-02


Breaking Changes
----------------

- Enabling or disabling individual messages will now take effect even if an
  ``--enable=all`` or ``disable=all`` follows in the same configuration file
  (or on the command line).

  This means for the following example, ``fixme`` messages will now be emitted:

  .. code-block::

      pylint my_module --enable=fixme --disable=all

  To regain the prior behavior, remove the superfluous earlier option.

  Closes #3696 (`#3696 <https://github.com/pylint-dev/pylint/issues/3696>`_)

- Remove support for launching pylint with Python 3.7.
  Code that supports Python 3.7 can still be linted with the ``--py-version=3.7`` setting.

  Refs #6306 (`#6306 <https://github.com/pylint-dev/pylint/issues/6306>`_)

- Disables placed in a ``try`` block now apply to the ``except`` block.
  Previously, they only happened to do so in the presence of an ``else`` clause.

  Refs #7767 (`#7767 <https://github.com/pylint-dev/pylint/issues/7767>`_)

- `pyreverse` now uses a new default color palette that is more colorblind friendly.
  The color scheme is taken from `Paul Tol's Notes <https://personal.sron.nl/~pault/>`_.
  If you prefer other colors, you can use the `--color-palette` option to specify custom colors.

  Closes #8251 (`#8251 <https://github.com/pylint-dev/pylint/issues/8251>`_)

- Everything related to the ``__implements__`` construct was removed. It was based on PEP245
  that was proposed in 2001 and rejected in 2006.

  The capability from pyreverse to take ``__implements__`` into account when generating diagrams
  was also removed.

  Refs #8404 (`#8404 <https://github.com/pylint-dev/pylint/issues/8404>`_)

- ``pyreverse``: Support for the ``.vcg`` output format (Visualization of Compiler Graphs) has been dropped.

  Closes #8416 (`#8416 <https://github.com/pylint-dev/pylint/issues/8416>`_)

- The warning when the now useless old pylint cache directory (pylint.d) was
  found was removed. The cache dir is documented in
  `the FAQ <https://pylint.readthedocs.io/en/latest/faq.html#where-is-the-persistent-data-stored-to-compare-between-successive-runs>`_.

  Refs #8462 (`#8462 <https://github.com/pylint-dev/pylint/issues/8462>`_)

- Following a deprecation period, ``pylint.config.PYLINTRC`` was removed.
  Use the ``pylint.config.find_default_config_files`` generator instead.

  Closes #8862 (`#8862 <https://github.com/pylint-dev/pylint/issues/8862>`_)



Changes requiring user actions
------------------------------

- The ``invalid-name`` message no longer checks for a minimum length of 3 characters by default.
  (This was an unadvertised commingling of concerns between casing
  and name length, and users regularly reported this to be surprising.)

  If checking for a minimum length is still desired, it can be regained in two ways:

  - If you are content with a ``disallowed-name`` message (instead of
    ``invalid-name``), then simply add the option ``bad-names-rgxs="^..?$"``,
    which will fail 1-2 character-long names. (Ensure you enable
    ``disallowed-name``.)

  - If you would prefer an ``invalid-name`` message to be emitted, or would
    prefer finer-grained control over the circumstances in which messages are
    emitted (classes vs. methods, etc.), then avail yourself of the regex
    options described
    `here <https://pylint.readthedocs.io/en/stable/user_guide/configuration/all-options.html#main-checker>`_.
    (In particular, take note of the commented out options in the "example
    configuration" given at the bottom of the section.) The prior regexes can
    be found in the
    `pull request <https://github.com/pylint-dev/pylint/pull/8813>`_
    that removed the length requirements.

  Closes #2018 (`#2018 <https://github.com/pylint-dev/pylint/issues/2018>`_)

- The compare to empty string checker (``pylint.extensions.emptystring``) and the compare to
  zero checker (``pylint.extensions.compare-to-zero``) have been removed and their checks are
  now part of the implicit booleaness checker:

  - ``compare-to-zero`` was renamed ``use-implicit-booleaness-not-comparison-to-zero`` and
    ``compare-to-empty-string`` was renamed ``use-implicit-booleaness-not-comparison-to-string``
    and they now need to be enabled explicitly.

  - The ``pylint.extensions.emptystring`` and ``pylint.extensions.compare-to-zero`` extensions
    no longer exist and need to be removed from the ``load-plugins`` option.

  - Messages related to implicit booleaness were made more explicit and actionable.
    This permits to make their likeness explicit and will provide better performance as they
    share most of their conditions to be raised.

  Closes #6871 (`#6871 <https://github.com/pylint-dev/pylint/issues/6871>`_)

- epylint was removed. It now lives at: https://github.com/emacsorphanage/pylint.

  Refs #7737 (`#7737 <https://github.com/pylint-dev/pylint/issues/7737>`_)

- The ``overgeneral-exceptions`` option now only takes fully qualified names
  into account (``builtins.Exception`` not ``Exception``). If you overrode
  this option, you need to use the fully qualified name now.

  There's still a warning, but it will be removed in 3.1.0.

  Refs #8411 (`#8411 <https://github.com/pylint-dev/pylint/issues/8411>`_)

- Following a deprecation period, it's no longer possible to use ``MASTER``
  or ``master`` as configuration section in ``setup.cfg`` or ``tox.ini``. It's bad practice
  to not start a section title with the tool name. Please use ``pylint.main`` instead.

  Refs #8465 (`#8465 <https://github.com/pylint-dev/pylint/issues/8465>`_)

- Package stats are now printed when running Pyreverse and a ``--verbose`` flag was added to get the original output with parsed modules. You might need to activate the verbose option if you want to keep the old output.

  Closes #8973 (`#8973 <https://github.com/pylint-dev/pylint/issues/8973>`_)



New Features
------------

- A new ``json2`` reporter has been added. It features a more enriched output that is
  easier to parse and provides more info.

  Compared to ``json`` the only changes are that messages are now under the ``"messages"``
  key and that ``"message-id"`` now follows the camelCase convention and is renamed to
  ``"messageId"``.
  The new reporter also reports the "score" of the modules you linted as defined by the
  ``evaluation`` option and provides statistics about the modules you linted.

  We encourage users to use the new reporter as the ``json`` reporter will no longer
  be maintained.

  Closes #4741 (`#4741 <https://github.com/pylint-dev/pylint/issues/4741>`_)

- In Pyreverse package dependency diagrams, show when a module imports another only for type-checking.

  Closes #8112 (`#8112 <https://github.com/pylint-dev/pylint/issues/8112>`_)

- Add new option (``--show-stdlib``, ``-L``) to ``pyreverse``.
  This is similar to the behavior of ``--show-builtin`` in that standard library
  modules are now not included by default, and this option will include them.

  Closes #8181 (`#8181 <https://github.com/pylint-dev/pylint/issues/8181>`_)

- Add Pyreverse option to exclude standalone nodes from diagrams with `--no-standalone`.

  Closes #8476 (`#8476 <https://github.com/pylint-dev/pylint/issues/8476>`_)



New Checks
----------

- Added ``DataclassChecker`` module and ``invalid-field-call`` checker to check for invalid dataclasses.field() usage.

  Refs #5159 (`#5159 <https://github.com/pylint-dev/pylint/issues/5159>`_)

- Add ``return-in-finally`` to emit a message if a return statement was found in a finally clause.

  Closes #8260 (`#8260 <https://github.com/pylint-dev/pylint/issues/8260>`_)

- Add a new message ``kwarg-superseded-by-positional-arg`` to warn when a function is called with a keyword argument which shares a name with a positional-only parameter and the function contains a keyword variadic parameter dictionary. It may be surprising behaviour when the keyword argument is added to the keyword variadic parameter dictionary.

  Closes #8558 (`#8558 <https://github.com/pylint-dev/pylint/issues/8558>`_)



Extensions
----------

- Add new ``prefer-typing-namedtuple`` message to the ``CodeStyleChecker`` to suggest
  rewriting calls to ``collections.namedtuple`` as classes inheriting from ``typing.NamedTuple``
  on Python 3.6+.

  Requires ``load-plugins=pylint.extensions.code_style`` and ``enable=prefer-typing-namedtuple`` to be raised.

  Closes #8660 (`#8660 <https://github.com/pylint-dev/pylint/issues/8660>`_)



False Positives Fixed
---------------------

- Extend concept of "function ambiguity" in ``safe_infer()`` from
  differing number of function arguments to differing set of argument names.

  Solves false positives in ``tensorflow``.

  Closes #3613 (`#3613 <https://github.com/pylint-dev/pylint/issues/3613>`_)

- Fix `unused-argument` false positive when `__new__` does not use all the arguments of `__init__`.

  Closes #3670 (`#3670 <https://github.com/pylint-dev/pylint/issues/3670>`_)

- Fix a false positive for ``invalid-name`` when a type-annotated class variable in an ``enum.Enum`` class has no assigned value.

  Refs #7402 (`#7402 <https://github.com/pylint-dev/pylint/issues/7402>`_)

- Fix ``unused-import`` false positive for usage of ``six.with_metaclass``.

  Closes #7506 (`#7506 <https://github.com/pylint-dev/pylint/issues/7506>`_)

- Fix false negatives and false positives for ``too-many-try-statements``,
  ``too-complex``, and ``too-many-branches`` by correctly counting statements
  under a ``try``.

  Refs #7767 (`#7767 <https://github.com/pylint-dev/pylint/issues/7767>`_)

- When checking for unbalanced dict unpacking in for-loops, Pylint will now test whether the length of each value to be
  unpacked matches the number of unpacking targets. Previously, Pylint would test the number of values for the loop
  iteration, which would produce a false unbalanced-dict-unpacking warning.

  Closes #8156 (`#8156 <https://github.com/pylint-dev/pylint/issues/8156>`_)

- Fix false positive for ``used-before-assignment`` when usage and assignment
  are guarded by the same test in different statements.

  Closes #8167 (`#8167 <https://github.com/pylint-dev/pylint/issues/8167>`_)

- Adds ``asyncSetUp`` to the default ``defining-attr-methods`` list to silence
  ``attribute-defined-outside-init`` warning when using
  ``unittest.IsolatedAsyncioTestCase``.

  Refs #8403 (`#8403 <https://github.com/pylint-dev/pylint/issues/8403>`_)

- `logging-not-lazy` is not longer emitted for explicitly concatenated string arguments.

  Closes #8410 (`#8410 <https://github.com/pylint-dev/pylint/issues/8410>`_)

- Fix false positive for isinstance-second-argument-not-valid-type when union types contains None.

  Closes #8424 (`#8424 <https://github.com/pylint-dev/pylint/issues/8424>`_)

- ``invalid-name`` now allows for integers in ``typealias`` names:
  - now valid: ``Good2Name``, ``GoodName2``.
  - still invalid: ``_1BadName``.

  Closes #8485 (`#8485 <https://github.com/pylint-dev/pylint/issues/8485>`_)

- No longer consider ``Union`` as type annotation as type alias for naming checks.

  Closes #8487 (`#8487 <https://github.com/pylint-dev/pylint/issues/8487>`_)

- ``unnecessary-lambda`` no longer warns on lambdas which use its parameters in
  their body (other than the final arguments), e.g.
  ``lambda foo: (bar if foo else baz)(foo)``.

  Closes #8496 (`#8496 <https://github.com/pylint-dev/pylint/issues/8496>`_)

- Fixed `unused-import` so that it observes the `dummy-variables-rgx` option.

  Closes #8500 (`#8500 <https://github.com/pylint-dev/pylint/issues/8500>`_)

- `Union` typed variables without assignment are no longer treated as
  `TypeAlias`.

  Closes #8540 (`#8540 <https://github.com/pylint-dev/pylint/issues/8540>`_)

- Allow parenthesized implicitly concatenated strings when `check-str-concat-over-line-jumps` is enabled.

  Closes #8552. (`#8552 <https://github.com/pylint-dev/pylint/issues/8552>`_)

- Fix false positive for ``positional-only-arguments-expected`` when a function contains both a positional-only parameter that has a default value, and ``**kwargs``.

  Closes #8555 (`#8555 <https://github.com/pylint-dev/pylint/issues/8555>`_)

- Fix false positive for ``keyword-arg-before-vararg`` when a positional-only parameter with a default value precedes ``*args``.

  Closes #8570 (`#8570 <https://github.com/pylint-dev/pylint/issues/8570>`_)

- Fix false positive for ``arguments-differ`` when overriding `__init_subclass__`.

  Closes #8919 (`#8919 <https://github.com/pylint-dev/pylint/issues/8919>`_)

- Fix a false positive for ``no-value-for-parameter`` when a staticmethod is called in a class body.

  Closes #9036 (`#9036 <https://github.com/pylint-dev/pylint/issues/9036>`_)



False Negatives Fixed
---------------------

- Emit ``used-before-assignment`` when calling module-level functions before definition.

  Closes #1144 (`#1144 <https://github.com/pylint-dev/pylint/issues/1144>`_)

- Apply ``infer_kwarg_from_call()`` to more checks

  These mostly solve false negatives for various checks,
  save for one false positive for ``use-maxsplit-arg``.

  Closes #7761 (`#7761 <https://github.com/pylint-dev/pylint/issues/7761>`_)

- `TypeAlias` variables defined in functions are now checked for `invalid-name` errors.

  Closes #8536 (`#8536 <https://github.com/pylint-dev/pylint/issues/8536>`_)

- Fix false negative for ``no-value-for-parameter`` when a function, whose signature contains both a positional-only parameter ``name`` and also ``*kwargs``, is called with a keyword-argument for ``name``.

  Closes #8559 (`#8559 <https://github.com/pylint-dev/pylint/issues/8559>`_)

- Fix a false negative for ``too-many-arguments`` by considering positional-only and keyword-only parameters.

  Closes #8667 (`#8667 <https://github.com/pylint-dev/pylint/issues/8667>`_)

- Emit ``assignment-from-no-return`` for calls to builtin methods like ``dict.update()``.
  Calls to ``list.sort()`` now raise ``assignment-from-no-return``
  rather than ``assignment-from-none`` for consistency.

  Closes #8714
  Closes #8810 (`#8714 <https://github.com/pylint-dev/pylint/issues/8714>`_)

- ``consider-using-augmented-assign`` is now applied to dicts and lists as well.

  Closes #8959. (`#8959 <https://github.com/pylint-dev/pylint/issues/8959>`_)



Other Bug Fixes
---------------

- Support ``duplicate-code`` message when parallelizing with ``--jobs``.

  Closes #374 (`#374 <https://github.com/pylint-dev/pylint/issues/374>`_)

- Support ``cyclic-import`` message when parallelizing with ``--jobs``.

  Closes #4171 (`#4171 <https://github.com/pylint-dev/pylint/issues/4171>`_)

- ``--jobs`` can now be used with ``--load-plugins``.

  This had regressed in astroid 2.5.0.

  Closes #4874 (`#4874 <https://github.com/pylint-dev/pylint/issues/4874>`_)

- docparams extension considers type comments as type documentation.

  Closes #6287 (`#6287 <https://github.com/pylint-dev/pylint/issues/6287>`_)

- When parsing comma-separated lists of regular expressions in the config, ignore
  commas that are inside braces since those indicate quantifiers, not delineation
  between expressions.

  Closes #7229 (`#7229 <https://github.com/pylint-dev/pylint/issues/7229>`_)

- The ``ignored-modules`` option will now be correctly taken into account for ``no-name-in-module``.

  Closes #7578 (`#7578 <https://github.com/pylint-dev/pylint/issues/7578>`_)

- ``sys.argv`` is now always correctly considered as impossible to infer (instead of
  using the actual values given to pylint).

  Closes #7710 (`#7710 <https://github.com/pylint-dev/pylint/issues/7710>`_)

- Avoid duplicative warnings for unqualified exception names in the ``overgeneral-exceptions``
  setting when running with ``--jobs``.

  Closes #7774 (`#7774 <https://github.com/pylint-dev/pylint/issues/7774>`_)

- Don't show class fields more than once in Pyreverse diagrams.

  Closes #8189 (`#8189 <https://github.com/pylint-dev/pylint/issues/8189>`_)

- Fix ``used-before-assignment`` false negative when TYPE_CHECKING imports
  are used in multiple scopes.

  Closes #8198 (`#8198 <https://github.com/pylint-dev/pylint/issues/8198>`_)

- ``--clear-cache-post-run`` now also clears LRU caches for pylint utilities
  holding references to AST nodes.

  Closes #8361 (`#8361 <https://github.com/pylint-dev/pylint/issues/8361>`_)

- Fix a crash when ``TYPE_CHECKING`` is used without importing it.

  Closes #8434 (`#8434 <https://github.com/pylint-dev/pylint/issues/8434>`_)

- Fix a ``used-before-assignment`` false positive when imports
  are made under the ``TYPE_CHECKING`` else if branch.

  Closes #8437 (`#8437 <https://github.com/pylint-dev/pylint/issues/8437>`_)

- Fix a regression of ``preferred-modules`` where a partial match was used instead of the required full match.

  Closes #8453 (`#8453 <https://github.com/pylint-dev/pylint/issues/8453>`_)

- Fix a crash in pyreverse when "/" characters are used in the output filename e.g pyreverse -o png -p name/ path/to/project.

  Closes #8504 (`#8504 <https://github.com/pylint-dev/pylint/issues/8504>`_)

- Don't show arrows more than once in Pyreverse diagrams.

  Closes #8522 (`#8522 <https://github.com/pylint-dev/pylint/issues/8522>`_)

- Improve output of ``consider-using-generator`` message for ``min()`` calls with ``default`` keyword.

  Closes #8563 (`#8563 <https://github.com/pylint-dev/pylint/issues/8563>`_)

- Fixed a crash when generating a configuration file: ``tomlkit.exceptions.TOMLKitError: Can't add a table to a dotted key``
  caused by tomlkit ``v0.11.8``.

  Closes #8632 (`#8632 <https://github.com/pylint-dev/pylint/issues/8632>`_)

- Fix a line break error in Pyreverse dot output.

  Closes #8671 (`#8671 <https://github.com/pylint-dev/pylint/issues/8671>`_)

- Fix a false positive for ``method-hidden`` when using ``cached_property`` decorator.

  Closes #8753 (`#8753 <https://github.com/pylint-dev/pylint/issues/8753>`_)

- Dunder methods defined in lambda do not trigger ``unnecessary-dunder-call`` anymore, if they cannot be replaced by the non-dunder call.

  Closes #8769 (`#8769 <https://github.com/pylint-dev/pylint/issues/8769>`_)

- Don't show duplicate type annotations in Pyreverse diagrams.

  Closes #8888 (`#8888 <https://github.com/pylint-dev/pylint/issues/8888>`_)

- Fixing inconsistent hashing issue in `BaseChecker` causing some reports not being exported.

  Closes #9001 (`#9001 <https://github.com/pylint-dev/pylint/issues/9001>`_)

- Don't add `Optional` to `|` annotations with `None` in Pyreverse diagrams.

  Closes #9014 (`#9014 <https://github.com/pylint-dev/pylint/issues/9014>`_)

- Pyreverse doesn't show multiple class association arrows anymore, but only the strongest one.

  Refs #9045 (`#9045 <https://github.com/pylint-dev/pylint/issues/9045>`_)

- Prevented data loss in the linter stats for messages relating
  to the linter itself (e.g. ``unknown-option-value``), fixing
  problems with score, fail-on, etc.

  Closes #9059 (`#9059 <https://github.com/pylint-dev/pylint/issues/9059>`_)

- Fix crash in refactoring checker when unary operand used with variable in for loop.

  Closes #9074 (`#9074 <https://github.com/pylint-dev/pylint/issues/9074>`_)



Other Changes
-------------

- Pylint now exposes its type annotations.

  Closes #5488 and #2079 (`#5488 <https://github.com/pylint-dev/pylint/issues/5488>`_)

- Search for ``pyproject.toml`` recursively in parent directories up to a project or file system root.

  Refs #7163, Closes #3289 (`#7163 <https://github.com/pylint-dev/pylint/issues/7163>`_)

- All code related to the optparse config parsing has been removed.

  Refs #8405 (`#8405 <https://github.com/pylint-dev/pylint/issues/8405>`_)

- Pylint now supports python 3.12.

  Refs #8718 (`#8718 <https://github.com/pylint-dev/pylint/issues/8718>`_)

- Add a CITATION.cff file to the root of the repository containing the necessary metadata to cite Pylint.

  Closes #8760 (`#8760 <https://github.com/pylint-dev/pylint/issues/8760>`_)

- Renamed the "unneeded-not" error into "unnecessary_negation" to be clearer.

  Closes #8789 (`#8789 <https://github.com/pylint-dev/pylint/issues/8789>`_)



Internal Changes
----------------

- ``get_message_definition`` was removed from the base checker API. You can access
  message definitions through the ``MessageStore``.

  Refs #8401 (`#8401 <https://github.com/pylint-dev/pylint/issues/8401>`_)

- Everything related to the ``__implements__`` construct was removed. It was based on PEP245
  that was proposed in 2001 and rejected in 2006.

  All the classes inheriting ``Interface`` in ``pylint.interfaces`` were removed.
  ``Checker`` should only inherit ``BaseChecker`` or any of the other checker types
  from ``pylint.checkers``. ``Reporter`` should only inherit ``BaseReporter``.

  Refs #8404 (`#8404 <https://github.com/pylint-dev/pylint/issues/8404>`_)

- ``modname`` and ``msg_store`` are now required to be given in ``FileState``.
  ``collect_block_lines`` has also been removed. ``Pylinter.current_name``
  cannot be null anymore.

  Refs #8407 (`#8407 <https://github.com/pylint-dev/pylint/issues/8407>`_)

- ``Reporter.set_output`` was removed in favor of ``reporter.out = stream``.

  Refs #8408 (`#8408 <https://github.com/pylint-dev/pylint/issues/8408>`_)

- A number of old utility functions and classes have been removed:

  ``MapReduceMixin``: To make a checker reduce map data simply implement
  ``get_map_data`` and ``reduce_map_data``.

  ``is_inside_lambda``: Use ``utils.get_node_first_ancestor_of_type(x, nodes.Lambda)``

  ``check_messages``: Use ``utils.only_required_for_messages``

  ``is_class_subscriptable_pep585_with_postponed_evaluation_enabled``: Use
  ``is_postponed_evaluation_enabled(node)`` and ``is_node_in_type_annotation_context(node)``

  ``get_python_path``: assumption that there's always an __init__.py is not true since
  python 3.3 and is causing problems, particularly with PEP 420. Use ``discover_package_path``
  and pass source root(s).

  ``fix_import_path``: Use ``augmented_sys_path`` and pass additional ``sys.path``
  entries as an argument obtained from ``discover_package_path``.

  ``get_global_option``: Use ``checker.linter.config`` to get all global options.

  Related private objects have been removed as well.

  Refs #8409 (`#8409 <https://github.com/pylint-dev/pylint/issues/8409>`_)

- ``colorize_ansi`` now only accepts a ``MessageStyle`` object.

  Refs #8412 (`#8412 <https://github.com/pylint-dev/pylint/issues/8412>`_)

- Following a deprecation period, ``Pylinter.check`` now only works with sequences of strings, not strings.

  Refs #8463 (`#8463 <https://github.com/pylint-dev/pylint/issues/8463>`_)

- Following a deprecation period, ``ColorizedTextReporter`` only accepts ``ColorMappingDict``.

  Refs #8464 (`#8464 <https://github.com/pylint-dev/pylint/issues/8464>`_)

- Following a deprecation period, ``MessageTest``'s ``end_line`` and ``end_col_offset``
  must be accurate in functional tests (for python 3.8 or above on cpython, and for
  python 3.9 or superior on pypy).

  Refs #8466 (`#8466 <https://github.com/pylint-dev/pylint/issues/8466>`_)

- Following a deprecation period, the ``do_exit`` argument of the ``Run`` class (and of the ``_Run``
  class in testutils) were removed.

  Refs #8472 (`#8472 <https://github.com/pylint-dev/pylint/issues/8472>`_)

- Following a deprecation period, the ``py_version`` argument of the
  ``MessageDefinition.may_be_emitted`` function is now required. The most likely solution
  is to use 'linter.config.py_version' if you need to keep using this
  function, or to use 'MessageDefinition.is_message_enabled' instead.

  Refs #8473 (`#8473 <https://github.com/pylint-dev/pylint/issues/8473>`_)

- Following a deprecation period, the ``OutputLine`` class now requires
  the right number of argument all the time. The functional output can be
  regenerated automatically to achieve that easily.

  Refs #8474 (`#8474 <https://github.com/pylint-dev/pylint/issues/8474>`_)

- Following a deprecation period, ``is_typing_guard``, ``is_node_in_typing_guarded_import_block`` and
  ``is_node_in_guarded_import_block`` from ``pylint.utils`` were removed: use a combination of
  ``is_sys_guard`` and ``in_type_checking_block`` instead.

  Refs #8475 (`#8475 <https://github.com/pylint-dev/pylint/issues/8475>`_)

- Following a deprecation period, the ``location`` argument of the
  ``Message`` class must now be a ``MessageLocationTuple``.

  Refs #8477 (`#8477 <https://github.com/pylint-dev/pylint/issues/8477>`_)

- Following a deprecation period, the ``check_single_file`` function of the
  ``Pylinter`` is replaced by ``Pylinter.check_single_file_item``.

  Refs #8478 (`#8478 <https://github.com/pylint-dev/pylint/issues/8478>`_)



Performance Improvements
------------------------

- ``pylint`` runs (at least) ~5% faster after improvements to ``astroid``
  that make better use of the inference cache.

  Refs pylint-dev/astroid#529 (`#529 <https://github.com/pylint-dev/pylint/issues/529>`_)

- - Optimize ``is_trailing_comma()``.
  - Cache ``class_is_abstract()``.

  Refs #1954 (`#1954 <https://github.com/pylint-dev/pylint/issues/1954>`_)

- Exit immediately if all messages are disabled.

  Closes #8715 (`#8715 <https://github.com/pylint-dev/pylint/issues/8715>`_)
