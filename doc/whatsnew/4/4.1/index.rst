
***************************
 What's New in Pylint 4.1
***************************

.. toctree::
   :maxdepth: 2

:Release:4.1
:Date: TBA

Summary -- Release highlights
=============================

The duplicate-code checker and ``symilar`` received optimizations that
result in considerable performance improvements and memory use reduction
on larger codebases. For example, pandas analysis went from 20 min to
55 s and pylint does not get OOM-killed when analyzing cpython anymore.

The required ``astroid`` version is now 4.1.1. See the
`astroid changelog <https://pylint.readthedocs.io/projects/astroid/en/latest/changelog.html#what-s-new-in-astroid-4-1-0>`_
for additional fixes, features, and performance improvements applicable to pylint.

.. towncrier release notes start
