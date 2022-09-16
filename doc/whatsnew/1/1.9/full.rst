Full changelog
==============

What's New in Pylint 1.9?
-------------------------

Release date: 2018-05-15

* Added two new Python 3 porting checks, ``exception-escape`` and ``comprehension-escape``

  These two are emitted whenever pylint detects that a variable defined in the
  said blocks is used outside of the given block. On Python 3 these values are deleted.

* Added a new ``deprecated-sys-function``, emitted when accessing removed sys members.

* Added ``xreadlines-attribute``, emitted when the ``xreadlines()`` attribute is accessed.

* The Python 3 porting mode can now run with Python 3 as well.

* docparams extension allows abstract methods to document what overriding
  implementations should return, and to raise NotImplementedError without
  documenting it.

  Closes #2044

* Special methods do not count towards ``too-few-methods``,
  and are considered part of the public API.

* Enum classes do not trigger ``too-few-methods``

  Closes #605

* Added a new Python 2/3 check for accessing ``operator.div``, which is removed in Python 3

  Closes #1936

* Added a new Python 2/3 check for accessing removed urllib functions

  Closes #1997
