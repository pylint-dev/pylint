:Release: 2.4
:Date: 2019-09-24


Summary -- Release highlights
=============================


New checkers
============

* ``import-outside-toplevel``

  This check warns when modules are imported from places other than a
  module toplevel, e.g. inside a function or a class.

* Added a new check, ``consider-using-sys-exit``

  This check is emitted when we detect that a quit() or exit() is invoked
  instead of sys.exit(), which is the preferred way of exiting in program.

  Closes #2925

* Added a new check, ``arguments-out-of-order``

  This check warns if you have arguments with names that match those in
  a function's signature but you are passing them in to the function
  in a different order.

  Closes #2975

* Added new checks, ``no-else-break`` and ``no-else-continue``

  These checks highlight unnecessary ``else`` and ``elif`` blocks after
  ``break`` and ``continue`` statements.

  Closes #2327

* Added ``unnecessary-comprehension`` that detects unnecessary comprehensions.

  This check is emitted when ``pylint`` finds list-, set- or dict-comprehensions,
  that are unnecessary and can be rewritten with the list-, set- or dict-constructors.

  Closes #2905

* Added a new check, ``invalid-overridden-method``

  This check is emitted when we detect that a method is overridden
  as a property or a property is overridden as a method. This can indicate
  a bug in the application code that will trigger a runtime error.

  Closes #2670

* Added a new check, ``redeclared-assigned-name``

  This check is emitted when ``pylint`` detects that a name was assigned one or multiple times in the same assignment,
  which indicate a potential bug.

  Closes #2898

* Added a new check, ``self-assigning-variable``

  This check is emitted when we detect that a variable is assigned
  to itself, which might indicate a potential bug in the code application.

  For example, the following would raise this warning::

    def new_a(attr, attr2):
      a_inst = Aclass()
      a_inst.attr2 = attr2
      # should be: a_inst.attr = attr, but have a typo
      attr = attr
      return a_inst

  Closes #2930

* Added a new check ``property-with-parameters`` which detects when a property
  has more than a single argument.

  Closes #3006

* Added ``subprocess-run-check`` to handle subprocess.run without explicitly set ``check`` keyword.

  Closes #2848

* We added a new check message ``dict-iter-missing-items``.
  This is emitted when trying to iterate through a dict in a for loop without calling its .items() method.

  Closes #2761

* We added a new check message ``missing-parentheses-for-call-in-test``.
  This is emitted in case a call to a function is made inside a test but
  it misses parentheses.

* A new check ``class-variable-slots-conflict`` was added.

  This check is emitted when ``pylint`` finds a class variable that conflicts with a slot
  name, which would raise a ``ValueError`` at runtime.

  For example, the following would raise an error::

    class A:
        __slots__ = ('first', 'second')
        first = 1

* A new check ``preferred-module`` was added.

  This check is emitted when ``pylint`` finds an imported module that has a
  preferred replacement listed in ``preferred-modules``.

  For example, you can set the preferred modules as ``xml:defusedxml,json:ujson``
  to make ``pylint`` suggest using ``defusedxml`` instead of ``xml``
  and ``ujson`` rather than ``json``.

* A new extension ``broad_try_clause`` was added.

  This extension enforces a configurable maximum number of statements inside
  of a try clause. This facilitates enforcing PEP 8's guidelines about try / except
  statements and the amount of code in the try clause.

  You can enable this extension using ``--load-plugins=pylint.extensions.broad_try_clause``
  and you can configure the amount of statements in a try statement using
  ``--max-try-statements``.


Other Changes
=============

* Don't emit ``protected-access`` when a single underscore prefixed attribute is used
  inside a special method

  Closes #1802

* ``len-as-condition`` now only fires when a ``len(x)`` call is made without an explicit comparison.

  The message and description accompanying this checker has been changed
  reflect this new behavior, by explicitly asking to either rely on the
  fact that empty sequence are false or to compare the length with a scalar.

  OK::

    if len(x) == 0:
      pass

    while not len(x) == 0:
      pass

    assert len(x) > 5, message

  KO::

    if not len(x):
      pass

    while len(x) and other_cond:
      pass

    assert len(x), message

* A file is now read from stdin if the ``--from-stdin`` flag is used on the
  command line. In addition to the ``--from-stdin`` flag a (single) file
  name needs to be specified on the command line, which is needed for the
  report.

* The checker for ungrouped imports is now more permissive.

The import can now be sorted alphabetically by import style.
This makes pylint compatible with isort.

The following imports do not trigger an ``ungrouped-imports`` anymore ::

    import unittest
    import zipfile
    from unittest import TestCase
    from unittest.mock import MagicMock

* The checker for missing return documentation is now more flexible.

The following does not trigger a ``missing-return-doc`` anymore ::

    def my_func(self):
        """This is a docstring.

        Returns
        -------
        :obj:`list` of :obj:`str`
            List of strings
        """
        return ["hi", "bye"] #@

* ``signature-mutators`` CLI and config option was added.

With this option, users can choose to ignore ``too-many-function-args``, ``unexpected-keyword-arg``,
and ``no-value-for-parameter`` for functions decorated with decorators that change
the signature of a decorated function.

For example a test may want to make use of hypothesis.
Adding ``hypothesis.extra.numpy.arrays`` to ``signature_mutators``
would mean that ``no-value-for-parameter`` would not be raised for::

    @given(img=arrays(dtype=np.float32, shape=(3, 3, 3, 3)))
    def test_image(img):
        ...

* Allow the option of f-strings as a valid logging string formatting method.

``logging-fstring--interpolation`` has been merged into
``logging-format-interpolation`` to allow the ``logging-format-style`` option
to control which logging string format style is valid.
To allow this, a new ``fstr`` value is valid for the ``logging-format-style``
option.

* ``--list-msgs-enabled`` command was added.

When enabling/disabling several messages and groups in a config file,
it can be unclear which messages are actually enabled and which are disabled.
This new command produces the final resolved lists of enabled/disabled messages,
sorted by symbol but with the ID provided for use with ``--help-msg``.
