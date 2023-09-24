Full changelog
==============

What's New in Pylint 2.1.1?
---------------------------
Release date: 2018-08-07

* fix pylint crash due to ``misplaced-format-function`` not correctly handling class attribute.

  Closes #2384

* Do not emit \*-builtin for Python 3 builtin checks when the builtin is used inside a try-except

  Closes #2228

* ``simplifiable-if-statement`` not emitted when dealing with subscripts


What's New in Pylint 2.1?
-------------------------

Release date: 2018-08-01

* ``trailing-comma-tuple`` gets emitted for ``yield`` statements as well.

  Closes #2363

* Get only the arguments of the scope function for ``redefined-argument-from-local``

  Closes #2364

* Add a check ``misplaced-format-function`` which is emitted if format function is used on
  non str object.

  Closes #2200

* ``chain.from_iterable`` no longer emits `dict-{}-not-iterating` when dealing with dict values and keys

* Demote the ``try-except-raise`` message from an error to a warning (E0705 -> W0706)

  Closes #2323

* Correctly handle the new name of the Python implementation of the ``abc`` module.

  Closes pylint-dev/astroid#2288

* Modules with ``__getattr__`` are exempted by default from ``no-member``

  There's no easy way to figure out if a module has a particular member when
  the said module uses ``__getattr__``, which is a new addition to Python 3.7.
  Instead we assume the safe thing to do, in the same way we do for classes,
  and skip those modules from checking.

  Closes #2331

* Fix a false positive ``invalid name`` message when method or attribute name is longer then 30 characters.

  Closes #2047

* Include the type of the next branch in ``no-else-return``

  Closes #2295

* Fix inconsistent behaviour for bad-continuation on first line of file

  Closes #2281

 * Fix not being able to disable certain messages on the last line through
   the global disable option

  Closes #2278

* Don't emit ``useless-return`` when we have a single statement that is the return itself

  We still want to be explicit when a function is supposed to return
  an optional value; even though ``pass`` could still work, it's not explicit
  enough and the function might look like it's missing an implementation.

  Closes #2300

* Fix false-positive undefined-variable for self referential class name in lamdbas

  Closes #704

* Don't crash when ``pylint`` is unable to infer the value of an argument to ``next()``

  Closes #2316

* Don't emit ``not-an-iterable`` when dealing with async iterators.

  But do emit it when using the usual iteration protocol against
  async iterators.

  Closes #2311

* Can specify a default docstring type for when the check cannot guess the type

  Closes #1169
