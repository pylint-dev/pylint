If you document the parameters of your functions, methods and constructors and
their types systematically in your code this optional component might
be useful for you. Sphinx style, Google style, and Numpy style are supported.
(For some examples, see https://pypi.python.org/pypi/sphinxcontrib-napoleon .)

You can activate this checker by adding the line::

    load-plugins=pylint.extensions.docparams

to the ``MASTER`` section of your ``.pylintrc``.

This checker verifies that all function, method, and constructor docstrings
include documentation of the

* parameters and their types
* return value and its type
* exceptions raised

and can handle docstrings in

* Sphinx style (``param``, ``type``, ``return``, ``rtype``,
  ``raise`` / ``except``)::

   def function_foo(x, y, z):
       '''function foo ...

       :param x: bla x
       :type x: int

       :param y: bla y
       :type y: float

       :param int z: bla z

       :return: sum
       :rtype: float

       :raises OSError: bla
       '''
       return x + y + z

* or the Google style (``Args:``, ``Returns:``, ``Raises:``)::

   def function_foo(x, y, z):
       '''function foo ...

       Args:
           x (int): bla x
           y (float): bla y

           z (int): bla z

       Returns:
           float: sum

       Raises:
           OSError: bla
       '''
       return x + y + z

* or the Numpy style (``Parameters``, ``Returns``, ``Raises``)::

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

       Raises
       ------
       OSError
           bla
       '''
       return x + y + z


You'll be notified of **missing parameter documentation** but also of
**naming inconsistencies** between the signature and the documentation which
often arise when parameters are renamed automatically in the code, but not in
the documentation.

Constructor parameters can be documented in either the class docstring or
the ``__init__`` docstring, but not both::

    class ClassFoo(object):
        '''Sphinx style docstring foo

        :param float x: bla x

        :param y: bla y
        :type y: int
        '''
        def __init__(self, x, y):
            pass

    class ClassBar(object):
        def __init__(self, x, y):
            '''Google style docstring bar

            Args:
                x (float): bla x
                y (int): bla y
            '''
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
