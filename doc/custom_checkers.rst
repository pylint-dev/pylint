Custom checkers
^^^^^^^^^^^^^^^

Writing your own checker
------------------------
You can find some simple examples in the examples
directory of the distribution (custom.py and custom_raw.py).

First, there are two kinds of checkers:

* raw checkers, which are analysing each module as a raw file stream
* AST checkers, which are working on an AST representation of the module

The AST representation used is an extension of the one provided with the
standard Python distribution in the `ast package`_. The extension
adds additional information and methods on the tree nodes to ease
navigation and code introspection.

An AST checker is a visitor, and should implement
`visit_<lowered class name>` or `leave_<lowered class name>`
methods for the nodes it's interested in. To get description of the different
classes used in an ast tree, look at the `ast package`_ documentation.
For each module, Pylint's engine is doing the following:

1. give the module source file as a stream to raw checkers
2. get an AST representation for the module
3. make a depth first descent of the tree, calling ``visit_<>`` on each AST
   checker when entering a node, and ``leave_<>`` on the back traversal

A checker is composed from multiple components, which needs to be given
in order for it to work properly:

1. a name. The name is internally for a couple of things, one of them
   being used for generating a special configuration
   section of the checker, in case in has provided options.

2. a priority that needs to be lower than 0. The checkers are ordered by
   the priority, from the most negative to the most positive.

3. a message dictionary. Each checker is being used for finding problems
   in your code, the problems being displayed to the user through **messages**.
   The message dictionary should specify what messages the said checker is
   going to emit. It has the following format::

       msgs = {'message-id': ('displayed-message', 'message-symbol', 'message-help')}

   The ``message id`` should be a 5-digits number, prefixed with a **message category**.
   There are multiple message categories, these being ``C``, ``W``, ``E``, ``F``, ``R``,
   standing for ``Convention``, ``Warning``, ``Error``, ``Fatal`` and ``Refactoring``.
   The rest of the 5 digits should not conflict with existing checkers and they should
   be consistent across the checker. For instance, the first two digits should not be
   different across the checker.

   The displayed message is used for displaying the message to the user, once it is emitted.
   The message symbol is an alias of the message id and it can be used wherever the message id
   can be used. The message help is used when calling ``pylint --help-msg``.

4. An options list (optional)


.. _`ast package`: http://docs.python.org/2/library/ast
