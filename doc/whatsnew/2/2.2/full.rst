Full changelog
==============

What's New in Pylint 2.2.2?
---------------------------
Release date: 2018-11-28

* Change the ``logging-format-style`` to use name identifier instead of their
  corresponding Python identifiers

  This is to prevent users having to think about escaping the default value for
  ``logging-format-style`` in the generated config file. Also our config parsing
  utilities don't quite support escaped values when it comes to ``choices`` detection,
  so this would have needed various hacks around that.

  Closes #2614


What's New in Pylint 2.2.1?
---------------------------
Release date: 2018-11-27

* Fix a crash caused by ``implicit-str-concat-in-sequence`` and multi-bytes characters.

  Closes #2610


What's New in Pylint 2.2?
-------------------------

Release date: 2018-11-25

* Consider ``range()`` objects for ``undefined-loop-variable`` leaking from iteration.

  Closes #2533

* ``deprecated-method`` can use the attribute name for identifying a deprecated method

 Previously we were using the fully qualified name, which we still do, but the fully
 qualified name for some ``unittest`` deprecated aliases leads to a generic
 deprecation function. Instead on relying on that, we now also rely on the attribute
 name, which should solve some false positives.

  Closes #1653
  Closes #1946

* Fix compatibility with changes to stdlib tokenizer.

* ``pylint`` is less eager to consume the whole line for pragmas

  Closes #2485

* Obtain the correct number of CPUs for virtualized or containerized environments.

  Closes #2519

* Change ``unbalanced-tuple-unpacking`` back to a warning.

 It used to be a warning until a couple of years ago, after it was promoted to
 an error. But the check might be suggesting the wrong thing in some cases,
 for instance when checking against ``sys.argv`` which cannot be known at static
 analysis time. Given it might rely on potential unknown data, it's best to
 have it as a warning.

  Closes #2522

* Remove ``enumerate`` usage suggestion when defining ``__iter__`` (C0200)

  Closes #2477

* Emit ``too-many-starred-assignment`` only when the number of Starred nodes is per assignment elements

  Closes #2513

* ``try-except-raise`` checker now handles multilevel inheritance hirerachy for exceptions correctly.

  Closes #2484

* Add a new check, ``simplifiable-if-expression`` for expressions like ``True if cond else False``.

  Closes #2487

* ``too-few-public-methods`` is not reported for ``typing.NamedTuple``

  Closes #2459

* ```too-few-public-methods`` is not reported for dataclasses created with options.

  Closes #2488

* Remove wrong modules from 'bad-python3-import'.

  Closes #2453

* The ``json`` reporter prints an empty list when no messages are emitted

  Closes #2446

* Add a new check, ``duplicate-string-formatting-argument``

 This new check is emitted whenever a duplicate string formatting argument
 is found.

  Closes #497

* ``assignment-from-no-return`` is not emitted for coroutines.

  Closes #1715

* Report format string type mismatches.

* ``consider-using-ternary`` and ``simplified-boolean-expression`` no longer emit for sequence based checks

  Closes #2473

* Handle ``AstroidSyntaxError`` when trying to import a module.

  Closes #2313

* Allow ``__module__`` to be redefined at a class level.

  Closes #2451

* ``pylint`` used to emit an ``unused-variable`` error if unused import was found in the function. Now instead of
  ``unused-variable``, ``unused-import`` is emitted.

  Closes #2421

* Handle asyncio.coroutine when looking for ``not-an-iterable`` check.

  Closes #996

* The ``locally-enabled`` check is gone.

  Closes #2442

* Infer decorated methods when looking for method-hidden

  Closes #2369

* Pick the latest value from the inferred values when looking for ``raising-non-exception``

  Closes #2431

* Extend the TYPE_CHECKING guard to TYPE_CHECKING name as well, not just the attribute

  Closes #2411

* Ignore import x.y.z as z cases for checker ``useless-import-alias``.

  Closes #2309

* Fix false positive ``undefined-variable`` and ``used-before-assignment`` with nonlocal keyword usage.

  Closes #2049

* Stop ``protected-access`` exception for missing class attributes

* Don't emit ``assignment-from-no-return`` for decorated function nodes

  Closes #2385

* ``unnecessary-pass`` is now also emitted when a function or class contains only docstring and pass statement.

  In Python, stubbed functions often have a body that contains just a single ``pass`` statement,
  indicating that the function doesn't do anything. However, a stubbed function can also have just a
  docstring, and function with a docstring and no body also does nothing.

  Closes #2208

* ``duplicate-argument-name`` is emitted for more than one duplicate argument per function

  Closes #1712

* Allow double indentation levels for more distinguishable indentations

  Closes #741

* Consider tuples in exception handler for ``try-except-raise``.

  Closes #2389

* Fix astroid.ClassDef check in checkers.utils.is_subclass_of

* Fix wildcard imports being ignored by the import checker

* Fix external/internal distinction being broken in the import graph

* Fix wildcard import check not skipping ``__init__.py``

  Closes #2430

* Add new option to logging checker, ``logging_format_style``

* Fix --ignore-imports to understand multi-line imports

  Closes #1422
  Closes #2019

* Add a new check 'implicit-str-concat-in-sequence' to spot string concatenation inside lists, sets & tuples.

* ``literal-comparison`` is now emitted for 0 and 1 literals.
