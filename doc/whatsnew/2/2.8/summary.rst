:Release: 2.8
:Date: 2021-04-24

Summary -- Release highlights
=============================

Breaking changes
================

* The 'doc' extra-require has been removed. `__pkginfo__`` does not contain the package metadata anymore
  (except ``numversion``, until 3.0). Meta-information are accessible with

```python
from importlib import metadata
metadata.metadata('pylint')
```
Prefer that to an import from ``__pkginfo__``.

New checkers
============

* New refactoring message ``consider-using-with``. This message is emitted if resource-allocating functions or methods of the
  standard library (like ``open()`` or ``threading.Lock.acquire()``) that can be used as a context manager are called without
  a ``with`` block.

* Add ``deprecated-argument`` check for deprecated arguments.

* Add new extension ``ConfusingConsecutiveElifChecker``. This optional checker emits a refactoring message (R5601 ``confusing-consecutive-elif``)
  if if/elif statements with different indentation levels follow directly one after the other.

* Add ``consider-using-min-max-builtin`` check for if statement which could be replaced by Python builtin min or max.

* Add new extension ``TypingChecker``. This optional checker can detect the use of deprecated typing aliases
  and can suggest the use of the alternative union syntax where possible.
  (For example, 'typing.Dict' can be replaced by 'dict', and 'typing.Unions' by '|', etc.)
  Make sure to check the config options if you plan on using it!

* Add ``deprecated-class`` check for deprecated classes.

Other Changes
=============

* New option ``--output=<file>`` to output result to a file rather than printing to stdout.

  Closes #1070

* Reduce usage of blacklist/whitelist terminology. Notably, ``extension-pkg-allow-list`` is an
  alternative to ``extension-pkg-whitelist`` and the message ``blacklisted-name`` is now emitted as
  ``disallowed-name``. The previous names are accepted to maintain backward compatibility.

* The packaging is now done via setuptools exclusively. ``doc``, ``tests``, ``man``, ``elisp`` and ``Changelog`` are
  not packaged anymore - reducing the size of the package by 75%.

* Updated ``astroid`` to 2.5.4

* COPYING has been renamed to LICENSE for standardization.
