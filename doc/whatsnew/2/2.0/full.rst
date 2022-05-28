Full changelog
==============

What's New in Pylint 2.0?
-------------------------

Release date: 2018-07-15

* ``try-except-raise`` should not be emitted if there are any parent exception class handlers.

   Close #2284

* ``trailing-comma-tuple`` can be emitted for ``return`` statements as well.

   Close #2269

* Fix a false positive ``inconsistent-return-statements`` message when exception is raised
  inside an else statement.

  Close #1782

* ``ImportFrom`` nodes correctly use the full name for the import sorting checks.

  Close #2181

* [].extend and similar builtin operations don't emit `dict-*-not-iterating` with the Python 3 porting checker

  Close #2187

* Add a check ``consider-using-dict-comprehension`` which is emitted if for dict initialization
  the old style with list comprehensions is used.

* Add a check ``consider-using-set-comprehension`` which is emitted if for set initialization
  the old style with list comprehensions is used.

* ``logging-not-lazy`` is emitted whenever pylint infers that a string is built with addition

  Close #2193

* Add a check ``chained-comparison`` which is emitted if a boolean operation can be simplified
  by chaining some of its operations.
  e.g "a < b and b < c", can be simplified as "a < b < c".

  Close #2032

* Add a check ``consider-using-in`` for comparisons of a variable against
  multiple values with "==" and "or"s instead of checking if the variable
  is contained "in" a tuple of those values.

* ``in`` is considered iterating context for some of the Python 3 porting checkers

  Close #2186

* Add ``--ignore-none`` flag to control if pylint should warn about ``no-member`` where the owner is None

* Fix a false positive related to ``too-many-arguments`` and bounded ``__get__`` methods

  Close #2172

* ``mcs`` as the first parameter of metaclass's ``__new__`` method was replaced by ``cls``

  Close #2028

* ``assignment-from-no-return`` considers methods as well.

   Close #2081

* Support typing.TYPE_CHECKING for *unused-import* errors

  Close #1948

* Inferred classes at a function level no longer emit ``invalid-name``
  when they don't respect the variable regular expression

  Close #1049

* Added basic support for postponed evaluation of function annotations.

  Close #2069

* Fix a bug with ``missing-kwoa`` and variadics parameters

  Close #1111

* ``simplifiable-if-statement`` takes in account only when assigning to same targets

   Close #1984

* Make ``len-as-condition`` test more cases, such as ``len() < 1`` or ``len <= 0``

* Fix false-positive ``line-too-long`` message emission for
  commented line at the end of a module

  Close #1950

* Fix false-positive ``bad-continuation`` for with statements

  Close #461

* Don't warn about ``stop-iteration-return`` when using ``next()`` over ``itertools.count``

  Close #2158

* Add a check ``consider-using-get`` for unidiomatic usage of value/default-retrieval
  for a key from a dictionary

  Close #2076

* invalid-slice-index is not emitted when the slice is used as index for a complex object.

  We only use a handful of known objects (list, set and friends) to figure out if
  we should emit invalid-slice-index when the slice is used to subscript an object.

* Don't emit ``unused-import`` anymore for typing imports used in type comments.

* Add a new check 'useless-import-alias'.

  Close #2052

* Add ``comparison-with-callable`` to warn for comparison with bare callable, without calling it.

  Close #2082

* Don't warn for ``missing-type-doc`` and/or ``missing-return-type-doc``, if type
  annotations exist on the function signature for a parameter and/or return type.
  Close #2083

* Add ``--exit-zero`` option for continuous integration scripts to more
  easily call Pylint in environments that abort when a program returns a
  non-zero (error) status code.

  Close #2042

* Warn if the first argument of an instance/ class method gets assigned

  Close #977

* New check ``comparison-with-itself`` to check comparison between same value.

  Close #2051

* Add a new warning, 'logging-fstring-interpolation', emitted when f-string
  is used within logging function calls.

  Close #1998

* Don't show 'useless-super-delegation' if the subclass method has different type annotations.

  Close #1923

* Add ``unhashable-dict-key`` check.

  Closes #586

* Don't warn that a global variable is unused if it is defined by an import

  Close #1453

* Skip wildcard import check for ``__init__.py``.

  Close #2026

* The Python 3 porting mode can now run with Python 3 as well.

* ``too-few-public-methods`` is not emitted for dataclasses.

   Close #1793

* New verbose mode option, enabled with ``--verbose`` command line flag, to
  display of extra non-checker-related output. It is disabled by default.

  Close #1863

* ``undefined-loop-variable`` takes in consideration non-empty iterred objects before emitting

  Close #2039

* Add support for numpydoc optional return value names.

  Close #2030

* ``singleton-comparison`` accounts for negative checks

  Close #2037

* Add a check ``consider-using-in`` for comparisons of a variable against
  multiple values with "==" and "or"s instead of checking if the variable
  is contained "in" a tuple of those values.

  Close #1977

* defaultdict and subclasses of dict are now handled for dict-iter-* checks

  Close #2005

* ``logging-format-interpolation`` also emits when f-strings are used instead of % syntax.

  Close #1788

* Don't trigger misplaced-bare-raise when the raise is in a finally clause

  Close #1924

* Add a new check, ``possibly-unused-variable``.

  This is similar to ``unused-variable``, the only difference is that it is
  emitted when we detect a locals() call in the scope of the unused variable.
  The ``locals()`` call could potentially use the said variable, by consuming
  all values that are present up to the point of the call. This new check
  allows to disable this error when the user intentionally uses ``locals()``
  to consume everything.

  Close #1909.

* ``no-else-return`` accounts for multiple cases

   The check was a bit overrestrictive because we were checking for
   return nodes in the .orelse node. At that point though the if statement
   can be refactored to not have the orelse. This improves the detection of
   other cases, for instance it now detects TryExcept nodes that are part of
   the .else branch.

   Close #1852

* Added two new checks, ``invalid-envvar-value`` and ``invalid-envvar-default``.

  The former is trigger whenever pylint detects that environment variable manipulation
  functions uses a different type than strings, while the latter is emitted whenever
  the said functions are using a default variable of different type than expected.

* Add a check ``consider-using-join`` for concatenation of strings using str.join(sequence)

  Close #1952

* Add a check ``consider-swap-variables`` for swapping variables with tuple unpacking

  Close #1922

* Add new checker ``try-except-raise`` that warns the user if an except handler block
  has a ``raise`` statement as its first operator. The warning is shown when there is
  a bare raise statement, effectively re-raising the exception that was caught or the
  type of the exception being raised is the same as the one being handled.

* Don't crash on invalid strings when checking for ``logging-format-interpolation``

  Close #1944

* Exempt ``__doc__`` from triggering a ``redefined-builtin``

  ``__doc__`` can be used to specify a docstring for a module without
  passing it as a first-statement string.

* Fix false positive bad-whitespace from function arguments with default
  values and annotations

  Close #1831

* Fix stop-iteration-return false positive when next builtin has a
  default value in a generator

  Close #1830

* Fix emission of false positive ``no-member`` message for class with  "private" attributes whose name is mangled.

  Close #1643

* Fixed a crash which occurred when ``Uninferable`` wasn't properly handled in ``stop-iteration-return``

  Close #1779

* Use the proper node to get the name for redefined functions (#1792)

  Close #1774

* Don't crash when encountering bare raises while checking inconsistent returns

  Close #1773

* Fix a false positive ``inconsistent-return-statements`` message when if statement is inside try/except.

  Close #1770

* Fix a false positive ``inconsistent-return-statements`` message when while loop are used.

  Close #1772

* Correct column number for whitespace conventions.

  Previously the column was stuck at 0

  Close #1649

* Fix ``unused-argument`` false positives with overshadowed variable in
  dictionary comprehension.

  Close #1731

* Fix false positive ``inconsistent-return-statements`` message when never
  returning functions are used (i.e sys.exit for example).

  Close #1771

* Fix error when checking if function is exception, as in ``bad-exception-context``.

* Fix false positive ``inconsistent-return-statements`` message when a
  function is defined under an if statement.

  Close #1794

* New ``useless-return`` message when function or method ends with a "return" or
  "return None" statement and this is the only return statement in the body.

* Fix false positive ``inconsistent-return-statements`` message by
  avoiding useless exception inference if the exception is not handled.

  Close #1794 (second part)

* Fix bad thread instantiation check when target function is provided in args.

  Close #1840

* Fixed false positive when a numpy Attributes section follows a Parameters
  section

  Close #1867

* Fix incorrect file path when file absolute path contains multiple ``path_strip_prefix`` strings.

  Close #1120

* Fix false positive undefined-variable for lambda argument in class definitions

  Close #1824

* Add of a new checker that warns the user if some messages are enabled or disabled
  by id instead of symbol.

  Close #1599

* Suppress false-positive ``not-callable`` messages from certain
  staticmethod descriptors

  Close #1699

* Fix indentation handling with tabs

  Close #1148

* Fix false-positive ``bad-continuation`` error

  Close #638

* Fix false positive unused-variable in lambda default arguments

  Close #1921
  Close #1552
  Close #1099
  Close #210

* Updated the default report format to include paths that can be clicked on in some terminals (e.g. iTerm).

* Fix inline def behavior with ``too-many-statements`` checker

  Close #1978

* Fix ``KeyError`` raised when using docparams and NotImplementedError is documented.

  Close #2102

* Fix 'method-hidden' raised when assigning to a property or data descriptor.

* Fix emitting ``useless-super-delegation`` when changing the default value of keyword arguments.

  Close #2022

* Expand ignored-argument-names include starred arguments and keyword arguments

  Close #2214

* Fix false-positive undefined-variable in nested lambda

  Close #760

* Fix false-positive ``bad-whitespace`` message for typing annoatations
  with ellipses in them

  Close 1992

* Broke down "missing-docstrings" between "module", "class" and "function"

  For this to work we had to make multiple messages with the same old name
  possible.

  Closes #1164
