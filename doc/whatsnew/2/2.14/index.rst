***************************
 What's New in Pylint 2.14
***************************

.. include:: ../../full_changelog_explanation.rst
.. include:: ../../summary_explanation.rst

.. toctree::
   :maxdepth: 2

   summary.rst
   full.rst


Internal changes
================

* Fixed an issue where many-core Windows machines (>~60 logical processors) would hang when
  using the default jobs count.

  Closes #6965
