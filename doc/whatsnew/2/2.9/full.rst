Full changelog
==============

What's New in Pylint 2.9.6?
---------------------------
Release date: 2021-07-28

* Fix a false positive ``undefined-variable`` when variable name in decoration
  matches function argument

  Closes #3791


What's New in Pylint 2.9.5?
---------------------------
Release date: 2021-07-21

* Fix a crash when there would be a 'TypeError object does not support
  item assignment' in the code we parse.

  Closes #4439

* Fix crash if a callable returning a context manager was assigned to a list or dict item

  Closes #4732

* Fix a crash when an AttributeInferenceError was not handled properly when
  failing to infer the real name of an import in astroid.

  Closes #4692


What's New in Pylint 2.9.4?
---------------------------
Release date: 2021-07-20

* Added ``time.clock`` to deprecated functions/methods for python 3.3

* Fix bug in which --fail-on can return a zero exit code even when the specified issue is present

  Closes #4296
  Closes #3363

* Fix hard failure when handling missing attribute in a class with duplicated bases

  Closes #4687

* Fix false-positive ``consider-using-with`` (R1732) if a ternary conditional is used together with ``with``

  Closes #4676

* Fix false-positive ``deprecated-module`` when relative import uses deprecated module name.

  Closes #4629

* Fix false-positive ``consider-using-with`` (R1732) if ``contextlib.ExitStack`` takes care of calling the ``__exit__`` method

  Closes #4654

* Fix a false positive for ``unused-private-member`` when mutating a private attribute
  with ``cls``

  Closes #4657

* Fix ignored empty functions by similarities checker with "ignore-signatures" option enabled

  Closes #4652

* Fix false-positive of ``use-maxsplit-arg`` when index is incremented in
  a loop

  Closes #4664

* Don't emit ``cyclic-import`` message if import is guarded by ``typing.TYPE_CHECKING``.

  Closes #3525

* Fix false-positive ``not-callable`` with alternative ``TypedDict`` syntax

  Closes #4715

* Clarify documentation for consider-using-from-import

* Don't emit ``unreachable`` warning for empty generator functions

  Closes #4698

* Don't emit ``import-error``, ``no-name-in-module``, and ``ungrouped-imports``
  for imports guarded by ``sys.version_info`` or ``typing.TYPE_CHECKING``.

  Closes #3285
  Closes #3382

* Fix ``invalid-overridden-method`` with nested property

  Closes #4368

* Fix false-positive of ``unused-private-member`` when using ``__new__`` in a class

  Closes #4668

* No longer emit ``consider-using-with`` for ``ThreadPoolExecutor`` and ``ProcessPoolExecutor``
  as they have legitimate use cases without a ``with`` block.

  Closes #4689

* Fix crash when inferring variables assigned in match patterns

  Closes #4685

* Fix a crash when a StopIteration was raised when inferring
  a faulty function in a context manager.

  Closes #4723


What's New in Pylint 2.9.3?
---------------------------
Release date: 2021-07-01


* Fix a crash that happened when analysing empty function with docstring
  in the ``similarity`` checker.

  Closes #4648

* The ``similarity`` checker no longer add three trailing whitespaces for
  empty lines in its report.


What's New in Pylint 2.9.2?
---------------------------
Release date: 2021-07-01

* Fix a crash that happened when analysing code using ``type(self)`` to access
  a class attribute in the ``unused-private-member`` checker.

  Closes #4638

* Fix a false positive for ``unused-private-member`` when accessing a private variable
  with ``self``

  Closes #4644

* Fix false-positive of ``unnecessary-dict-index-lookup`` and ``consider-using-dict-items``
  for reassigned dict index lookups

  Closes #4630


What's New in Pylint 2.9.1?
---------------------------
Release date: 2021-06-30

* Upgrade astroid to 2.6.2

  Closes #4631
  Closes #4633


What's New in Pylint 2.9.0?
---------------------------
Release date: 2021-06-29

* Python 3.10 is now supported.

* Add type annotations to pyreverse dot files

  Closes #1548

* Fix missing support for detecting deprecated aliases to existing
  functions/methods.

  Closes #4618

* astroid has been upgraded to 2.6.1

* Added various deprecated functions/methods for python 3.10, 3.7, 3.6 and 3.3

* Fix false positive ``useless-type-doc`` on ignored argument using ``pylint.extensions.docparams``
  when a function was typed using pep484 but not inside the docstring.

  Closes #4117
  Closes #4593

* ``setuptools_scm`` has been removed and replaced by ``tbump`` in order to not
  have hidden runtime dependencies to setuptools

* Fix a crash when a test function is decorated with ``@pytest.fixture`` and astroid can't
  infer the name of the decorator when using ``open`` without ``with``.

  Closes #4612

* Added ``deprecated-decorator``: Emitted when deprecated decorator is used.

  Closes #4429

* Added ``ignore-paths`` behaviour. Defined regex patterns are matched against full file path.

  Closes #2541

* Fix false negative for ``consider-using-with`` if calls like ``open()`` were used outside of assignment expressions.

* The warning for ``arguments-differ`` now signals explicitly the difference it detected
  by naming the argument or arguments that changed and the type of change that occurred.

* Suppress ``consider-using-with`` inside context managers.

  Closes #4430

* Added ``--fail-on`` option to return non-zero exit codes regardless of ``--fail-under`` value.

* numversion tuple contains integers again to fix multiple pylint's plugins that relied on it

  Closes #4420

* Fix false-positive ``too-many-ancestors`` when inheriting from builtin classes,
  especially from the ``collections.abc`` module

  Closes #4166
  Closes #4415

* Stdlib deprecated modules check is moved to stdlib checker. New deprecated
  modules are added.

* Fix raising false-positive ``no-member`` on abstract properties

* Created new error message called ``arguments-renamed`` which identifies any changes at the parameter
  names of overridden functions.

  Closes #3536

* New checker ``consider-using-dict-items``. Emitted  when iterating over dictionary keys and then
  indexing the same dictionary with the key within loop body.

  Closes #3389

* Don't emit ``import-error`` if import guarded behind ``if sys.version_info >= (x, x)``

* Fix incompatibility with Python 3.6.0 caused by ``typing.Counter`` and ``typing.NoReturn`` usage

  Closes #4412

* New checker ``use-maxsplit-arg``. Emitted either when accessing only the first or last
  element of ``str.split()``.

  Closes #4440

* Add ignore_signatures to duplicate code checker

  Closes #3619

* Fix documentation errors in "Block disables" paragraph of User Guide.

* New checker ``unnecessary-dict-index-lookup``. Emitted when iterating over dictionary items
  (key-value pairs) and accessing the value by index lookup.

  Closes #4470

* New checker``consider-using-from-import``. Emitted when a submodule/member of a package is imported and aliased
  with the same name.

  Closes #2309

* Allow comma-separated list in ``output-format`` and separate output files for
  each specified format.

  Closes #1798

* Make ``using-constant-test`` detect constant tests consisting of list literals like ``[]`` and
  ``[1, 2, 3]``.

* Improved error message of ``unnecessary-comprehension`` checker by providing code suggestion.

  Closes #4499

* New checker ``unused-private-member``. Emitted when a private member (i.e., starts with ``__``) of a class
  is defined but not used.

  Closes #4483

* Fix false negative of ``consider-using-enumerate`` when iterating over an attribute.

  Closes #3657

* New checker ``invalid-class-object``. Emitted when a non-class is assigned to a ``__class__`` attribute.

  Closes #585

* Fix a crash when a plugin from the configuration could not be loaded and raise an error
  'bad-plugin-value' instead

  Closes #4555

* Added handling of floating point values when parsing configuration from pyproject.toml

  Closes #4518

* ``invalid-length-returned``, now also works when nothing at all is returned
  following an upgrade in astroid.

* ``logging-format-interpolation`` and ``logging-not-lazy``, now works on logger
  class created from renamed logging import following an upgrade in astroid.

* Fix false-positive ``no-member`` with generic base class

  Closes pylint-dev/astroid#942

* Fix ``assigning-non-slot`` false-positive with base that inherits from ``typing.Generic``

  Closes #4509
  Closes pylint-dev/astroid#999

* New checker ``invalid-all-format``. Emitted when ``__all__`` has an invalid format,
  i.e. isn't a ``tuple`` or ``list``.

* Fix false positive ``unused-variable`` and ``undefined-variable`` with
  Pattern Matching in Python 3.10

* New checker ``await-outside-async``. Emitted when await is used outside an async function.

* Clarify documentation for ``typing`` extension.

  Closes #4545

* Add new extension ``CodeStyleChecker``. It includes checkers that can improve code
  consistency. As such they don't necessarily provide a performance benefit
  and are often times opinionated.

* New checker ``consider-using-tuple``. Emitted when an in-place defined
  list or set can be replaced by a tuple.

* New checker ``consider-using-namedtuple-or-dataclass``. Emitted when dictionary values
  can be replaced by namedtuples or dataclass instances.

* Fix error that occurred when using ``slice`` as subscript for dict.

* Reduce false-positives around inference of ``.value`` and ``.name``
  properties on ``Enum`` subclasses, following an upgrade in astroid

  Closes #1932
  Closes #2062

* Fix issue with ``cached_property`` that caused ``invalid-overridden-method`` error
  when overriding a ``property``.

  Closes #4023

* Fix ``unused-import`` false positive for imported modules referenced in
  attribute lookups in type comments.

  Closes #4603
