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

* Avoid reporting ``unnecessary-dict-index-lookup`` or ``unnecessary-list-index-lookup``
  when the index lookup is part of a destructuring assignment.

  Closes #6788

False negatives fixed
=====================


Other bug fixes
===============


Other Changes
=============


Internal changes
================
