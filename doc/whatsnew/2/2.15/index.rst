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


Removed checkers
================


Extensions
==========


False positives fixed
=====================


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

* Emit ``used-before-assignment`` for self-referencing assignments under if conditions.

  Closes #6643


Other bug fixes
===============


Other Changes
=============


Internal changes
================

* ``pylint.testutils.primer`` is now a private API.

  Refs #6905

* Fixed an issue where it was impossible to update functional tests output when the existing
  output was impossible to parse. Instead of raising an error we raise a warning message and
  let the functional test fail with a default value.

  Refs #6891
