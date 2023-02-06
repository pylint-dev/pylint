:Release: 2.9
:Date: 2021-06-29

Summary -- Release highlights
=============================

Pylint is now compatible with python 3.10.

A lot of new checks have been added, some non-opinionated performance warnings
like ``use-maxsplit-arg``, some consensual style warnings like
``unnecessary-dict-index-lookup`` or new deprecation checks.

We're aiming to reduce pylint noise for first time users and making some
new checks optional is a step in that direction. In order to do that we
created an optional code style checker that can be loaded using
``pylint.extensions.code_style`` with the ``load-plugins`` options.
More than ever, if as a veteran you want the most checks you can possibly get,
`you should check the list of pylint extensions. <https://pylint.readthedocs.io/en/latest/user_guide/checkers/extensions.html#optional-checkers>`_.


New checkers
============

* ``deprecated-decorator``: Emitted when deprecated decorator is used.

* ``consider-using-dict-items``: Emitted when iterating over dictionary keys and then
  indexing the same dictionary with the key within loop body.

* ``use-maxsplit-arg``: Emitted either when accessing only the first or last
  element of ``str.split()``.

* An ``ignore_signatures`` option has been added to the similarity checker. It will permits  to reduce false positives when multiple functions have the same parameters.

* ``unnecessary-dict-index-lookup``: Emitted when iterating over dictionary items
  (key-value pairs) and accessing the value by index lookup.

* ``consider-using-from-import``: Emitted when a submodule/member of a package is imported and aliased with the same name.

* New checker ``unused-private-member``: Emitted when a private member (i.e., starts with ``__``) of a class is defined but not used.

* New checker ``invalid-class-object``: Emitted when a non-class is assigned to a ``__class__`` attribute.

* ``invalid-all-format``: Emitted when ``__all__`` has an invalid format,
  i.e. isn't a ``tuple`` or ``list``.

* New checker ``await-outside-async``: Emitted when await is used outside an async function.

* Add new extension ``CodeStyleChecker``. It includes checkers that can improve code
  consistency. As such they don't necessarily provide a performance benefit
  and are often times opinionated.

  * ``consider-using-tuple``: Emitted when an in-place defined list or set can be replaced by a tuple.

  * ``consider-using-namedtuple-or-dataclass``: Emitted when dictionary values
    can be replaced by namedtuples or dataclass instances.


Other Changes
=============

* Fix false-positive ``consider-using-with`` (R1732) if a ternary conditional is used together with ``with``

* Fix false-positive ``consider-using-with`` (R1732) if ``contextlib.ExitStack`` takes care of calling the ``__exit__`` method

* Add type annotations to pyreverse dot files

* Pylint's tags are now the standard form ``vX.Y.Z`` and not ``pylint-X.Y.Z`` anymore.

* Fix false-positive ``too-many-ancestors`` when inheriting from builtin classes,
  especially from the ``collections.abc`` module

* The output messages for ``arguments-differ`` error message have been customized based on the different error cases.

* New option ``--fail-on=<msg ids>`` to return non-zero exit codes regardless of ``fail-under`` value.

* A new error called ``arguments-renamed`` has been created, which identifies any changes at the parameter names
  of overridden functions. It aims to separate the functionality of ``arguments-differ``.

* Fix incompatibility with Python 3.6.0 caused by ``typing.Counter`` and ``typing.NoReturn`` usage

* Allow comma-separated list in ``output-format`` and separate output files for
  each specified format.  Each output file can be defined after a semicolon for example : ``--output-format=json:myfile.json,colorized``

* The ``using-constant-test`` checker now detects constant tests consisting of list literals
  like ``[]`` and ``[1, 2, 3]``.

* ``ignore-paths`` configuration directive has been added. Defined regex patterns are matched against file path.

* Added handling of floating point values when parsing configuration from pyproject.toml

* Fix false positive ``useless-type-doc`` on ignored argument using ``pylint.extensions.docparams`` when a function
  was typed using pep484 but not inside the docstring.

* Fix missing support for detecting deprecated aliases to existing functions/methods.
  functions/methods.

* Added various deprecated functions/methods for python 3.10, 3.7, 3.6 and 3.3

* No longer emit ``consider-using-with`` for ``ThreadPoolExecutor`` and ``ProcessPoolExecutor``
  as they have legitimate use cases without a ``with`` block.

* Fix crash if a callable returning a context manager was assigned to a list or dict item
