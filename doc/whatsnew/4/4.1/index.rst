
***************************
 What's New in Pylint 4.1
***************************

.. toctree::
   :maxdepth: 2

:Release:4.1
:Date: TBA

Summary -- Release highlights
=============================

Startup is about 25% faster thanks to lazy imports. The import checker caches
its isort configuration, which makes pylint about 17% faster on ansible.
Finding the files to lint with ``--recursive=y`` no longer walks ignored
directories such as ``.venv`` or ``node_modules``, which took seconds on large
trees. The duplicate-code checker and ``symilar`` also received optimizations
that result in considerable performance improvements and memory use reduction
on larger codebases. For example, pandas analysis went from 20 min to 55 s and
pylint does not get OOM-killed when analyzing cpython anymore.

Python 3.15 support progresses: the unpacking in comprehensions added by
PEP 798 no longer raises false positives, and the standard library
deprecations of Python 3.15 are followed.

For CI, there is a new built-in ``junit`` output format
(``--output-format=junit``), the ``NO_COLOR`` and ``FORCE_COLOR`` environment
variables are respected, and the files to lint can now be set with the
``files`` option in the configuration file.

New checks: ``looping-through-iterator``, ``impossible-comparison``,
``chained-comparison-all-equal`` and
``using-comprehension-unpacking-in-unsupported-version``.

Running with ``--jobs`` no longer duplicates the messages of extensions or
ignores extensions enabled in the configuration.

Plugin authors: the ``confidence`` parameter can no longer be ``None``, except
in ``is_message_enabled``, and the ``MSG_STATE_*`` constants are deprecated in
favor of the ``MessageDisableReason`` enum.

The required ``astroid`` version is now 4.3.2. See the
`astroid changelog <https://pylint.readthedocs.io/projects/astroid/en/latest/changelog.html#what-s-new-in-astroid-4-3-2>`_
for additional fixes, features, and performance improvements applicable to pylint.

.. towncrier release notes start

What's new in Pylint 4.1.3?
---------------------------
Release date: 2026-10-10


False Positives Fixed
---------------------

- Fixed a false positive for ``attribute-defined-outside-init`` when an
  attribute is assigned inside the setter of an old-style, non-decorator
  ``property(fget, fset)`` call. The decorator form (``@property`` /
  ``@x.setter``) was already exempted by the fix for #409; the classic
  call form was not.

  Closes #3325 (`#3325 <https://github.com/pylint-dev/pylint/issues/3325>`_)

- Fix a false positive for ``used-before-assignment`` when a name bound by an earlier
  target of the same assignment is used by a later target, as in ``a = b[a] = 0``.

  Closes #5955 (`#5955 <https://github.com/pylint-dev/pylint/issues/5955>`_)

- Fix a ``no-member`` false positive in a comprehension inside a branch that
  cannot run, such as ``if sys.platform == "win32":`` on Linux. Like the rest of
  the branch, the comprehension is no longer checked for missing members.

  Closes #7240 (`#7240 <https://github.com/pylint-dev/pylint/issues/7240>`_)

- Fix a false positive for ``used-before-assignment`` when a name bound by a tuple
  or list target of a ``with`` item is used by a later item of the same ``with`` statement.

  Closes #7545 (`#7545 <https://github.com/pylint-dev/pylint/issues/7545>`_)

- Fix false positives such as ``not-callable``, ``not-an-iterable``,
  ``unpacking-non-sequence`` and ``no-member`` on the result of a function whose
  body is only ``...``, like ``@overload`` and ``.pyi`` stubs. Such calls were
  inferred as returning ``None``. This affected ``sqlalchemy.func``,
  ``pydantic.Field``, and the ``torch`` functions wrapped by ``_add_docstr``,
  such as ``torch.linalg.qr``.

  Closes #8138
  Closes #9218
  Closes #9354
  Closes #10087 (`#8138 <https://github.com/pylint-dev/pylint/issues/8138>`_)

- Fix a false positive for ``protected-access`` when a subclass of a subscripted
  generic base, such as ``class Child(Parent[T])``, accesses a protected member
  through that base, such as ``Parent._foo(self)``.

  Closes #8600 (`#8600 <https://github.com/pylint-dev/pylint/issues/8600>`_)

- Avoid emitting ``unreachable`` for a ``yield`` immediately after ``raise`` or
  ``sys.exit()`` that marks a function as a generator, matching the existing
  handling of ``return``.

  Closes #8909 (`#8909 <https://github.com/pylint-dev/pylint/issues/8909>`_)

- Fix a false positive for :ref:`super-init-not-called` in ``.pyi`` stub files, where
  every ``__init__`` body is ``...`` and cannot call the parent's ``__init__``.

  Closes #9096 (`#9096 <https://github.com/pylint-dev/pylint/issues/9096>`_)

- Fix a false positive for :ref:`possibly-used-before-assignment` when a lambda
  uses its parameters, including from a nested lambda, and that name is assigned
  later in the module.

  Closes #9126 (`#9126 <https://github.com/pylint-dev/pylint/issues/9126>`_)

- Fix a false positive for ``useless-parent-delegation`` when a keyword-only
  parameter is passed to the parent under the same keyword but with a different value.

  Closes #9226 (`#9226 <https://github.com/pylint-dev/pylint/issues/9226>`_)

- Fix a false positive for :ref:`unused-argument` in ``.pyi`` stub files, where
  function bodies are ``...`` and cannot use their arguments.

  Closes #9417 (`#9417 <https://github.com/pylint-dev/pylint/issues/9417>`_)

- Fix a false positive for ``used-before-assignment`` when a name assigned with an
  assignment expression in the condition of a comprehension is used in its element,
  for example ``[y for x in data if (y := f(x))]``.

  Closes #9460 (`#9460 <https://github.com/pylint-dev/pylint/issues/9460>`_)

- Fixed false positive ``arguments-differ`` and ``signature-differs`` for
  ``typing.overload`` stubs. Overload stubs in a subclass are no longer compared
  to the overridden method, and an overridden method with overloads is compared
  through its implementation instead of its first stub.

  Closes #10186
  Closes #5264 (`#10186 <https://github.com/pylint-dev/pylint/issues/10186>`_)

- Stop emitting :ref:`redefined-variable-type` when the bare ``_`` variable is
  reused to discard values of different types.

  Closes #10374 (`#10374 <https://github.com/pylint-dev/pylint/issues/10374>`_)

- Allow the ``__main__`` module name in the ``camelCase``, ``PascalCase`` and
  ``UPPER_CASE`` naming styles without reporting ``invalid-name``.

  Closes #10442 (`#10442 <https://github.com/pylint-dev/pylint/issues/10442>`_)

- Fixed a false positive for ``unexpected-keyword-arg`` when a decorator that
  returns its argument unchanged is stacked above a decorator accepting ``**kwargs``.

  Closes #10831 (`#10831 <https://github.com/pylint-dev/pylint/issues/10831>`_)

- Fix ``invalid-name`` false positives for module-level all-caps aliases that
  preserve the name of an external callable.

  Closes #11012 (`#11012 <https://github.com/pylint-dev/pylint/issues/11012>`_)

- ``redefined-builtin`` no longer warns for method parameters that retain a
  built-in name from an overridden method.

  Closes #11438 (`#11438 <https://github.com/pylint-dev/pylint/issues/11438>`_)

- Fixed a false positive for ``useless-suppression`` of ``line-too-long`` when a ``#`` inside a string literal comes before the ``# pylint: disable=line-too-long`` comment.

  Closes #11440 (`#11440 <https://github.com/pylint-dev/pylint/issues/11440>`_)

- Fix a false positive for :ref:`unnecessary-ellipsis` when an ellipsis is the
  sole body statement of a ``Protocol`` method defined inside a conditional block
  such as ``if TYPE_CHECKING:``.

  Closes #11459 (`#11459 <https://github.com/pylint-dev/pylint/issues/11459>`_)

- Fix a false positive for :ref:`unnecessary-negation` when negating a comparison
  between instances of a ``set`` or ``frozenset`` subclass.

  Refs #11513 (`#11513 <https://github.com/pylint-dev/pylint/issues/11513>`_)

- Fixed a false positive for ``arguments-differ`` when an overriding method declares
  a parameter as positional-only (``/``) that is a regular parameter in the
  overridden method. Positional-only parameters are now counted as positional
  parameters in the comparison.

  Closes #11567 (`#11567 <https://github.com/pylint-dev/pylint/issues/11567>`_)



Other Bug Fixes
---------------

- Fix ``pyreverse`` hanging or crashing with a ``RecursionError`` when
  ``--all-associated`` (``-S``) follows an attribute whose inferred class is rebuilt by
  astroid on every inference, such as a ``numpy`` array.

  Closes #3602 (`#3602 <https://github.com/pylint-dev/pylint/issues/3602>`_)

- Fix a crash in ``pyreverse`` when a diagram includes a class created by
  ``namedtuple``, or an ``argparse.Namespace``.

  Closes #10767 (`#10767 <https://github.com/pylint-dev/pylint/issues/10767>`_)

- The "difference" column of the "Messages by category" and "Duplication" reports
  (``--reports=y``) now shows the change since the previous run instead of repeating
  the previous count.

  Closes #11520 (`#11520 <https://github.com/pylint-dev/pylint/issues/11520>`_)

- Fixed ``nested-min-max`` suggesting a non-equivalent rewrite when an inner
  ``min``/``max`` call had multiple arguments.

  Refs #11593 (`#11593 <https://github.com/pylint-dev/pylint/issues/11593>`_)

- Using several output formats that all write to stdout (for example ``--output-format=colorized,no-header``)
  now raises an error instead of printing every message more than once.

  Closes #11597 (`#11597 <https://github.com/pylint-dev/pylint/issues/11597>`_)

- Fixed an ``IndexError`` crash in the typecheck checker when an ``Enum`` class defines an ``__init__`` method without arguments.

  Closes #11608 (`#11608 <https://github.com/pylint-dev/pylint/issues/11608>`_)

- Fix a crash in the ``duplicate-code`` checker when ``min-similarity-lines`` is set to ``0``.
  The checker is now disabled in that case, as documented.

  Closes #11625 (`#11625 <https://github.com/pylint-dev/pylint/issues/11625>`_)



What's new in Pylint 4.1.2?
---------------------------
Release date: 2026-10-03


False Positives Fixed
---------------------

- Fixed a false positive ``unbalanced-tuple-unpacking`` when unpacking a tuple
  concatenation whose elements have several possible values.

  Fixed by upgrading astroid to 4.3.3.

  Closes #2621 (`#2621 <https://github.com/pylint-dev/pylint/issues/2621>`_)



Other Bug Fixes
---------------

- Fixed a crash when calling ``__bases__`` on a class.

  Fixed by upgrading astroid to 4.3.3.

  Closes #11491 (`#11491 <https://github.com/pylint-dev/pylint/issues/11491>`_)

- Fix a crash (``astroid-error``) when the class of a called attribute cannot
  be fully inferred, for example when the attribute is used as a ``with``
  statement target or inside a comprehension.

  Closes #11492 (`#11492 <https://github.com/pylint-dev/pylint/issues/11492>`_)

- Fix a crash when a name bound by a ``type`` statement (a TypeVar) is used in a ``with`` statement.

  Closes #11510 (`#11510 <https://github.com/pylint-dev/pylint/issues/11510>`_)

- Fixed a crash (``TypeError``) in the variables checker when checking a class
  whose metaclass name binding has no line number, for example a class defined
  with ``metaclass=__annotations__``.

  Closes #11511 (`#11511 <https://github.com/pylint-dev/pylint/issues/11511>`_)

- Fix a crash in the ``using-final-decorator-in-unsupported-version`` check
  when ``import final`` is used.

  Closes #11521 (`#11521 <https://github.com/pylint-dev/pylint/issues/11521>`_)

- Fix a crash when a plugin passes ``confidence=None`` to ``add_message``, as
  ``pylint-pytest`` does, for a message that is disabled. ``confidence=None`` is
  accepted again and means ``UNDEFINED``, like in pylint 4.0. Passing it
  explicitly to ``add_message``, ``add_ignored_message`` or ``Message`` now emits a
  ``DeprecationWarning``: it will raise an error in pylint 5.0.

  Closes #11530 (`#11530 <https://github.com/pylint-dev/pylint/issues/11530>`_)



What's new in Pylint 4.1.1?
---------------------------
Release date: 2026-09-29


Other Changes
-------------

- Pylint 4.1.0 could not be uploaded to PyPI, because it required an unreleased
  version of ``dill`` on Python 3.15, and PyPI refuses such a dependency. 4.1.1 is
  the first 4.1 release available on PyPI, see the 4.1.0 changes below.

  Refs #11495 (`#11495 <https://github.com/pylint-dev/pylint/issues/11495>`_)



What's new in Pylint 4.1.0?
---------------------------
Release date: 2026-09-29


Breaking Changes
----------------

- The ``confidence`` parameter is no longer nullable on any APIs except for
  ``is_message_enabled`` (where ``confidence=None`` means "don't filter by
  confidence"). The default became ``interfaces.UNDEFINED`` (an immutable value);
  the behavior is unchanged unless you were passing an explicit ``None``. This
  avoids a runtime check in multiple function to set the default value conditionally.

  The ``constants.MSG_STATE_*`` integer were replaced by a ``MessageDisableReason`` enum.
  The old names remain as deprecated aliases pointing at the enum members.
  ``MessageDisableReason`` is an ``IntEnum`` so existing code comparing the return of
  ``_get_message_state_scope`` to the literal ``0`` / ``1`` / ``2`` keeps working.

  Refs #11018 (`#11018 <https://github.com/pylint-dev/pylint/issues/11018>`_)



New Features
------------

- Add support for ``ignore-pattern-in-long-lines`` to allow ignoring specific parts of a line when checking line length.

  Refs #3352 (`#3352 <https://github.com/pylint-dev/pylint/issues/3352>`_)

- Support for the ``NO_COLOR`` and ``FORCE_COLOR`` environment variables has been added.
  When running pylint, the reporter that writes to stdout is switched between ``text``
  and ``colorized`` according to the requested mode.
  The order is: ``NO_COLOR`` > ``FORCE_COLOR`` > ``--output-format=...``.

  Closes #3995 (`#3995 <https://github.com/pylint-dev/pylint/issues/3995>`_)

- The dict-init-mutate message now includes a suggested dictionary literal showing how to combine the initialization and subsequent mutations into a single statement.

  Closes #7819 (`#7819 <https://github.com/pylint-dev/pylint/issues/7819>`_)

- Add a built-in ``junit`` output format (``--output-format=junit``) that produces JUnit-compatible XML output for CI/CD integration with Jenkins, Azure DevOps, GitLab CI, and GitHub Actions.

  Closes #9143 (`#9143 <https://github.com/pylint-dev/pylint/issues/9143>`_)

- Trailing pragmas understood by other common tooling (``# type: ignore``,
  ``# pyright: ignore``, ``# noqa``, ``# pragma: no cover`` and
  ``# pragma: no branch``) are no longer counted toward the line length, so a line
  is not flagged as ``line-too-long`` solely because of such a pragma. This mirrors
  the existing behaviour for Pylint's own ``# pylint:`` pragmas.

  Closes #10172 (`#10172 <https://github.com/pylint-dev/pylint/issues/10172>`_)

- pyreverse: add ``--no-signatures`` to show method names without parameter lists or return type annotations in class diagrams.

  Closes #10772 (`#10772 <https://github.com/pylint-dev/pylint/issues/10772>`_)

- Add support for `--known-first-party` similar to `--known-third-party`.

  Refs #10803 (`#10803 <https://github.com/pylint-dev/pylint/issues/10803>`_)



New Checks
----------

- Added a new checker `looping-through-iterator` (W4801) to detect when an iterator from an outer scope is consumed in a nested loop, which can lead to the iterator being unexpectedly exhausted.

  Refs #2996 (`#2996 <https://github.com/pylint-dev/pylint/issues/2996>`_)

- Add new checks ``impossible-comparison`` and ``chained-comparison-all-equal``.
  ``impossible-comparison`` flags boolean conditions whose chain of numeric
  comparisons is logically contradictory and can never be true (for example
  ``a > b and b > a``). ``chained-comparison-all-equal`` flags boolean conditions
  whose operands form a cycle of weak inequalities (``<=`` or ``>=``) and can be
  simplified to a chain of equalities (for example ``a >= b and b >= a`` is
  equivalent to ``a == b``).

  Closes #5814 (`#5814 <https://github.com/pylint-dev/pylint/issues/5814>`_)

- Add ``using-comprehension-unpacking-in-unsupported-version`` (W2607), emitted when
  the code uses the unpacking in comprehensions added by PEP 798 while
  ``py-version`` still includes a Python version that cannot compile it.

  Refs #10982 (`#10982 <https://github.com/pylint-dev/pylint/issues/10982>`_)



False Positives Fixed
---------------------

- Fix a false positive for ``unnecessary-negation`` (C0117) when negating a
  comparison between dict views (``dict.keys()``/``dict.items()``), which like
  ``set``/``frozenset`` support only a partial (subset/superset) ordering, so
  ``not a.items() <= b.items()`` is not equivalent to ``a.items() > b.items()``.

  Closes #3668 (`#3668 <https://github.com/pylint-dev/pylint/issues/3668>`_)

- Fix false positives for :ref:`attribute-defined-outside-init` where ``__init__``
  (etc.) uses a helper method to create attributes.

  Closes #5214 (`#5214 <https://github.com/pylint-dev/pylint/issues/5214>`_)

- Fix a false positive for ``consider-using-generator`` and ``use-a-generator``
  with an asynchronous list comprehension. Turning it into a generator expression
  would create an asynchronous generator, which those functions cannot consume.

  Closes #7271 (`#7271 <https://github.com/pylint-dev/pylint/issues/7271>`_)

- Fixed a false positive ``assigning-non-slot`` when assigning to an inherited
  descriptor through an instance returned by a method annotated with the
  subclass. This regressed in pylint 3.0.0.

  Fixed by upgrading astroid to 4.1.0.

  Closes #8053 (`#8053 <https://github.com/pylint-dev/pylint/issues/8053>`_)

- Fixed a false positive ``no-member`` when a ``classmethod`` annotated with
  ``typing.Self`` is overridden in a subclass and its result is used directly,
  as in ``Subclass.build().only_on_subclass()``. The return type is now narrowed
  to the subclass rather than the base class. This regressed in pylint 3.0.0.

  Fixed by upgrading astroid to 4.1.0.

  Closes #9159 (`#9159 <https://github.com/pylint-dev/pylint/issues/9159>`_)

- Avoid emitting ``deprecated-class`` for imports inside a recognized
  ``sys.version_info`` guard.

  Closes #9533 (`#9533 <https://github.com/pylint-dev/pylint/issues/9533>`_)

- Fix a false positive for ``inconsistent-return-statements`` when an instance
  method annotated with ``NoReturn`` (or ``Never``) is called via the class
  rather than an instance (e.g. ``MyClass.raise_method(obj)``). The unbound
  method form is now recognised as never returning, matching the existing
  behaviour for the bound-method form.

  Closes #9692 (`#9692 <https://github.com/pylint-dev/pylint/issues/9692>`_)

- Fix ``used-before-assignment`` false positive for names bound in only some arms of an ``if/elif/else`` chain.

  Closes #9879 (`#9879 <https://github.com/pylint-dev/pylint/issues/9879>`_)

- Fix a false positive for ``useless-parent-delegation`` when a method overrides a
  method of a C-level parent whose signature cannot be inspected, such as
  ``Exception.__init__``. Because ``Exception.__init__`` accepts ``*args``, an
  override taking only ``self`` narrows the accepted arguments and is not useless.
  Overrides of ``object.__init__`` are still reported.

  Closes #9994 (`#9994 <https://github.com/pylint-dev/pylint/issues/9994>`_)

- Fixed a false positive ``no-name-in-module`` when a module is imported with
  an alias that shadows its base module and a function named ``format`` is
  called on the alias.

  Fixed by upgrading astroid to 4.3.1.

  Closes #10193 (`#10193 <https://github.com/pylint-dev/pylint/issues/10193>`_)

- Fixed a false positive ``unsubscriptable-object`` on instances of a generic class defining ``__class_getitem__``.

  Closes #10360 (`#10360 <https://github.com/pylint-dev/pylint/issues/10360>`_)

- Fixed a false positive ``unexpected-keyword-argument`` when passing ``dtype``
  to ``numpy.concatenate()``.

  Fixed by upgrading astroid to 4.3.1.

  Closes #10548 (`#10548 <https://github.com/pylint-dev/pylint/issues/10548>`_)

- Fix a false positive for ``unexpected-keyword-arg`` for dataclasses
  using generic type aliases (PEP 695).

  Closes #10703 (`#10703 <https://github.com/pylint-dev/pylint/issues/10703>`_)

- Fix false positive ``unreachable`` when calling a function with ``@overload`` where one signature returns ``NoReturn``.

  Closes #10785 (`#10785 <https://github.com/pylint-dev/pylint/issues/10785>`_)

- Fix a false positive for ``too-many-function-args`` for dataclasses
  using generic type aliases (PEP 695).

  Closes #10788 (`#10788 <https://github.com/pylint-dev/pylint/issues/10788>`_)

- Fix a false positive ``relative-beyond-top-level`` error when linting specific files in namespace packages in parallel mode by augmenting ``sys.path`` before loading plugins and expanding files consistently for parallel workers.

  Closes #10794 (`#10794 <https://github.com/pylint-dev/pylint/issues/10794>`_)

- Fix ``# pylint: enable`` inside a ``try`` block leaking into the ``except``
  handler. For example in the following code, ``no-member`` is no longer
  incorrectly re-enabled in the ``except`` block:

  .. code-block:: python

      class Basket:
          # pylint: disable=no-member
          def pick(self):
              try:
                  # pylint: enable=no-member
                  print(self.apple)  # no-member emitted here
              except KeyError:
                  print(self.banana)  # no-member NOT emitted here (correct)

  Requires astroid 4.2.

  Refs #10933 (`#10933 <https://github.com/pylint-dev/pylint/issues/10933>`_)

- Fix false positives for the Python 3.15 syntax added by PEP 798, unpacking in
  comprehensions:

  - ``star-needs-assignment-target`` (E0114) was emitted for the unpacked element
    of a comprehension, e.g. ``[*sub for sub in lists]``.
  - ``consider-using-dict-comprehension`` (R1717) was emitted for
    ``dict([*pairs for pairs in nested])``, which flattens its argument and is
    therefore not equivalent to a key/value dict comprehension.

  Refs #10982 (`#10982 <https://github.com/pylint-dev/pylint/issues/10982>`_)

- Fix ``access-member-before-definition`` false positive for bare type annotations
  (``self.x: Type``) that don't assign a value.

  Refs #11015 (`#11015 <https://github.com/pylint-dev/pylint/issues/11015>`_)

- Fix a false positive for ``assignment-from-no-return`` when the called function's
  body ends in an unconditional ``raise``, such as ``pathlib.Path.readlink()`` on
  platforms without symlink support.

  Closes #11114 (`#11114 <https://github.com/pylint-dev/pylint/issues/11114>`_)

- Fix a false positive for ``protected-access`` when a protected member is
  accessed through ``self.__class__``, which is now treated like ``type(self)``.

  Closes #11160 (`#11160 <https://github.com/pylint-dev/pylint/issues/11160>`_)

- Treat ``typing.NoReturn`` and ``typing.Never`` the same as ``NoReturn`` / ``Never`` when deciding that a call never returns.

  Closes #11271 (`#11271 <https://github.com/pylint-dev/pylint/issues/11271>`_)

- Fix a false positive for :ref:`unreachable` on the statement following an
  instantiation of ``_sitebuiltins.Quitter`` (the class of the ``exit`` and
  ``quit`` builtins). Only calling the instance terminates, not creating it.

  Closes #11310 (`#11310 <https://github.com/pylint-dev/pylint/issues/11310>`_)

- Fixed a false positive ``unbalanced-tuple-unpacking`` when unpacking the ``args``
  of an exception.

  Fixed by upgrading astroid to 4.3.2.

  Closes #11312 (`#11312 <https://github.com/pylint-dev/pylint/issues/11312>`_)

- Fixed a false positive for ``unnecessary-semicolon`` when an f-string ending in ``;`` is continued onto the next line with a backslash on Python 3.12+.

  Closes #11444 (`#11444 <https://github.com/pylint-dev/pylint/issues/11444>`_)



False Negatives Fixed
---------------------

- ``missing-param-doc`` and ``missing-type-doc`` no longer false-negative on
  NumPy-style parameters whose type line includes a default value, e.g.
  ``number : int, default 0``. Any text after the colon on the type line is
  now accepted as the type, matching the NumPy style guide.

  Closes #6211 (`#6211 <https://github.com/pylint-dev/pylint/issues/6211>`_)

- The ``docparams`` extension now emits ``multiple-constructor-doc`` when
  constructor parameters are documented in both the class docstring and the
  constructor docstring, even when the constructor method is skipped by
  ``no-docstring-rgx``.

  Closes #6692 (`#6692 <https://github.com/pylint-dev/pylint/issues/6692>`_)

- ``chained-comparison`` is now emitted for additional simplifiable patterns
  (e.g. ``a > 1 and a > 10``) and its message now includes the suggested
  simplification.

  Refs #7611 (`#7611 <https://github.com/pylint-dev/pylint/issues/7611>`_)

- Fix a false negative for ``abstract-method`` where a concrete subclass
  inheriting from an abstract class (without redeclaring ``abc.ABC`` or
  ``ABCMeta``) was treated as abstract and silently exempted from the check.
  A class is now only considered abstract when it opts in explicitly, via
  direct ``abc.ABC`` inheritance, ``metaclass=ABCMeta``, an
  ``@abstractmethod`` defined on the class, or being a ``Protocol``.

  Closes #7950 (`#7950 <https://github.com/pylint-dev/pylint/issues/7950>`_)

- ``no-value-for-parameter`` is now emitted when a call unpacks a dictionary literal
  with ``**`` and that dictionary does not provide a required argument.

  Closes #8785 (`#8785 <https://github.com/pylint-dev/pylint/issues/8785>`_)

- :ref:`attribute-defined-outside-init` now reports attributes assigned with
  ``setattr(self, "name", value)`` outside defining methods.
  It no longer reports attributes assigned normally when a defining method of the
  class or of a parent initializes them with ``setattr``.

  Closes #9798 (`#9798 <https://github.com/pylint-dev/pylint/issues/9798>`_)

- ``superfluous-parens`` (``C0325``) no longer false-negatives on a single
  parenthesised literal after the ``in`` keyword, e.g. ``x in ("foo")``. The
  parentheses around a single string or number literal are now reported as
  superfluous, while a tuple (``x in ("foo",)``) or a larger expression
  (``x in ("foo" + bar)``) is still left untouched.

  Closes #9878 (`#9878 <https://github.com/pylint-dev/pylint/issues/9878>`_)

- ``comparison-with-itself`` now detects repeated attribute chains such as
  ``object.attribute == object.attribute``.

  Closes #10713 (`#10713 <https://github.com/pylint-dev/pylint/issues/10713>`_)

- ``not-an-iterable`` and ``not-a-mapping`` are now also emitted for the value
  unpacked by PEP 798 comprehension unpacking, e.g. ``[*number for number in
  numbers]`` or ``{**number for number in numbers}``.

  Refs #10982 (`#10982 <https://github.com/pylint-dev/pylint/issues/10982>`_)

- Fix a false negative in ``unnecessary-negation`` (``C0117``): ``not (a is not b)`` and ``not (a not in b)`` are now flagged (they simplify to ``a is b`` and ``a in b``), consistent with the existing handling of ``is`` / ``in``.

  Closes #11140 (`#11140 <https://github.com/pylint-dev/pylint/issues/11140>`_)

- Emit ``arguments-differ`` when an overridden special method takes a different
  number of parameters. Only renamed parameters and removed variadics stay
  exempt, and the constructor family (``__new__``, ``__init__``,
  ``__init_subclass__`` and ``__post_init__``) is still fully ignored.

  Closes #11295 (`#11295 <https://github.com/pylint-dev/pylint/issues/11295>`_)

- ``access-member-before-definition`` is now also emitted when ``__init__`` calls a
  method that reads an instance attribute which ``__init__`` only assigns after the call.

  Closes #11338 (`#11338 <https://github.com/pylint-dev/pylint/issues/11338>`_)

- Fix a false negative for ``unspecified-encoding`` and ``bad-open-mode`` when the
  mode of an ``open`` call is a parameter of the enclosing function that has a
  default value. The default is now used to check the call, as a literal mode
  would be. Calls with such a mode stopped being reported in pylint 4.0.8.

  Refs #11415 (`#11415 <https://github.com/pylint-dev/pylint/issues/11415>`_)



Other Bug Fixes
---------------

- ``# pylint: disable`` comments at the beginning of an ``else`` block (or on
  the line just above the ``else`` keyword) now suppress messages in that block
  instead of being ignored.

  Fixed by upgrading astroid to 4.3.1.

  Closes #872 (`#872 <https://github.com/pylint-dev/pylint/issues/872>`_)

- ``dangerous-default-value`` now detects mutable default values in ``typing.NamedTuple`` field definitions.

  Closes #3716 (`#3716 <https://github.com/pylint-dev/pylint/issues/3716>`_)

- Repeated ``--output-format`` options now write reports to every requested file instead of only the last one.

  Closes #8147 (`#8147 <https://github.com/pylint-dev/pylint/issues/8147>`_)

- Fixed a crash when defining a functional ``namedtuple`` with a field name
  that changes under NFKC normalization, like ``"µ"`` (MICRO SIGN).

  Fixed by upgrading astroid to 4.3.1.

  Closes #8746 (`#8746 <https://github.com/pylint-dev/pylint/issues/8746>`_)

- Fix a crash in ``pyreverse`` when a requested class cannot be inferred.

  Closes #9797 (`#9797 <https://github.com/pylint-dev/pylint/issues/9797>`_)

- Fix enabling checks from extensions which are disabled by default if multiple jobs are used.

  Closes #10037 (`#10037 <https://github.com/pylint-dev/pylint/issues/10037>`_)

- Fixed an ``AstroidBuildingError`` crash when inheriting from a generic
  dataclass that rebinds ``__init__`` in ``__init_subclass__``.

  Fixed by upgrading astroid to 4.3.1.

  Closes #10519 (`#10519 <https://github.com/pylint-dev/pylint/issues/10519>`_)

- ``wrong-import-position`` now exempts ``try``, ``if``, ``with``, and ``match`` blocks from marking the import boundary. Fixed ``async def`` not being detected as an import boundary. Pragma on non-import lines now suppresses following imports until the next non-import.

  Closes #10589 (`#10589 <https://github.com/pylint-dev/pylint/issues/10589>`_)

- Fix duplicate messages for extension checks if multiple jobs are used.

  Refs #10642 (`#10642 <https://github.com/pylint-dev/pylint/issues/10642>`_)

- Fix an issue where discovery can miss a similarly named directory if a shorter named directory is processed first.

  Closes #10969 (`#10969 <https://github.com/pylint-dev/pylint/issues/10969>`_)

- Follow the standard library deprecations of Python 3.15.

  Refs #10982 (`#10982 <https://github.com/pylint-dev/pylint/issues/10982>`_)

- Fixed inflated message occurrence counts in the final ``Messages`` report when
  running pylint in parallel mode with ``--jobs`` greater than 1.

  Closes #10996 (`#10996 <https://github.com/pylint-dev/pylint/issues/10996>`_)

- Fix a crash in ``consider-using-dict-items`` when the ``for`` loop or comprehension target is an attribute or a subscript (e.g. ``for self.key in d``) rather than a simple variable name.

  Closes #11173 (`#11173 <https://github.com/pylint-dev/pylint/issues/11173>`_)

- ``nan-comparison`` now also recognizes ``math.nan``, ``numpy.nan``, ``Decimal("nan")``
  and any name or attribute that pylint can infer to a NaN constant, such as a module
  level constant defined as ``math.nan``. Only ``numpy.NaN`` -- removed in numpy 2.0 --
  and ``float("nan")`` were detected before. Infinities are still not reported, as
  comparing against them is meaningful.

  Refs #11219 (`#11219 <https://github.com/pylint-dev/pylint/issues/11219>`_)

- Fix a crash in the comparison checker when a NaN comparison operand is a call to a name that cannot be inferred, such as ``1 == b('nan')``.

  Closes #11224 (`#11224 <https://github.com/pylint-dev/pylint/issues/11224>`_)

- Fix a crash in :ref:`invalid-class-object` and :ref:`assigning-non-slot` when ``__class__`` is assigned outside a simple assignment (e.g. ``for obj.__class__ in classes:``).

  Closes #11267 (`#11267 <https://github.com/pylint-dev/pylint/issues/11267>`_)

- Avoid a fatal :ref:`astroid-error` in :ref:`invalid-name`,
  :ref:`stop-iteration-return`, :ref:`assigning-non-slot` and
  :ref:`redefined-slots-in-subclass` for classes with duplicate or inconsistent
  bases, which leave the class without an MRO to walk.

  Refs #11272 (`#11272 <https://github.com/pylint-dev/pylint/issues/11272>`_)

- ``collections.abc.Callable`` and ``collections.abc.Buffer`` no longer count towards ``too-many-ancestors``. Every other abstract base class in ``collections.abc`` was already ignored, so a class deriving from ``Callable`` was charged for an ancestor while an otherwise identical class deriving from ``Iterable`` was not.

  Refs #11358 (`#11358 <https://github.com/pylint-dev/pylint/issues/11358>`_)

- Fix ``import-private-name`` depending on the order of the checked files: type
  annotations are now collected for each module instead of only for the first
  module checked that contains an import. This removes a false positive on imports
  used only as annotations and a false negative on private imports used at runtime.

  Closes #11466 (`#11466 <https://github.com/pylint-dev/pylint/issues/11466>`_)



Other Changes
-------------

- Clarify how to choose the Python interpreter and ``py-version`` when linting a
  project that supports multiple Python versions.

  Closes #5038 (`#5038 <https://github.com/pylint-dev/pylint/issues/5038>`_)

- You can now set the ``files`` option in configuration files and on the command line.
  Passing files without the ``--files`` flag is still supported. This allows to set
  ``files`` to ``files = my_source_directory`` and invoking ``pylint`` with only
  the ``pylint`` command similar to how other CLI tools allow to do so.
  The help message can always be invoked with ``pylint -h`` or ``pylint --help``.
  Without ``files`` in the configuration and without positional arguments, ``pylint``
  still exits with ``No files to lint``: linting the current directory by default is
  planned for pylint 5.0.

  Refs #5701 (`#5701 <https://github.com/pylint-dev/pylint/issues/5701>`_)

- Removed messages (such as ``print-statement`` or ``apply-builtin``) now have
  their own page in the documentation, with a link to the change that removed
  them. They are also listed in the messages overview alongside renamed messages.

  Closes #6670 (`#6670 <https://github.com/pylint-dev/pylint/issues/6670>`_)

- Documentation for options defined by ``Run``, such as ``--errors-only`` and
  ``--init-hook``, is now generated alongside checker configuration options.

  Closes #6938 (`#6938 <https://github.com/pylint-dev/pylint/issues/6938>`_)

- Document that the ``wrong-import-order`` (C0411) classification of imports as
  third-party vs first-party depends on the current working directory and
  recommend ``known-first-party`` as the deterministic workaround.

  Closes #8801 (`#8801 <https://github.com/pylint-dev/pylint/issues/8801>`_)

- Clarify related ``no-else-*`` messages so they say that only the first ``elif``
  after the reported branch should change. Expand the ``no-else-return``
  documentation to explain later branches and when retaining an ``elif`` chain
  can better communicate an exhaustive decision.

  Closes #9274 (`#9274 <https://github.com/pylint-dev/pylint/issues/9274>`_)

- ``assignment-from-no-return`` now names the callable that does not return anything and,
  for functions listed in the new ``known-side-effects-only-functions`` option, hints at
  the equivalent function to use instead (e.g. ``reversed(...)`` for ``reverse()``).

  Closes #10383 (`#10383 <https://github.com/pylint-dev/pylint/issues/10383>`_)



Internal Changes
----------------

- Add ``assertDoesNotAddMessages`` to ``CheckerTestCase`` to assert that
  specific messages are not emitted, while allowing other messages to be
  present. This complements ``assertNoMessages`` which asserts that no
  messages at all are emitted.

  Refs #9598 (`#9598 <https://github.com/pylint-dev/pylint/issues/9598>`_)

- The primer now pairs residual messages — first by ``(symbol, path, obj)`` and then by
  exact source location — and reports altered messages as a single *changed* entry with
  a compact diff, rather than as a separate removal + addition. The location-based pass
  also catches symbol renames at the same code position (e.g. ``used-before-assignment``
  → ``possibly-used-before-assignment``). When several messages are eligible, the one
  closest to the original line wins, so pairs never cross. New messages are classified
  into fixed false positives (``useless-suppression``), ``astroid-error`` fatal errors,
  and the rest. ``astroid-error`` messages are excluded from pairing (their text embeds
  a unique crash-report path) so persistent crashes keep raising the prominent warning.
  Truncated comments are now cut at a line break and keep their code fences and
  ``<details>`` blocks closed.

  Refs #10914 (`#10914 <https://github.com/pylint-dev/pylint/issues/10914>`_)

- The primer's project cache key is now derived from the commits pinned in
  ``packages_to_prime.json`` instead of the remote branch tips. ``main`` and PR primer
  runs now share the same project cache and lint files in the same on-disk order,
  removing spurious diffs from primer comments (message positions and astroid inference
  results depend on the order in which modules are linted).

  Closes #11192 (`#11192 <https://github.com/pylint-dev/pylint/issues/11192>`_)



Performance Improvements
------------------------

- Lazily import ``isort``, ``dill``, ``multiprocessing``/``concurrent.futures``,
  and ``tomlkit`` so they are only loaded when actually needed.
  This reduces startup time by ~25% (e.g. ``--version``: 91 => 67 ms,
  ``--help``: 176 => 133 ms, single-file lint: 272 => 226 ms).

  Closes #2866 (`#2866 <https://github.com/pylint-dev/pylint/issues/2866>`_)

- Sped up the ``duplicate-code`` checker.  When run inside pylint the
  checker now reuses the already-parsed AST instead of re-parsing every
  file like it has to do when launched via ``symilar``, and it uses a
  rolling hash window with caching across file pairs. Additionally, a
  quadratic blow-up in the hash-matching phase is avoided by switching
  algorithm at a threshold, which previously caused the checker to hang
  on files with many repeated lines.

  Speedup scales with codebase size from 1.5x on small projects
  (~10k lines), to 20x on large ones (500k+ lines). Memory usage also
  drops 12-27%. Codebases that previously hung or were OOM-killed could
  now complete.

  Refs #10881 (`#10881 <https://github.com/pylint-dev/pylint/issues/10881>`_)

- Skip isort classification in the import checker when no import-ordering message is enabled,
  and cache the isort configuration so it is built once instead of once per import statement.
  Skipping the isort processing become a negligible improvement once the caching is applied.
  pylint became ~17% faster on ansible (~=4500 imports) even with isort enabled.

  Refs #10886, #2866, #10637 (`#10886 <https://github.com/pylint-dev/pylint/issues/10886>`_)

- Finding the files to lint with ``--recursive=y`` is faster. Directories matching
  ``ignore``, ``ignore-patterns`` or ``ignore-paths`` (such as ``.venv``, ``.git``
  or ``node_modules``) are no longer walked, and neither are the packages already
  found. In a checkout of pylint with its virtual environment, this step is about
  three times faster when ``.git``, ``.tox`` and ``.venv`` are ignored, and about
  twenty times faster when a large ignored tree is present.

  Directories and files are now also visited in sorted order, so the order in
  which files are linted no longer depends on the file system. The order of
  messages can change once for projects whose file system listed directories in
  another order.

  Closes #11005 (`#11005 <https://github.com/pylint-dev/pylint/issues/11005>`_)
