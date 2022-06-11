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

* Emit ``used-before-assignment`` for self-referencing named expressions (``:=``) lacking
  prior assignments.

  Closes #5653

* Emit ``using-constant-test`` when testing the truth value of a call that only returns generators.

  Closes #6909


Other bug fixes
===============


Other Changes
=============


Internal changes
================

* ``pylint.testutils.primer`` is now a private API.

  Refs #6905
