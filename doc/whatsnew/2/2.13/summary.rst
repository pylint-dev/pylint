:Release: 2.13
:Date: 2022-03-24

Summary -- Release highlights
=============================

In 2.13, we introduced a new check to deal with unicode security issues. On top of that a lot of work was
done inside the unicode checker by @CarliJoy. We also introduced a new check when importing private name
and for unnecessary ellipsis among other.

We fixed long standing issues related to duplicate code that could not be disabled, line numbers
that were not accurate some of the time, and added the ability to lint all files in a directory without
specifying each one. One of the most anticipated issue from the repository. Thank you @matusvalo !

A lot of ``undefined-variables`` and ``used-before-assignment`` issues were resolved thanks to @jacobtylerwalls.

We started integrating ``pylint-error`` the documentation created by @vald-phoenix a developer from Hlyniane,
Ukraine. We hope he's doing well despite the current situation. The deployment is set up but `there's still a lot to do so we welcome any community effort
help to review, integrate, and add good/bad examples <https://github.com/pylint-dev/pylint/issues/5953>`_. This should be doable
without any pylint or astroid knowledge, so this is the perfect entrypoint if you want to contribute
to pylint without investing any time learning the internals.

This release is the last one to support interpreter below 3.7.2, 3.6 end of life was reached in december 2021.

New checkers
============

* Added several checkers to deal with unicode security issues
  (see `Trojan Sources <https://trojansource.codes/>`_ and
  `PEP 672 <https://peps.python.org/pep-0672/>`_ for details) that also
  concern the readability of the code. In detail the following checks were added:

  * ``bad-file-encoding`` checks that the file is encoded in UTF-8 as suggested by
    `PEP8 <https://peps.python.org/pep-0008/#source-file-encoding>`_.
    UTF-16 and UTF-32 are `not supported by Python <https://bugs.python.org/issue1503789>`_
    at the moment. If this ever changes
    ``invalid-unicode-codec`` checks that they aren't used, to allow for backwards
    compatibility.

  * ``bidirectional-unicode`` checks for bidirectional unicode characters that
    could make code execution different than what the user expects.

  * ``invalid-character-backspace``, ``invalid-character-carriage-return``,
    ``invalid-character-sub``, ``invalid-character-esc``,
    ``invalid-character-zero-width-space`` and ``invalid-character-nul``
    to check for possibly harmful unescaped characters.

  Closes #5281

* ``unnecessary-ellipsis``: Emitted when the ellipsis constant is used unnecessarily.

  Closes #5460

* Added new checker ``typevar-name-missing-variance``. Emitted when a covariant
  or contravariant ``TypeVar`` does not end with  ``_co`` or ``_contra`` respectively or
  when a ``TypeVar`` is not either but has a suffix.

* Add ``modified-iterating-list``, ``modified-iterating-dict``, and ``modified-iterating-set``,
  emitted when items are added to or removed from respectively a list, dictionary or
  set being iterated through.

  Closes #5348

* Add checker ``redefined-slots-in-subclass``: Emitted when a slot is redefined in a subclass.

  Closes #5617

* Rewrote Checker of ``non-ascii-name``.
   It now ensures __all__ Python names are ASCII and also properly
   checks the names of imports (``non-ascii-module-import``) as
   well as file names (``non-ascii-file-name``) and emits their respective new warnings.

   Non ASCII characters could be homoglyphs (look alike characters) and hard to
   enter on a non specialized keyboard.
   See `Confusable Characters in PEP 672`_

.. _`Confusable Characters in PEP 672`: https://peps.python.org/pep-0672/#confusable-characters-in-identifiers

* Added ``cache-max-size-none`` checker with checks for the use of ``functools.lru_cache``
  on class methods with a ``maxsize`` of ``None``. This is unrecommended as it
  creates memory leaks by never letting the instance get garbage collected.

  Closes #5670
  Closes #6180

Removed checkers
================

* Removed the deprecated ``check_docs`` extension. You can use the ``docparams`` checker
  to get the checks previously included in ``check_docs``.

  Closes #5322

Extensions
==========
* New extension ``import-private-name``: indicate imports of external private packages
  and objects (prefixed with ``_``). It can be loaded using ``load-plugins=pylint.extensions.private_import``.

  Closes #5463

* Pyreverse - add output in mermaid-js format and html which is an mermaid js diagram with html boilerplate

* ``TypingChecker``

  * Added new check ``broken-noreturn`` to detect broken uses of ``typing.NoReturn``
    if ``py-version`` is set to Python ``3.7.1`` or below.
    https://bugs.python.org/issue34921

  * Added new check ``broken-collections-callable`` to detect broken uses of ``collections.abc.Callable``
    if ``py-version`` is set to Python ``3.9.1`` or below.
    https://bugs.python.org/issue42965

* ``DocstringParameterChecker``

  * Fixed incorrect classification of Numpy-style docstring as Google-style docstring for
    docstrings with property setter documentation.
    Docstring classification is now based on the highest amount of matched sections instead
    of the order in which the docstring styles were tried.

* ``DocStringStyleChecker``

    * Disable checker ``bad-docstring-quotes`` for Python <= 3.7, because in these versions the line
      numbers for decorated functions and classes are not reliable which interferes with the checker.

   Closes #3077

Other Changes
=============

* Include ``testing_pylintrc`` in source and wheel distributions.

  Closes #6028

* Fix false positive for ``unused-import`` when disabling both ``used-before-assignment`` and ``undefined-variable``.

  Closes #6089

* Fix false positive for ``unnecessary-ellipsis`` when using an ellipsis as a default argument.

  Closes #5973

* Add missing dunder methods to ``unexpected-special-method-signature`` check.

* No longer emit ``no-member`` in for loops that reference ``self`` if the binary operation that
  started the for loop uses a ``self`` that is encapsulated in tuples or lists.

  Refs pylint-dev/astroid#1360
  Closes #4826

* Fix matching ``--notes`` options that end in a non-word character.

  Closes #5840

* The line numbering for messages related to function arguments is now more accurate. This can
  require some message disables to be relocated to updated positions.

* ``using-f-string-in-unsupported-version`` and ``using-final-decorator-in-unsupported-version`` msgids
    were renamed from ``W1601`` and ``W1602`` to ``W2601`` and ``W2602``. Disables using these msgids will break.
    This is done in order to restore consistency with the already existing msgids for ``apply-builtin`` and
    ``basestring-builtin`` from the now deleted python 3K+ checker. There is now a check that we're not using
    existing msgids or symbols from deleted checkers.

  Closes #5729

* Add ``--recursive`` option to allow recursive discovery of all modules and packages in subtree. Running pylint with
  ``--recursive=y`` option will check all discovered ``.py`` files and packages found inside subtree of directory provided
  as parameter to pylint.

  Closes #352

* Updated the position of messages for class and function definitions to no longer cover
  the complete definition. Only the ``def`` or ``class`` + the name of the class/function
  are covered.

  Closes #5466

* Reinstated checks from the python3 checker that are still useful for python 3
  (``eq-without-hash``). This is now in the ``pylint.extensions.eq_without_hash`` optional
  extension.

  Closes #5025

* Fix false-negative for ``assignment-from-none`` checker with list.sort() method.

  Closes #5722

* Fix ``unused-private-member`` false positive when accessing private methods through ``property``.

  Closes #4756

* Fixed crash from ``arguments-differ`` and ``arguments-renamed`` when methods were
  defined outside the top level of a class.

  Closes #5648

* Better warning messages for useless else or elif when a function returns early.

  Closes #5614

* Asterisks are no longer required in Sphinx and Google style parameter documentation
  for ``missing-param-doc`` and are parsed correctly.

  Closes #5815
  Closes #5406

* Fixed an ``AstroidError`` in 2.13.0 raised by the ```duplicate-code``` checker with
  ``ignore-imports`` or ``ignore-signatures`` enabled.

  Closes #6301

* Use the ``tomli`` package instead of ``toml`` to parse ``.toml`` files.

  Closes #5885

* Fixed false positive ``consider-using-dict-comprehension`` when creating a dict
  using a list of tuples where key AND value vary depending on the same condition.

  Closes #5588

* When run in parallel mode ``pylint`` now pickles the data passed to subprocesses with
  the ``dill`` package. The ``dill`` package has therefore been added as a dependency.

* Fixed false positive for ``global-variable-undefined`` when ``global`` is used with a class name

  Closes #3088

* Fixed crash on properties and inherited class methods when comparing them for
  equality against an empty dict.

  Closes #5646

* By default, pylint does no longer take files starting with ``.#`` into account. Those are
  considered `Emacs file locks`_. This behavior can be reverted by redefining the
  ``ignore-patterns`` option.

  Closes #367

.. _`Emacs file locks`: https://www.gnu.org/software/emacs/manual/html_node/elisp/File-Locks.html

* Fix ``super-init-not-called`` when parent or ``self`` is a ``Protocol``

  Closes #4790

* The issue template for crashes is now created for crashes which were previously not covered
  by this mechanism.

  Closes #5668

* An astroid issue where symlinks were not being taken into account
  was fixed

  Closes #1470
  Closes #3499
  Closes #4302
  Closes #4798
  Closes #5081

* Fix false negative for ``undefined-variable`` and related variable messages
  when the same undefined variable is used as a type annotation and is
  accessed multiple times, or is used as a default argument to a function.

  Closes #5399

* Emit ``used-before-assignment`` instead of ``undefined-variable`` when attempting
  to access unused type annotations.

  Closes #5713

* Fixed an issue where ``ungrouped-imports`` could not be disabled without raising
  ``useless-suppression``.

  Refs #2366

* Fixed a crash on ``__init__`` nodes when the attribute was previously uninferable due to a cache
  limit size. This limit can be hit when the inheritance pattern of a class (and therefore of the ``__init__`` attribute) is very large.

  Closes #5679

* Fixed extremely long processing of long lines with comma's.

  Closes #5483

* Fix false positive ``super-init-not-called`` for classes that inherit their ``init`` from
  a parent.

  Closes #4941

* Fix false positives for ``used-before-assignment`` from using named
  expressions in a ternary operator test and using that expression as
  a call argument.

  Closes #5177, #5212

* Fixed crash with recursion error for inference of class attributes that referenced
  the class itself.

  Closes #5408
  Refs pylint-dev/astroid#1392

* Fixed false positive for ``unused-argument`` when a method overridden in a subclass
  does nothing with the value of a keyword-only argument.

  Closes #5771
  Refs pylint-dev/astroid#1382

* Optimize parsing of long lines when ``missing-final-newline`` is enabled.

  Closes #5724

* Fix false positive for ``used-before-assignment`` from a class definition
  nested under a function subclassing a class defined outside the function.

  Closes #4590

* Fix ``unnecessary_dict_index_lookup`` false positive when deleting a dictionary's entry.

  Closes #4716

* Fix false positive for ``used-before-assignment`` when an except handler
  shares a name with a test in a filtered comprehension.

  Closes #5817

* Fix a crash in ``unused-private-member`` checker when analyzing code using
  ``type(self)`` in bound methods.

  Closes #5569

* Fix crash in ``unnecessary-dict-index-lookup`` checker if the output of
  ``items()`` is assigned to a 1-tuple.

  Closes #5504

* Fixed crash with slots assignments and annotated assignments.

  Closes #5479

* Fixed a crash in ``unspecified-encoding`` checker when providing ``None``
  to the ``mode`` argument of an ``open()`` call.

  Closes #5731

* Fixed a crash involving a ``NewType`` named with an f-string.

  Closes #5770
  Refs pylint-dev/astroid#1400

* Improved ``bad-open-mode`` message when providing ``None`` to the ``mode``
  argument of an ``open()`` call.

  Closes #5733

* Fix false negative for ``consider-iterating-dictionary`` during membership checks encapsulated in iterables
  or ``not in`` checks

  Closes #5323

* Allow disabling ``duplicate-code`` with a disable comment when running through
  pylint.

  Closes #214

* Fix false positive for ``undefined-variable`` when ``namedtuple`` class
  attributes are used as return annotations.

  Closes #5568

* Added confidence level ``CONTROL_FLOW`` for warnings relying on assumptions
  about control flow.

* ``used-before-assignment`` now considers that assignments in a try block
  may not have occurred when the except or finally blocks are executed.

  Closes #85, #2615

* Fixed false negative for ``used-before-assignment`` when a conditional
  or context manager intervened before the try statement that suggested
  it might fail.

  Closes #4045

* Fixed false negative for ``used-before-assignment`` in finally blocks
  if an except handler did not define the assignment that might have failed
  in the try block.

* Fix a false positive for ``assigning-non-slot`` when the slotted class
  defined ``__setattr__``.

  Closes #3793

* Fixed a false positive for ``invalid-class-object`` when the object
  being assigned to the ``__class__`` attribute is uninferable.

* Added a ``testutil`` extra require to the packaging, as ``gitpython`` should not be a dependency
  all the time but is still required to use the primer helper code in ``pylint.testutil``. You can
  install it with ``pip install pylint[testutil]``.

  Closes #5486

* Fixed a false positive for ``used-before-assignment`` when a named expression
  appears as the first value in a container.

  Closes #5112

* Fixed false positive for ``used-before-assignment`` with self-referential type
  annotation in conditional statements within class methods.

  Closes #5499

* ``used-before-assignment`` now assumes that assignments in except blocks
  may not have occurred and warns accordingly.

  Closes #4761

* When evaluating statements after an except block, ``used-before-assignment``
  assumes that assignments in the except blocks took place if the
  corresponding try block contained a return statement.

  Closes #5500

* Fixed a false negative for ``used-before-assignment`` when some but not all
  except handlers defined a name relied upon after an except block when the
  corresponding try block contained a return statement.

  Closes #5524

* When evaluating statements in the ``else`` clause of a loop, ``used-before-assignment``
  assumes that assignments in the except blocks took place if the
  except handlers constituted the only ways for the loop to finish without
  breaking early.

  Closes #5683

* ``used-before-assignment`` now checks names in try blocks.

* Fixed false positive with ``used-before-assignment`` for assignment expressions
  in lambda statements.

  Closes #5360, #3877

* Improve ``invalid-name`` check for ``TypeVar`` names.
  The accepted pattern can be customized with ``--typevar-rgx``.

  Closes #3401

* Fixed a false positive (affecting unreleased development) for
  ``used-before-assignment`` involving homonyms between filtered comprehensions
  and assignments in except blocks.

  Closes #5586

* Fixed crash on list comprehensions that used ``type`` as inner variable name.

  Closes #5461

* Fixed crash in ``use-maxsplit-arg`` checker when providing the ``sep`` argument
  to ``str.split()`` by keyword.

  Closes #5737

* Fix false positive for ``unused-variable`` for a comprehension variable matching
  an outer scope type annotation.

  Closes #5326

* Fix false negative for ``undefined-variable`` for a variable used multiple times
  in a comprehension matching an unused outer scope type annotation.

  Closes #5654

* Require Python ``3.6.2`` to run pylint.

  Closes #5065

* Fixed crash on uninferable decorators on Python 3.6 and 3.7

* Emit ``redefined-outer-name`` when a nested except handler shadows an outer one.

  Closes #4434
  Closes #5370

* ``encoding`` can now be supplied as a positional argument to calls that open
  files without triggering ``unspecified-encoding``.

  Closes #5638

* Fatal errors now emit a score of 0.0 regardless of whether the linted module
  contained any statements

  Closes #5451

* ``fatal`` was added to the variables permitted in score evaluation expressions.

* The default score evaluation now uses a floor of 0.

  Closes #2399

* Fix ``comparison-with-callable`` false positive for callables that raise, such
  as typing constants.

  Closes #5557

* When invoking ``pylint``, ``epylint``, ``symilar`` or ``pyreverse`` by importing them in a python file
  you can now pass an ``argv`` keyword besides patching ``sys.argv``.

  Closes #5320

* The ``PyLinter`` class will now be initialized with a ``TextReporter``
  as its reporter if none is provided.

* Fix false positive ``not-callable`` with attributes that alias ``NamedTuple``

  Fixes part of #1730

* The ``testutils`` for unittests now accept ``end_lineno`` and ``end_column``. Tests
  without these will trigger a ``DeprecationWarning``.

* ``arguments-differ`` will no longer complain about method redefinitions with extra parameters
  that have default values.

  Closes #1556, #5338

* Disables for ``deprecated-module`` and similar warnings for stdlib features deprecated
  in newer versions of Python no longer raise ``useless-suppression`` when linting with
  older Python interpreters where those features are not yet deprecated.

* Importing the deprecated stdlib module ``xml.etree.cElementTree`` now emits ``deprecated_module``.

  Closes #5862

* Importing the deprecated stdlib module ``distutils`` now emits ``deprecated_module`` on Python 3.10+.

* Fixed false positive ``unexpected-keyword-arg`` for decorators.

  Closes #258

* ``missing-raises-doc`` will now check the class hierarchy of the raised exceptions

  .. code-block:: python

    def my_function():
      """My function.

      Raises:
        Exception: if something fails
      """
      raise ValueError

  Closes #4955

* Fixed false positive for ``unused-variable`` when a ``nonlocal`` name is assigned as part of a multi-name assignment.

  Closes #3781

* Fix false positive - Allow unpacking of ``self`` in a subclass of ``typing.NamedTuple``.

  Closes #5312

* Fixed false negative ``unpacking-non-sequence`` when value is an empty list.

  Closes #5707

* Fixed false positive for ``global-variable-not-assigned`` when the ``del`` statement is used

  Closes #5333

* Fix type hints in class diagrams generated by pyreverse for class methods and methods returning None.

* Output better error message if unsupported file formats are used with ``pyreverse``.

  Closes #5950

* Fixed false positive for ``unused-argument`` when a ``nonlocal`` name is used
  in a nested function that is returned without being called by its parent.

  Closes #5187

* Avoid emitting ``raising-bad-type`` when there is inference ambiguity on
  the variable being raised.

  Closes #2793

* Fix false positive for ``superfluous-parens`` for patterns like
  "return (a or b) in iterable".

  Closes #5803

* Fix a crash in the ``unsupported-membership-test`` checker when assigning
  multiple constants to class attributes including ``__iter__`` via unpacking.

  Closes #6366

* Fix false positive for ``used-before-assignment`` for assignments taking place via
  nonlocal declarations after an earlier type annotation.

  Closes #5394

* Fixed a false positive for ``unused-variable`` when a builtin specified in
  ``--additional-builtins`` is given a type annotation.

  Closes #6388

* Fix false positive for 'nonexistent-operator' when repeated '-' are
  separated (e.g. by parens).

  Closes #5769

* Fix a false positive for ``undefined-loop-variable`` when the ``else`` of a ``for``
  loop raises or returns.

  Closes #5971

* Only raise ``not-callable`` when all the inferred values of a property are not callable.

  Closes #5931

* Fix false positive for ``unused-variable`` for classes inside functions
  and where a metaclass is provided via a call.

  Closes #4020

* Avoid reporting ``superfluous-parens`` on expressions using the ``is not`` operator.

  Closes #5930

* Fix a false positive for ``undefined-loop-variable`` for a variable used in a lambda
  inside the first of multiple loops.

  Closes #6419

* Fix false positive for ``unsubscriptable-object`` in Python 3.8 and below for
  statements guarded by ``if TYPE_CHECKING``.

  Closes #3979

* Fix a crash when accessing ``__code__`` and assigning it to a variable.

  Closes #6539

* Fix a crash when linting a file that passes an integer ``mode=`` to
  ``open``

  Closes #6414

* Fix false positives for ``no-name-in-module`` and ``import-error`` for ``numpy.distutils``
  and ``pydantic``.

  Closes #6497

* Fix ``IndexError`` crash in ``uninferable_final_decorators`` method.

  Refs #6531

* Fix a crash in ``unnecessary-dict-index-lookup`` when subscripting an attribute.

  Closes #6557

* Fix a false positive for ``undefined-loop-variable`` when using ``enumerate()``.

  Closes #6593
