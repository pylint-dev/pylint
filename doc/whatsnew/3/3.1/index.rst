
***************************
 What's New in Pylint 3.1
***************************

.. toctree::
   :maxdepth: 2

:Release: 3.1
:Date: 2024-02-25

Summary -- Release highlights
=============================

Two new checks -- ``use-yield-from``, ``deprecated-attribute`` --
and a smattering of bug fixes.

.. towncrier release notes start

What's new in Pylint 3.1.1?
---------------------------
Release date: 2024-05-13


False Positives Fixed
---------------------

- Treat `attrs.define` and `attrs.frozen` as dataclass decorators in
  `too-few-public-methods` check.

  Closes #9345 (`#9345 <https://github.com/pylint-dev/pylint/issues/9345>`_)

- Fix a false positive with ``singledispatchmethod-function`` when a method is decorated with both ``functools.singledispatchmethod`` and ``staticmethod``.

  Closes #9531 (`#9531 <https://github.com/pylint-dev/pylint/issues/9531>`_)

- Fix a false positive for ``consider-using-dict-items`` when iterating using ``keys()`` and then deleting an item using the key as a lookup.

  Closes #9554 (`#9554 <https://github.com/pylint-dev/pylint/issues/9554>`_)



What's new in Pylint 3.1.0?
---------------------------
Release date: 2024-02-25


New Features
------------

- Skip ``consider-using-join`` check for non-empty separators if an ``suggest-join-with-non-empty-separator`` option is set to ``no``.

  Closes #8701 (`#8701 <https://github.com/pylint-dev/pylint/issues/8701>`_)

- Discover ``.pyi`` files when linting.

  These can be ignored with the ``ignore-patterns`` setting.

  Closes #9097 (`#9097 <https://github.com/pylint-dev/pylint/issues/9097>`_)

- Check ``TypeAlias`` and ``TypeVar`` (PEP 695) nodes for ``invalid-name``.

  Refs #9196 (`#9196 <https://github.com/pylint-dev/pylint/issues/9196>`_)

- Support for resolving external toml files named pylintrc.toml and .pylintrc.toml.

  Closes #9228 (`#9228 <https://github.com/pylint-dev/pylint/issues/9228>`_)

- Check for `.clear`, `.discard`, `.pop` and `remove` methods being called on a set while it is being iterated over.

  Closes #9334 (`#9334 <https://github.com/pylint-dev/pylint/issues/9334>`_)



New Checks
----------

- New message `use-yield-from` added to the refactoring checker. This message is emitted when yielding from a loop can be replaced by `yield from`.

  Closes #9229. (`#9229 <https://github.com/pylint-dev/pylint/issues/9229>`_)

- Added a ``deprecated-attribute`` message to check deprecated attributes in the stdlib.

  Closes #8855 (`#8855 <https://github.com/pylint-dev/pylint/issues/8855>`_)


False Positives Fixed
---------------------

- Fixed false positive for ``inherit-non-class`` for generic Protocols.

  Closes #9106 (`#9106 <https://github.com/pylint-dev/pylint/issues/9106>`_)

- Exempt ``TypedDict`` from ``typing_extensions`` from ``too-many-ancestor`` checks.

  Refs #9167 (`#9167 <https://github.com/pylint-dev/pylint/issues/9167>`_)



False Negatives Fixed
---------------------

- Extend broad-exception-raised and broad-exception-caught to except*.

  Closes #8827 (`#8827 <https://github.com/pylint-dev/pylint/issues/8827>`_)

- Fix a false-negative for unnecessary if blocks using a different than expected ordering of arguments.

  Closes #8947. (`#8947 <https://github.com/pylint-dev/pylint/issues/8947>`_)



Other Bug Fixes
---------------

- Improve the message provided for wrong-import-order check.  Instead of the import statement ("import x"), the message now specifies the import that is out of order and which imports should come after it.  As reported in the issue, this is particularly helpful if there are multiple imports on a single line that do not follow the PEP8 convention.

  The message will report imports as follows:
  For "import X", it will report "(standard/third party/first party/local) import X"
  For "import X.Y" and "from X import Y", it will report "(standard/third party/first party/local) import X.Y"
  The import category is specified to provide explanation as to why pylint has issued the message and guidance to the developer on how to fix the problem.

  Closes #8808 (`#8808 <https://github.com/pylint-dev/pylint/issues/8808>`_)



Other Changes
-------------

- Print how many files were checked in verbose mode.

  Closes #8935 (`#8935 <https://github.com/pylint-dev/pylint/issues/8935>`_)

- Fix a crash when an enum class which is also decorated with a ``dataclasses.dataclass`` decorator is defined.

  Closes #9100 (`#9100 <https://github.com/pylint-dev/pylint/issues/9100>`_)



Internal Changes
----------------

- Update astroid version to 3.1.0.

  Refs #9457 (`#9457 <https://github.com/pylint-dev/pylint/issues/9457>`_)
