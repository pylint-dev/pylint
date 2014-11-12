
Extending Pylint
================

Writing your own checker
------------------------
You can find some simple examples in the examples
directory of the distribution (custom.py and custom_raw.py). I'll try to
quickly explain the essentials here.

First, there are two kinds of checkers:

* raw checkers, which are analysing each module as a raw file stream
* ast checkers, which are working on an ast representation of the module

The ast representation used is an extension of the one provided with the
standard Python distribution in the `ast package`_. The extension
adds additional information and methods on the tree nodes to ease
navigation and code introspection.

An AST checker is a visitor, and should implement
`visit_<lowered class name>` or `leave_<lowered class name>`
methods for the nodes it's interested in. To get description of the different
classes used in an ast tree, look at the `ast package`_ documentation.
Checkers are ordered by priority. For each module, Pylint's engine:

1. give the module source file as a stream to raw checkers
2. get an ast representation for the module
3. make a depth first descent of the tree, calling ``visit_<>`` on each AST
   checker when entering a node, and ``leave_<>`` on the back traversal

Notice that the source code is probably the best source of
documentation, it should be clear and well documented. Don't hesitate to
ask for any information on the code-quality mailing list.

.. _`ast package`: http://docs.python.org/2/library/ast
