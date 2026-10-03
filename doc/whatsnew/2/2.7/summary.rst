:Release: 2.7
:Date: 2021-02-21

Summary -- Release highlights
=============================

* Python 3.6+ is now required.
* No more duplicate messages when using multiple jobs.
* Handling of the new typing provided by mypy 0.8
* Reduced the number of false positives in general
* Reduced the occurrence of genuinely large recursion that went above system limit (See #3836, for a fix for pandas)

New checkers
============

* Add ``nan-comparison`` check for comparison of NaN values

* Add support to ``ignored-argument-names`` in DocstringParameterChecker and
  adds ``useless-param-doc`` and ``useless-type-doc`` messages.

* Add ``empty-comment`` check for empty comments.

* Add ``simplifiable-condition`` check for extraneous constants in conditionals using and/or.

* Add ``condition-evals-to-constant`` check for conditionals using and/or that evaluate to a constant.

* Add ``consider-using-generator`` check for the use of list comprehension inside ``any`` or ``all`` function.

Other Changes
=============

* Fix false positive for ``builtin-not-iterating`` when ``zip`` or ``map`` receives iterable

* Fix linter multiprocessing pool shutdown which triggered warnings when ran in parallels with other pytest plugins.

* Enums are now required to be named in UPPER_CASE by ``invalid-name``.

* Fix bug that lead to duplicate messages when using ``--jobs 2`` or more.

* Adds option ``check-protected-access-in-special-methods`` in the ClassChecker to activate/deactivate
  ``protected-access`` message emission for single underscore prefixed attribute in special methods.

* ``inconsistent-return-statements`` message is now emitted if one of ``try/except`` statement
  is not returning explicitly while the other do.

* Fix false positive message ``useless-super-delegation`` when default keyword argument is a dictionary.

* Fix vulnerable regular expressions in ``pyreverse``. The ambiguities of vulnerable regular expressions are removed, making the repaired regular expressions safer and faster matching.

* ``len-as-conditions`` is now triggered only for classes that are inheriting directly from list, dict, or set and not implementing the ``__bool__`` function, or from generators like range or list/dict/set comprehension. This should reduce the false positive for other classes, like pandas's DataFrame or numpy's Array.

* Fixes duplicate code detection for --jobs=2+

* New option ``allowed-redefined-builtins`` defines variable names allowed to shadow builtins.

* Improved protected access checks to allow access inside class methods
