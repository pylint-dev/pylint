:Release: 2.12
:Date: 2021-11-24

Summary -- Release highlights
=============================

In 2.12, we introduced a new option ``py-version`` that permits to analyse code for a python
version that may differ from your current python interpreter. This does not affect all checkers but
permits, for example, to check for python 3.5 code smells (using f-string's) while using pylint with python 3.6.
The minimum version to run pylint is now 3.6.2, while the last working version for python 3.6.0
and 3.6.1 was pylint 2.9.3.

On top of fixing a lot of false positives and bugs, we also added new default checks, like
``use-implicit-booleaness-not-comparison``, ``overridden-final-method``, and ``useless-with-lock``.
There's also better check for TOML configurations.

Lastly, in addition to the information we already had about start line and start column,
we introduced new information about the end line and end column of messages. This
will permit to have more precise visual clue in IDE like in pylint for vs-code. The default
will stay the same to not break compatibility but it can be retrieved by adding ``end_line``
and ``end_column`` to the ``--msg-template`` option. For better result stick to python 3.8+.

The checker for Yoda conditions is now an extension, you might want to enable it if you were
relying on this check. There's also a new extension checker, ``consider-using-any-or-all`` that
detects for loops that could be replaced by any or all, entirely contributed by @areveny,
welcome to the team !

New checkers
============

* Added ``missing-any-param-doc`` triggered when a function has neither parameter nor parameter type
  documentation. Undocumented parameters are now being properly identified. A warning might start to
  appear unexpectedly if ``missing-param-doc`` and ``missing-type-doc`` were disabled, as a new message
  ``missing-any-param-doc`` will be emitted instead.

  Closes #3799

typing.final
------------

* Added ``overridden-final-method``: Emitted when a method which is annotated with ``typing.final`` is overridden

* Added ``subclassed-final-class``: Emitted when a class which is annotated with ``typing.final`` is subclassed

  Closes #3197

* Created new ``UnsupportedVersionChecker`` checker class that includes checks for features
  not supported by all versions indicated by a ``py-version``.

  * Added ``using-f-string-in-unsupported-version`` checker. Issued when ``py-version``
    is set to a version that does not support f-strings (< 3.6)

* Added new checker ``use-implicit-booleaness-not-comparison``: Emitted when
  collection literal comparison is being used to check for emptiness.

  Closes #4774

* Added ``using-final-decorator-in-unsupported-version`` checker. Issued when ``py-version``
  is set to a version that does not support typing.final (< 3.8)

* Added new checker ``useless-with-lock`` to find incorrect usage of with statement and threading module locks.
  Emitted when ``with threading.Lock():`` is used instead of ``with lock_instance:``.

  Closes #5208

* A new ``bad-configuration-section`` checker was added that will emit for misplaced option
  in pylint's top level namespace for toml configuration. Top-level dictionaries or option defined
  in the wrong section will still silently not be taken into account, which is tracked in a
  follow-up issue.

  Follow-up in #5259

* ``MessageTest`` of the unittest ``testutil`` now requires the ``confidence`` attribute
  to match the expected value. If none is provided it is set to ``UNDEFINED``.

* ``add_message`` of the unittest ``testutil`` now actually handles the ``col_offset`` parameter
  and allows it to be checked against actual output in a test.

Extensions
==========

* Added an optional extension ``consider-using-any-or-all``: Emitted when a ``for`` loop only
  produces a boolean and could be replaced by ``any`` or ``all`` using a generator. Also suggests
  a suitable any/all statement if it is concise.

  Closes #5008

* Moved ``misplaced-comparison-constant`` to its own extension ``comparison_placement``.
  This checker was opinionated and now no longer a default. It can be reactived by adding
  ``pylint.extensions.comparison_placement`` to ``load-plugins`` in your config.

  Closes #1064

Other Changes
=============

* Fix ``install graphiz`` message which isn't needed for puml output format.

* ``pylint`` no longer crashes when checking assignment expressions within if-statements

  Closes #5178

* Added configuration option ``exclude-too-few-public-methods`` to allow excluding
  classes from the ``min-public-methods`` checker.

  Closes #3370

* Fix ``accept-no-yields-doc`` and ``accept-no-return-doc`` not allowing missing ``yield`` or
  ``return`` documentation when a docstring is partially correct

  Closes #5223

* Fix ``simplify-boolean-expression`` when condition can be inferred as False.

  Closes #5200

* Fix exception when pyreverse parses ``property function`` of a class.

* Improve and flatten ``unused-wildcard-import`` message

  Closes #3859

* In length checker, ``len-as-condition`` has been renamed as
  ``use-implicit-booleaness-not-len`` in order to be consistent with
  ``use-implicit-booleaness-not-comparison``.

* Fixed ``protected-access`` for accessing of attributes and methods of inner classes

  Closes #3066

* Update ``literal-comparison``` checker to ignore tuple literals

  Closes #3031

* The functional ``testutils`` now accept ``end_lineno`` and ``end_column``. Expected
  output files without these will trigger a ``DeprecationWarning``. Expected output files
  can be easily updated with the ``python tests/test_functional.py --update-functional-output`` command.

* The functional ``testutils`` now correctly check the distinction between ``HIGH`` and
  ``UNDEFINED`` confidence. Expected output files without defined ``confidence`` levels will now
  trigger a ``DeprecationWarning``. Expected output files can be easily updated with the
  ``python tests/test_functional.py --update-functional-output`` command.

* The functional test runner now supports the option ``min_pyver_end_position`` to control on which python
  versions the ``end_lineno`` and ``end_column`` attributes should be checked. The default value is 3.8.

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

* ``self-cls-assignment`` now also considers tuple assignment

* ``undefined-variable`` now correctly triggers for assignment expressions in if ... else statements
  This includes a basic form of control flow inference for if ... else statements using
  constant boolean values

  Closes #3688

* Fix crash for ``unused-private-member`` when checking private members on ``__class__``

  Closes #5261

* Fix double emitting of ``not-callable`` on inferable ``properties``

  Closes #4426

* Support configuring mixin class pattern via ``mixin-class-rgx``

* Normalize the input to the ``ignore-paths`` option to allow both Posix and
  Windows paths

  Closes #5194

* ``missing-param-doc`` now correctly parses asterisks for variable length and
  keyword parameters

  Closes #3733

* ``missing-param-doc`` now correctly handles Numpy parameter documentation without
  explicit typing

  Closes #5222

* The ``--jobs`` parameter now falls back to 1 if the host operating system does not
  have functioning shared semaphore implementation.

  Closes #5216

* Crashes when a list is encountered in a toml configuration do not happen anymore.

  Closes #4580

* Fix crash for ``protected-access`` on (outer) class traversal

* Fix ``useless-super-delegation`` false positive when default keyword argument is a variable.

* Make yn validator case insensitive, to allow for ``True`` and ``False`` in config files.

* The last version compatible with python '3.6.0' and '3.6.1' is pylint '2.9.3'. We did not
  realize that when adding incompatible typing at the time, and all versions since are broken
  for this interpreter. 2.12.0 meta-information will permit to download pylint on those
  interpreters but the installation will fail and tell you to install '2.9.3' instead.
  pylint 2.12.1 will require python >= 3.6.2.

  Closes #5171
  Follow-up in #5065

* Added the ``--enable-all-extensions`` command line option. It will load all available extensions
  which can be listed by running ``--list-extensions``

* It is now recommended to do ``pylint`` development on ``Python`` 3.8 or higher. This
  allows using the latest ``ast`` parser.

* All standard jobs in the ``pylint`` CI now run on ``Python`` 3.8 by default. We still
  support python 3.6 and 3.7 and run tests for those interpreters.

* Fix crash on ``open()`` calls when the ``mode`` argument is not a simple string.

  Fixes part of #5321

* Add ability to add ``end_line`` and ``end_column`` to the ``--msg-template`` option.
  With the standard ``TextReporter`` this will add the line and column number of the
  end of a node to the output of Pylint. If these numbers are unknown, they are represented
  by an empty string.

* Introduced primer tests and a configuration tests framework. The helper classes available in
  ``pylint/testutil/`` are still unstable and might be modified in the near future.

  Closes #4412 #5287

* Add ``endLine`` and ``endColumn`` keys to output of ``JSONReporter``.

  Closes #5380

* Fix false negative for ``consider-iterating-dictionary`` during membership checks encapsulated in iterables
  or ``not in`` checks

  Closes #5323
