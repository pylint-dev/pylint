***************************
 What's New in Pylint 2.15
***************************

.. toctree::
   :maxdepth: 2

:Release: 2.15
:Date: TBA

Summary -- Release highlights
=============================

* We improved ``pylint``'s handling of namespace packages. More packages should be
  linted without resorting to using the ``-recursive=y`` option.

Other Changes
=============


* ``bad-exception-context`` has been renamed to ``bad-exception-cause`` as it is about the cause and not the context.

  Closes #3694

.. towncrier release notes start
