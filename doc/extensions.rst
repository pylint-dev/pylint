
Optional Pylint checkers in the extensions module
=================================================

Parameter documentation checker
-------------------------------

If you document the parameters of your functions, methods and constructors and
their types systematically in your code this optional component might
be useful for you. Sphinx style, Google style, and Numpy style are supported.
(For some examples, see https://pypi.python.org/pypi/sphinxcontrib-napoleon .)

You can activate this checker by adding the line::

    load-plugins=pylint.extensions.docparams

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
tolerated without any warnings. If you want to switch off this behavior
(forcing functions to document their parameters), set the option
``accept-no-param-doc`` to ``no`` in your ``.pylintrc``.

By default, omitting the exception raising documentation of a function
altogether is tolerated without any warnings. If you want to switch off this
behavior (forcing functions that raise exceptions to document them), set the
option ``accept-no-raise-doc`` to ``no`` in your ``.pylintrc``.

By default, omitting the return documentation of a function altogether is
tolerated without any warnings. If you want to switch off this behavior
(forcing functions to document their returns), set the option
``accept-no-return-doc`` to ``no`` in your ``.pylintrc``.


Prohibit builtin checker
------------------------

This used to be the ``bad-builtin`` core checker, but it was moved to
an extension instead. It can be used for finding prohibited used builtins,
such as ``map`` or ``filter``, for which other alternatives exists.

If you want to control for what builtins the checker should warn about,
you can use the ``bad-functions`` option::

    $ pylint a.py --load-plugins=pylint.extensions.bad_builtin --bad-functions=apply,reduce
    ...


.. _mccabe_extension:

Complexity checker
------------------

You can now use this plugin for finding complexity issues in your code base.

Activate it through ``pylint --load-plugins=pylint.extensions.mccabe``. It introduces
a new warning, ``too-complex``, which is emitted when a code block has a complexity
higher than a preestablished value, which can be controlled through the
``max-complexity`` option, such as in this example::

    $ cat a.py
    def f10():
        """McCabe rating: 11"""
        myint = 2
        if myint == 5:
            return myint
        elif myint == 6:
            return myint
        elif myint == 7:
            return myint
        elif myint == 8:
            return myint
        elif myint == 9:
            return myint
        elif myint == 10:
            if myint == 8:
                while True:
                    return True
            elif myint == 8:
                with myint:
                    return 8
        else:
            if myint == 2:
                return myint
            return myint
        return myint
    $ pylint a.py --load-plugins=pylint.extensions.mccabe
    R:1: 'f10' is too complex. The McCabe rating is 11 (too-complex)
    $ pylint a.py --load-plugins=pylint.extensions.mccabe --max-complexity=50
    $
