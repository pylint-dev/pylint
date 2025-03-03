Optional checkers
=================

.. This file is auto-generated. Make any changes to the associated
.. docs extension in 'doc/exts/pylint_extensions.py'.

Pylint provides the following optional plugins:

- :ref:`pylint.extensions.bad_builtin`
- :ref:`pylint.extensions.broad_try_clause`
- :ref:`pylint.extensions.check_elif`
- :ref:`pylint.extensions.code_style`
- :ref:`pylint.extensions.comparison_placement`
- :ref:`pylint.extensions.confusing_elif`
- :ref:`pylint.extensions.consider_refactoring_into_while_condition`
- :ref:`pylint.extensions.consider_ternary_expression`
- :ref:`pylint.extensions.dict_init_mutate`
- :ref:`pylint.extensions.docparams`
- :ref:`pylint.extensions.docstyle`
- :ref:`pylint.extensions.dunder`
- :ref:`pylint.extensions.empty_comment`
- :ref:`pylint.extensions.eq_without_hash`
- :ref:`pylint.extensions.for_any_all`
- :ref:`pylint.extensions.magic_value`
- :ref:`pylint.extensions.mccabe`
- :ref:`pylint.extensions.no_self_use`
- :ref:`pylint.extensions.overlapping_exceptions`
- :ref:`pylint.extensions.private_import`
- :ref:`pylint.extensions.redefined_loop_name`
- :ref:`pylint.extensions.redefined_variable_type`
- :ref:`pylint.extensions.set_membership`
- :ref:`pylint.extensions.typing`
- :ref:`pylint.extensions.while_used`

You can activate any or all of these extensions by adding a ``load-plugins`` line to the ``MAIN`` section of your ``.pylintrc``, for example::

    load-plugins=pylint.extensions.docparams,pylint.extensions.docstyle

.. _pylint.extensions.broad_try_clause:

Broad Try Clause checker
~~~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.broad_try_clause``.
Verbatim name of the checker is ``broad_try_clause``.

See also :ref:`broad_try_clause checker's options' documentation <broad_try_clause-options>`

Broad Try Clause checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:too-many-try-statements (W0717):
  Try clause contains too many statements.


.. _pylint.extensions.code_style:

Code Style checker
~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.code_style``.
Verbatim name of the checker is ``code_style``.

Code Style checker Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Checkers that can improve code consistency.
As such they don't necessarily provide a performance benefit and
are often times opinionated.

See also :ref:`code_style checker's options' documentation <code_style-options>`

Code Style checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^
:consider-using-tuple (R6102): *Consider using an in-place tuple instead of list*
  Only for style consistency! Emitted where an in-place defined ``list`` can be
  replaced by a ``tuple``. Due to optimizations by CPython, there is no
  performance benefit from it.
:consider-using-namedtuple-or-dataclass (R6101): *Consider using namedtuple or dataclass for dictionary values*
  Emitted when dictionary values can be replaced by namedtuples or dataclass
  instances.
:prefer-typing-namedtuple (R6105): *Prefer 'typing.NamedTuple' over 'collections.namedtuple'*
  'typing.NamedTuple' uses the well-known 'class' keyword with type-hints for
  readability (it's also faster as it avoids an internal exec call). Disabled
  by default!
:consider-using-assignment-expr (R6103): *Use '%s' instead*
  Emitted when an if assignment is directly followed by an if statement and
  both can be combined by using an assignment expression ``:=``. Requires
  Python 3.8 and ``py-version >= 3.8``.
:consider-using-augmented-assign (R6104): *Use '%s' to do an augmented assign directly*
  Emitted when an assignment is referring to the object that it is assigning
  to. This can be changed to be an augmented assign. Disabled by default!


.. _pylint.extensions.comparison_placement:

Comparison-Placement checker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.comparison_placement``.
Verbatim name of the checker is ``comparison-placement``.

Comparison-Placement checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:misplaced-comparison-constant (C2201): *Comparison should be %s*
  Used when the constant is placed on the left side of a comparison. It is
  usually clearer in intent to place it in the right hand side of the
  comparison.


.. _pylint.extensions.confusing_elif:

Confusing Elif checker
~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.confusing_elif``.
Verbatim name of the checker is ``confusing_elif``.

Confusing Elif checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:confusing-consecutive-elif (R5601): *Consecutive elif with differing indentation level, consider creating a function to separate the inner elif*
  Used when an elif statement follows right after an indented block which
  itself ends with if or elif. It may not be obvious if the elif statement was
  willingly or mistakenly unindented. Extracting the indented if statement into
  a separate function might avoid confusion and prevent errors.


.. _pylint.extensions.for_any_all:

Consider-Using-Any-Or-All checker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.for_any_all``.
Verbatim name of the checker is ``consider-using-any-or-all``.

Consider-Using-Any-Or-All checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:consider-using-any-or-all (C0501): *`for` loop could be `%s`*
  A for loop that checks for a condition and return a bool can be replaced with
  any or all.


.. _pylint.extensions.consider_refactoring_into_while_condition:

Consider Refactoring Into While checker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.consider_refactoring_into_while_condition``.
Verbatim name of the checker is ``consider_refactoring_into_while``.

Consider Refactoring Into While checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:consider-refactoring-into-while-condition (R3501): *Consider using 'while %s' instead of 'while %s:' an 'if', and a 'break'*
  Emitted when `while True:` loop is used and the first statement is a break
  condition. The ``if / break`` construct can be removed if the check is
  inverted and moved to the ``while`` statement.


.. _pylint.extensions.consider_ternary_expression:

Consider Ternary Expression checker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.consider_ternary_expression``.
Verbatim name of the checker is ``consider_ternary_expression``.

Consider Ternary Expression checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:consider-ternary-expression (W0160): *Consider rewriting as a ternary expression*
  Multiple assign statements spread across if/else blocks can be rewritten with
  a single assignment and ternary expression


.. _pylint.extensions.bad_builtin:

Deprecated Builtins checker
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.bad_builtin``.
Verbatim name of the checker is ``deprecated_builtins``.

Deprecated Builtins checker Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This used to be the ``bad-builtin`` core checker, but it was moved to
an extension instead. It can be used for finding prohibited used builtins,
such as ``map`` or ``filter``, for which other alternatives exists.

If you want to control for what builtins the checker should warn about,
you can use the ``bad-functions`` option::

    $ pylint a.py --load-plugins=pylint.extensions.bad_builtin --bad-functions=apply,reduce
    ...

See also :ref:`deprecated_builtins checker's options' documentation <deprecated_builtins-options>`

Deprecated Builtins checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:bad-builtin (W0141): *Used builtin function %s*
  Used when a disallowed builtin function is used (see the bad-function
  option). Usual disallowed functions are the ones like map, or filter , where
  Python offers now some cleaner alternative like list comprehension.


.. _pylint.extensions.mccabe:

Design checker
~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.mccabe``.
Verbatim name of the checker is ``design``.

Design checker Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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

See also :ref:`design checker's options' documentation <design-options>`

Design checker Messages
^^^^^^^^^^^^^^^^^^^^^^^
:too-complex (R1260): *%s is too complex. The McCabe rating is %d*
  Used when a method or function is too complex based on McCabe Complexity
  Cyclomatic


.. _pylint.extensions.dict_init_mutate:

Dict-Init-Mutate checker
~~~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.dict_init_mutate``.
Verbatim name of the checker is ``dict-init-mutate``.

Dict-Init-Mutate checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:dict-init-mutate (C3401): *Declare all known key/values when initializing the dictionary.*
  Dictionaries can be initialized with a single statement using dictionary
  literal syntax.


.. _pylint.extensions.docstyle:

Docstyle checker
~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.docstyle``.
Verbatim name of the checker is ``docstyle``.

Docstyle checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^
:bad-docstring-quotes (C0198): *Bad docstring quotes in %s, expected """, given %s*
  Used when a docstring does not have triple double quotes.
:docstring-first-line-empty (C0199): *First line empty in %s docstring*
  Used when a blank line is found at the beginning of a docstring.


.. _pylint.extensions.dunder:

Dunder checker
~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.dunder``.
Verbatim name of the checker is ``dunder``.

See also :ref:`dunder checker's options' documentation <dunder-options>`

Dunder checker Messages
^^^^^^^^^^^^^^^^^^^^^^^
:bad-dunder-name (W3201): *Bad or misspelled dunder method name %s.*
  Used when a dunder method is misspelled or defined with a name not within the
  predefined list of dunder names.


.. _pylint.extensions.check_elif:

Else If Used checker
~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.check_elif``.
Verbatim name of the checker is ``else_if_used``.

Else If Used checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:else-if-used (R5501): *Consider using "elif" instead of "else" then "if" to remove one indentation level*
  Used when an else statement is immediately followed by an if statement and
  does not contain statements that would be unrelated to it.


.. _pylint.extensions.empty_comment:

Empty-Comment checker
~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.empty_comment``.
Verbatim name of the checker is ``empty-comment``.

Empty-Comment checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:empty-comment (R2044): *Line with empty comment*
  Used when a # symbol appears on a line not followed by an actual comment


.. _pylint.extensions.eq_without_hash:

Eq-Without-Hash checker
~~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.eq_without_hash``.
Verbatim name of the checker is ``eq-without-hash``.

Eq-Without-Hash checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:eq-without-hash (W1641): *Implementing __eq__ without also implementing __hash__*
  Used when a class implements __eq__ but not __hash__. Objects get None as
  their default __hash__ implementation if they also implement __eq__.


.. _pylint.extensions.private_import:

Import-Private-Name checker
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.private_import``.
Verbatim name of the checker is ``import-private-name``.

Import-Private-Name checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:import-private-name (C2701): *Imported private %s (%s)*
  Used when a private module or object prefixed with _ is imported. PEP8
  guidance on Naming Conventions states that public attributes with leading
  underscores should be considered private.


.. _pylint.extensions.magic_value:

Magic-Value checker
~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.magic_value``.
Verbatim name of the checker is ``magic-value``.

See also :ref:`magic-value checker's options' documentation <magic-value-options>`

Magic-Value checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:magic-value-comparison (R2004): *Consider using a named constant or an enum instead of '%s'.*
  Using named constants instead of magic values helps improve readability and
  maintainability of your code, try to avoid them in comparisons.


.. _pylint.extensions.redefined_variable_type:

Multiple Types checker
~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.redefined_variable_type``.
Verbatim name of the checker is ``multiple_types``.

Multiple Types checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:redefined-variable-type (R0204): *Redefinition of %s type from %s to %s*
  Used when the type of a variable changes inside a method or a function.


.. _pylint.extensions.no_self_use:

No Self Use checker
~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.no_self_use``.
Verbatim name of the checker is ``no_self_use``.

No Self Use checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:no-self-use (R6301): *Method could be a function*
  Used when a method doesn't use its bound instance, and so could be written as
  a function.


.. _pylint.extensions.overlapping_exceptions:

Overlap-Except checker
~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.overlapping_exceptions``.
Verbatim name of the checker is ``overlap-except``.

Overlap-Except checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:overlapping-except (W0714): *Overlapping exceptions (%s)*
  Used when exceptions in handler overlap or are identical


.. _pylint.extensions.docparams:

Parameter Documentation checker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.docparams``.
Verbatim name of the checker is ``parameter_documentation``.

Parameter Documentation checker Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you document the parameters of your functions, methods and constructors and
their types systematically in your code this optional component might
be useful for you. Sphinx style, Google style, and Numpy style are supported.
(For some examples, see https://pypi.org/project/sphinxcontrib-napoleon/ .)

You can activate this checker by adding the line::

    load-plugins=pylint.extensions.docparams

to the ``MAIN`` section of your ``.pylintrc``.

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
**Note:** by default docstrings of private and magic methods are not checked.
To change this behaviour (for example, to also check ``__init__``) add
``no-docstring-rgx=^(?!__init__$)_`` to the ``BASIC`` section of your ``.pylintrc``.

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

See also :ref:`parameter_documentation checker's options' documentation <parameter_documentation-options>`

Parameter Documentation checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:differing-param-doc (W9017): *"%s" differing in parameter documentation*
  Please check parameter names in declarations.
:differing-type-doc (W9018): *"%s" differing in parameter type documentation*
  Please check parameter names in type declarations.
:multiple-constructor-doc (W9005): *"%s" has constructor parameters documented in class and __init__*
  Please remove parameter declarations in the class or constructor.
:missing-param-doc (W9015): *"%s" missing in parameter documentation*
  Please add parameter declarations for all parameters.
:missing-type-doc (W9016): *"%s" missing in parameter type documentation*
  Please add parameter type declarations for all parameters.
:missing-raises-doc (W9006): *"%s" not documented as being raised*
  Please document exceptions for all raised exception types.
:useless-param-doc (W9019): *"%s" useless ignored parameter documentation*
  Please remove the ignored parameter documentation.
:useless-type-doc (W9020): *"%s" useless ignored parameter type documentation*
  Please remove the ignored parameter type documentation.
:missing-any-param-doc (W9021): *Missing any documentation in "%s"*
  Please add parameter and/or type documentation.
:missing-return-doc (W9011): *Missing return documentation*
  Please add documentation about what this method returns.
:missing-return-type-doc (W9012): *Missing return type documentation*
  Please document the type returned by this method.
:missing-yield-doc (W9013): *Missing yield documentation*
  Please add documentation about what this generator yields.
:missing-yield-type-doc (W9014): *Missing yield type documentation*
  Please document the type yielded by this method.
:redundant-returns-doc (W9008): *Redundant returns documentation*
  Please remove the return/rtype documentation from this method.
:redundant-yields-doc (W9010): *Redundant yields documentation*
  Please remove the yields documentation from this method.


.. _pylint.extensions.redefined_loop_name:

Redefined-Loop-Name checker
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.redefined_loop_name``.
Verbatim name of the checker is ``redefined-loop-name``.

Redefined-Loop-Name checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:redefined-loop-name (W2901): *Redefining %r from loop (line %s)*
  Used when a loop variable is overwritten in the loop body.


.. _pylint.extensions.set_membership:

Set Membership checker
~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.set_membership``.
Verbatim name of the checker is ``set_membership``.

Set Membership checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:use-set-for-membership (R6201): *Consider using set for membership test*
  Membership tests are more efficient when performed on a lookup optimized
  datatype like ``sets``.


.. _pylint.extensions.typing:

Typing checker
~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.typing``.
Verbatim name of the checker is ``typing``.

Typing checker Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Find issue specifically related to type annotations.

See also :ref:`typing checker's options' documentation <typing-options>`

Typing checker Messages
^^^^^^^^^^^^^^^^^^^^^^^
:broken-noreturn (E6004): *'NoReturn' inside compound types is broken in 3.7.0 / 3.7.1*
  ``typing.NoReturn`` inside compound types is broken in Python 3.7.0 and
  3.7.1. If not dependent on runtime introspection, use string annotation
  instead. E.g. ``Callable[..., 'NoReturn']``.
  https://bugs.python.org/issue34921
:broken-collections-callable (E6005): *'collections.abc.Callable' inside Optional and Union is broken in 3.9.0 / 3.9.1 (use 'typing.Callable' instead)*
  ``collections.abc.Callable`` inside Optional and Union is broken in Python
  3.9.0 and 3.9.1. Use ``typing.Callable`` for these cases instead.
  https://bugs.python.org/issue42965
:deprecated-typing-alias (W6001): *'%s' is deprecated, use '%s' instead*
  Emitted when a deprecated typing alias is used.
:consider-using-alias (R6002): *'%s' will be deprecated with PY39, consider using '%s' instead%s*
  Only emitted if 'runtime-typing=no' and a deprecated typing alias is used in
  a type annotation context in Python 3.7 or 3.8.
:consider-alternative-union-syntax (R6003): *Consider using alternative union syntax instead of '%s'%s*
  Emitted when ``typing.Union`` or ``typing.Optional`` is used instead of the
  shorthand union syntax. For example, ``Union[int, float]`` instead of ``int |
  float``. Using the shorthand for unions aligns with Python typing
  recommendations, removes the need for imports, and avoids confusion in
  function signatures.
:unnecessary-default-type-args (R6007): *Type `%s` has unnecessary default type args. Change it to `%s`.*
  Emitted when types have default type args which can be omitted. Mainly used
  for `typing.Generator` and `typing.AsyncGenerator`.
:redundant-typehint-argument (R6006): *Type `%s` is used more than once in union type annotation. Remove redundant typehints.*
  Duplicated type arguments will be skipped by `mypy` tool, therefore should be
  removed to avoid confusion.


.. _pylint.extensions.while_used:

While Used checker
~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.while_used``.
Verbatim name of the checker is ``while_used``.

While Used checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^
:while-used (W0149): *Used `while` loop*
  Unbounded `while` loops can often be rewritten as bounded `for` loops.
  Exceptions can be made for cases such as event loops, listeners, etc.
