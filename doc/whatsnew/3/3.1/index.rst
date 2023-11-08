
***************************
 What's New in Pylint 3.1
***************************

.. toctree::
   :maxdepth: 2

:Release:3.1
:Date: TBA

Summary -- Release highlights
=============================

.. towncrier release notes start

What's new in Pylint 3.1.0?
---------------------------
Release date: 2023-11-08


False Positives Fixed
---------------------

- Fixed false positive for ``inherit-non-class`` for generic Protocols.

  Closes #9106 (`#9106 <https://github.com/pylint-dev/pylint/issues/9106>`_)



Other Changes
-------------

- Fix a crash when an enum class which is also decorated with a ``dataclasses.dataclass`` decorator is defined.

  Closes #9100 (`#9100 <https://github.com/pylint-dev/pylint/issues/9100>`_)
