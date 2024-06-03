Full changelog
==============

What's New in Pylint 2.12.2?
----------------------------
Release date: 2021-11-25

* Fixed a false positive for ``unused-import`` where everything
  was not analyzed properly inside typing guards.

* Fixed a false-positive regression for ``used-before-assignment`` for
  typed variables in the body of class methods that reference the same class

  Closes #5342

* Specified that the ``ignore-paths`` option considers "\" to represent a
  windows directory delimiter instead of a regular expression escape
  character.

* Fixed a crash with the ``ignore-paths`` option when invoking the option
  via the command line.

  Closes #5437

* Fixed handling of Sphinx-style parameter docstrings with asterisks. These
  should be escaped with by prepending a "\".

  Closes #5406

* Add ``endLine`` and ``endColumn`` keys to output of ``JSONReporter``.

  Closes #5380

* Fixed handling of Google-style parameter specifications where descriptions
  are on the line following the parameter name. These were generating
  false positives for ``missing-param-doc``.

  Closes #5452

* Fix false negative for ``consider-iterating-dictionary`` during membership checks encapsulated in iterables
  or ``not in`` checks

  Closes #5323

* ``unused-import`` now check all ancestors for typing guards

  Closes #5316


What's New in Pylint 2.12.1?
----------------------------
Release date: 2021-11-25

* Require Python ``3.6.2`` to run pylint.

  Closes #5065


What's New in Pylint 2.12.0?
----------------------------
Release date: 2021-11-24

* Upgrade astroid to 2.9.0

  Closes #4982

* Add ability to add ``end_line`` and ``end_column`` to the ``--msg-template`` option.
  With the standard ``TextReporter`` this will add the line and column number of the
  end of a node to the output of Pylint. If these numbers are unknown, they are represented
  by an empty string.

* Introduced primer tests and a configuration tests framework. The helper classes available in
  ``pylint/testutil/`` are still unstable and might be modified in the near future.

  Closes #4412 #5287

* Fix ``install graphiz`` message which isn't needed for puml output format.

* ``MessageTest`` of the unittest ``testutil`` now requires the ``confidence`` attribute
  to match the expected value. If none is provided it is set to ``UNDEFINED``.

* ``add_message`` of the unittest ``testutil`` now actually handles the ``col_offset`` parameter
  and allows it to be checked against actual output in a test.

* Fix a crash in the ``check_elif`` extensions where an undetected if in a comprehension
  with an if statement within an f-string resulted in an out of range error. The checker no
  longer relies on counting if statements anymore and uses known if statements locations instead.
  It should not crash on badly parsed if statements anymore.

* Fix ``simplify-boolean-expression`` when condition can be inferred as False.

  Closes #5200

* Fix exception when pyreverse parses ``property function`` of a class.

* The functional ``testutils`` now accept ``end_lineno`` and ``end_column``. Expected
  output files without these will trigger a ``DeprecationWarning``. Expected output files
  can be easily updated with the ``python tests/test_functional.py --update-functional-output`` command.

* The functional ``testutils`` now correctly check the distinction between ``HIGH`` and
  ``UNDEFINED`` confidence. Expected output files without defined ``confidence`` levels will now
  trigger a ``DeprecationWarning``. Expected output files can be easily updated with the
  ``python tests/test_functional.py --update-functional-output`` command.

* The functional test runner now supports the option ``min_pyver_end_position`` to control on which python
  versions the ``end_lineno`` and ``end_column`` attributes should be checked. The default value is 3.8.

* Fix ``accept-no-yields-doc`` and ``accept-no-return-doc`` not allowing missing ``yield`` or
  ``return`` documentation when a docstring is partially correct

  Closes #5223

* Add an optional extension ``consider-using-any-or-all`` : Emitted when a ``for`` loop only
  produces a boolean and could be replaced by ``any`` or ``all`` using a generator. Also suggests
  a suitable any or all statement.

  Closes #5008

* Properly identify parameters with no documentation and add new message called ``missing-any-param-doc``

  Closes #3799

* Add checkers ``overridden-final-method`` & ``subclassed-final-class``

  Closes #3197

* Fixed ``protected-access`` for accessing of attributes and methods of inner classes

  Closes #3066

* Added support for ``ModuleNotFoundError`` (``import-error`` and ``no-name-in-module``).
  ``ModuleNotFoundError`` inherits from ``ImportError`` and was added in Python ``3.6``

* ``undefined-variable`` now correctly flags variables which only receive a type annotations
  and never get assigned a value

  Closes #5140

* ``undefined-variable`` now correctly considers the line numbering and order of classes
  used in metaclass declarations

  Closes #4031

* ``used-before-assignment`` now correctly considers references to classes as type annotation
  or default values in first-level methods

  Closes #3771

* ``undefined-variable`` and ``unused-variable`` now correctly trigger for assignment expressions
  in functions defaults

  Refs #3688

* ``undefined-variable`` now correctly triggers for assignment expressions in if ... else statements
  This includes a basic form of control flow inference for if ... else statements using
  constant boolean values

  Closes #3688

* Added the ``--enable-all-extensions`` command line option. It will load all available extensions
  which can be listed by running ``--list-extensions``

* Fix bug with importing namespace packages with relative imports

  Closes #2967 and #5131

* Improve and flatten ``unused-wildcard-import`` message

  Closes #3859

* In length checker, ``len-as-condition`` has been renamed as
  ``use-implicit-booleaness-not-len`` in order to be consistent with
  ``use-implicit-booleaness-not-comparison``.

* Created new ``UnsupportedVersionChecker`` checker class that includes checks for features
  not supported by all versions indicated by a ``py-version``.

  * Added ``using-f-string-in-unsupported-version`` checker. Issued when ``py-version``
    is set to a version that does not support f-strings (< 3.6)

* Fix ``useless-super-delegation`` false positive when default keyword argument is a variable.

* Properly emit ``duplicate-key`` when Enum members are duplicate dictionary keys

  Closes #5150

* Use ``py-version`` setting for alternative union syntax check (PEP 604),
  instead of the Python interpreter version.

* Subclasses of ``dict`` are regarded as reversible by the ``bad-reversed-sequence`` checker
  (Python 3.8 onwards).

  Closes #4981

* Support configuring mixin class pattern via ``mixin-class-rgx``

* Added new checker ``use-implicit-booleaness-not-comparison``: Emitted when
  collection literal comparison is being used to check for emptiness.

  Closes #4774

* ``missing-param-doc`` now correctly parses asterisks for variable length and
  keyword parameters

  Closes #3733

* ``missing-param-doc`` now correctly handles Numpy parameter documentation without
  explicit typing

  Closes #5222

* ``pylint`` no longer crashes when checking assignment expressions within if-statements

  Closes #5178

* Update ``literal-comparison``` checker to ignore tuple literals

  Closes #3031

* Normalize the input to the ``ignore-paths`` option to allow both Posix and
  Windows paths

  Closes #5194

* Fix double emitting of ``not-callable`` on inferable ``properties``

  Closes #4426

* ``self-cls-assignment`` now also considers tuple assignment

* Fix ``missing-function-docstring`` not being able to check ``__init__`` and other
  magic methods even if the ``no-docstring-rgx`` setting was set to do so

* Added ``using-final-decorator-in-unsupported-version`` checker. Issued when ``py-version``
  is set to a version that does not support ``typing.final`` (< 3.8)

* Added configuration option ``exclude-too-few-public-methods`` to allow excluding
  classes from the ``min-public-methods`` checker.

  Closes #3370

* The ``--jobs`` parameter now fallbacks to 1 if the host operating system does not
  have functioning shared semaphore implementation.

  Closes #5216

* Fix crash for ``unused-private-member`` when checking private members on ``__class__``

  Closes #5261

* Crashes when a list is encountered in a toml configuration do not happen anymore.

  Closes #4580

* Moved ``misplaced-comparison-constant`` to its own extension ``comparison_placement``.
  This checker was opinionated and now no longer a default. It can be reactived by adding
  ``pylint.extensions.comparison_placement`` to ``load-plugins`` in your config.

  Closes #1064

* A new ``bad-configuration-section`` checker was added that will emit for misplaced option
  in pylint's top level namespace for toml configuration. Top-level dictionaries or option defined
  in the wrong section will still silently not be taken into account, which is tracked in a
  follow-up issue.

  Follow-up in #5259

* Fix crash for ``protected-access`` on (outer) class traversal

* Added new checker ``useless-with-lock`` to find incorrect usage of with statement and threading module locks.
  Emitted when ``with threading.Lock():`` is used instead of ``with lock_instance:``.

  Closes #5208

* Make yn validator case insensitive, to allow for ``True`` and ``False`` in config files.

* Fix crash on ``open()`` calls when the ``mode`` argument is not a simple string.

  Fixes part of #5321

* Inheriting from a class that implements ``__class_getitem__`` no longer raises ``inherit-non-class``.

* Pyreverse - Add the project root directory to sys.path

  Closes #2479

* Don't emit ``consider-using-f-string`` if ``py-version`` is set to Python < ``3.6``.
  ``f-strings`` were added in Python ``3.6``

  Closes #5019

* Fix regression for ``unspecified-encoding`` with ``pathlib.Path.read_text()``

  Closes #5029

* Don't emit ``consider-using-f-string`` if the variables to be interpolated include a backslash

* Fixed false positive for ``cell-var-from-loop`` when variable is used as the default
  value for a keyword-only parameter.

  Closes #5012

* Fix false-positive ``undefined-variable`` with ``Lambda``, ``IfExp``, and
  assignment expression.

* Fix false-positive ``useless-suppression`` for ``wrong-import-order``

  Closes #2366

* Fixed ``toml`` dependency issue

  Closes #5066

* Fix false-positive ``useless-suppression`` for ``line-too-long``

  Closes #4212

* Fixed ``invalid-name`` not checking parameters of overwritten base ``object`` methods

  Closes #3614

* Fixed crash in ``consider-using-f-string`` if ``format`` is not called

  Closes #5058

* Fix crash with ``AssignAttr`` in ``if TYPE_CHECKING`` blocks.

  Closes #5111

* Improve node information for ``invalid-name`` on function argument.

* Prevent return type checkers being called on functions with ellipses as body

  Closes #4736

* Add ``is_sys_guard`` and ``is_typing_guard`` helper functions from astroid
  to ``pylint.checkers.utils``.

* Fix regression on ClassDef inference

  Closes #5030
  Closes #5036

* Fix regression on Compare node inference

  Closes #5048

* Fix false-positive ``isinstance-second-argument-not-valid-type`` with ``typing.Callable``.

  Closes #3507
  Closes #5087

* It is now recommended to do ``pylint`` development on ``Python`` 3.8 or higher. This
  allows using the latest ``ast`` parser.

* All standard jobs in the ``pylint`` CI now run on ``Python`` 3.8 by default. We still
  support python 3.6 and 3.7 and run tests for those interpreters.

* ``TypingChecker``

  * Fix false-negative for ``deprecated-typing-alias`` and ``consider-using-alias``
    with ``typing.Type`` + ``typing.Callable``.
