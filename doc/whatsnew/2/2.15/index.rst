***************************
 What's New in Pylint 2.15
***************************

.. toctree::
   :maxdepth: 2

:Release: 2.15
:Date: TBA

Summary -- Release highlights
=============================


New checkers
============

Added new checker ``missing-timeout`` to warn of default timeout values that could cause
a program to be hanging indefinitely.


Removed checkers
================


Extensions
==========


False positives fixed
=====================

* The ``differing-param-doc`` check was triggered by positional only arguments.

  Closes #6950

* Don't report ``unsupported-binary-operation`` on Python <= 3.9 when using the ``|`` operator
  with types, if one has a metaclass that overloads ``__or__`` or ``__ror__`` as appropriate.

  Closes #4951

False negatives fixed
=====================

* Emit ``modified-iterating-list`` and analogous messages for dicts and sets when iterating
  literals, or when using the ``del`` keyword.

  Closes #6648

* Emit ``using-constant-test`` when testing the truth value of a variable or call result
  holding a generator.

  Closes #6909

* Emit ``used-before-assignment`` for self-referencing named expressions (``:=``) lacking
  prior assignments.

  Closes #5653

* Emit ``used-before-assignment`` when calling nested functions before assignment.

  Closes #6812

* Emit ``used-before-assignment`` when relying on a name that is reimported later in a function.

  Closes #4624

* Emit ``used-before-assignment`` for self-referencing assignments under if conditions.

  Closes #6643

* Rename ``unhashable-dict-key`` to ``unhashable-member`` and emit when creating sets and dicts,
  not just when accessing dicts.

  Closes #7034, Closes #7055


Other bug fixes
===============


Other Changes
=============

* ``useless-super-delegation`` has been renamed to ``useless-parent-delegation`` in order to be more generic.

  Closes #6953


Internal changes
================

* ``pylint.testutils.primer`` is now a private API.

  Refs #6905

* Fixed an issue where it was impossible to update functional tests output when the existing
  output was impossible to parse. Instead of raising an error we raise a warning message and
  let the functional test fail with a default value.

  Refs #6891
