
Optional Pylint checkers in the extensions module
=================================================

Sphinx parameter documentation checker
--------------------------------------

If you're using Sphinx to document your code, this optional component might
be useful for you. You can activate it by adding the line::

    load-plugins=pylint.extensions.check_docs

to the ``MASTER`` section of your ``.pylintrc``.

This checker verifies that all function, method, and constructor parameters are
mentioned in the Sphinx ``param`` and ``type`` parts of the docstring::

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

You'll be notified of **missing parameter documentation** but also of
**naming inconsistencies** between the signature and the documentation which
often arise when parameters are renamed automatically in the code, but not in the
documentation.

By convention, constructor parameters are documented in the class docstring.
(``__init__`` and ``__new__`` methods are considered constructors.)::

    class ClassFoo(object):
        '''docstring foo

        :param float x: bla x

        :param y: bla y
        :type y: int
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
       '''callback ...

       :param x: bla x
       :type x: int

       For the other parameters, see
       :class:`MyFrameworkUsingAndDefiningCallback`
       '''
       return x + y + z

Naming inconsistencies in existing ``param`` and ``type`` documentations are
still detected.
