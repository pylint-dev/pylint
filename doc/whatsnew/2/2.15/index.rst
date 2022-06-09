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

* ``NoDictSubscriptChecker``

    * Added optional extension ``no-dict-subscript`` to emit messages when the ``[]`` operator is used
      to access a dictionary value.

False positives fixed
=====================


False negatives fixed
=====================

* Emit ``modified-iterating-list`` and analogous messages for dicts and sets when iterating
  literals, or when using the ``del`` keyword.

  Closes #6648


Other bug fixes
===============


Other Changes
=============


Internal changes
================
