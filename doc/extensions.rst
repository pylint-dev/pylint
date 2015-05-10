
Optional Pylint checkers in the extensions module
=================================================

Parameter documentation checker
-------------------------------

If you document the parameters of your functions, methods and constructors and
their types systematically in your code this optional component might
be useful for you. Sphinx style, Google style, and Numpy style are supported.
(For some examples, see https://pypi.python.org/pypi/sphinxcontrib-napoleon .)

You can activate this checker by adding the line::

    load-plugins=pylint.extensions.check_docs

to the ``MASTER`` section of your ``.pylintrc``.

This checker verifies that all function, method, and constructor parameters are
mentioned in the

* Sphinx ``param`` and ``type`` parts of the docstring::

   def function_foo(x, y, z):
       '''function foo ...

       :param x: bla x
       :type x: int

       :param y: bla y
       :type y: float

       :param int z: bla z

       :return: sum
       :rtype: float
       '''
       return x + y + z

* or the Google style ``Args:`` part of the docstring::

   def function_foo(x, y, z):
       '''function foo ...

       Args:
           x (int): bla x
           y (float): bla y

           z (int): bla z

       Returns:
           float: sum
       '''
       return x + y + z

* or the Numpy style ``Parameters`` part of the docstring::

   def function_foo(x, y, z):
       '''function foo ...

       Parameters
       ----------
       x: int
           bla x
       y: float
           bla y

       z: int
           bla z

       Returns
       -------
       float
           sum
       '''
       return x + y + z


You'll be notified of **missing parameter documentation** but also of
**naming inconsistencies** between the signature and the documentation which
often arise when parameters are renamed automatically in the code, but not in
the documentation.

By convention, constructor parameters are documented in the class docstring.
(``__init__`` and ``__new__`` methods are considered constructors.)::

    class ClassFoo(object):
        '''Sphinx style docstring foo

        :param float x: bla x

        :param y: bla y
        :type y: int
        '''
        def __init__(self, x, y):
            pass

    class ClassFoo(object):
        '''Google style docstring foo

        Args:
            x (float): bla x
            y (int): bla y
        '''
        def __init__(self, x, y):
            pass

In some cases, having to document all parameters is a nuisance, for instance if
many of your functions or methods just follow a **common interface**. To remove
this burden, the checker accepts missing parameter documentation if one of the
following phrases is found in the docstring:

* For the other parameters, see
* For the parameters, see

(with arbitrary whitespace between the words). Please add a link to the
docstring defining the interface, e.g. a superclass method, after "see"::

   def callback(x, y, z):
       '''Sphinx style docstring for callback ...

       :param x: bla x
       :type x: int

       For the other parameters, see
       :class:`MyFrameworkUsingAndDefiningCallback`
       '''
       return x + y + z

   def callback(x, y, z):
       '''Google style docstring for callback ...

       Args:
           x (int): bla x

       For the other parameters, see
       :class:`MyFrameworkUsingAndDefiningCallback`
       '''
       return x + y + z

Naming inconsistencies in existing parameter and their type documentations are
still detected.

By default, omitting the parameter documentation of a function altogether is
tolerated without any warnings. If you want to switch off this behavior,
set the option ``accept-no-param-doc`` to ``yes`` in your ``.pylintrc``.
