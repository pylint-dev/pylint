.. -*- coding: utf-8 -*-

=======
Plugins
=======

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


Why write a plugin?
-------------------

Pylint is a static analysis tool and Python is a dynamically typed language.
So there will be cases where Pylint cannot analyze files properly (this problem
can happen in statically typed languages also if reflection or dynamic
evaluation is used). Plugin is a way to tell Pylint how to handle such cases,
since only the user would know what needs to be done.

Example
-------

Let us run Pylint on a module from the Python source: `warnings.py`_ and see what happens:

.. sourcecode:: bash

  amitdev$ pylint -E Lib/warnings.py
  E:297,36: Instance of 'WarningMessage' has no 'message' member (no-member)
  E:298,36: Instance of 'WarningMessage' has no 'filename' member (no-member)
  E:298,51: Instance of 'WarningMessage' has no 'lineno' member (no-member)
  E:298,64: Instance of 'WarningMessage' has no 'line' member (no-member)


Did we catch a genuine error? Let's open the code and look at ``WarningMessage`` class:

.. sourcecode:: python

  class WarningMessage(object):

    """Holds the result of a single showwarning() call."""

    _WARNING_DETAILS = ("message", "category", "filename", "lineno", "file",
                        "line")

    def __init__(self, message, category, filename, lineno, file=None,
                    line=None):
      local_values = locals()
      for attr in self._WARNING_DETAILS:
        setattr(self, attr, local_values[attr])
      self._category_name = category.__name__ if category else None

    def __str__(self):
      ...

Ah, the fields (``message``, ``category`` etc) are not defined statically on the class.
Instead they are added using ``setattr``. Pylint would have a tough time figuring
this out.

Enter Plugin
------------

We can write a plugin to tell Pylint about how to analyze this properly. A
plugin is a module which should have a function ``register`` and takes the
`lint`_ module as input. So a basic hello-world plugin can be implemented as:

.. sourcecode:: python

  # Inside hello_plugin.py
  def register(linter):
    print 'Hello world'

We can run this plugin by placing this module in the PYTHONPATH and invoking as:

.. sourcecode:: bash

  amitdev$ pylint -E --load-plugins hello_plugin foo.py
  Hello world

Back to our example: one way to fix that would be to transform the ``WarningMessage`` class
and set the attributes using a plugin so that Pylint can see them. This can be done by
registering a transform function. We can transform any node in the parsed AST like
Module, Class, Function etc. In our case we need to transform a class. It can be done so:

.. sourcecode:: python

  from astroid import MANAGER
  from astroid import scoped_nodes

  def register(linter):
    pass

  def transform(cls):
    if cls.name == 'WarningMessage':
      import warnings
      for f in warnings.WarningMessage._WARNING_DETAILS:
        cls.locals[f] = [scoped_nodes.Class(f, None)]

  MANAGER.register_transform(scoped_nodes.Class, transform)

Let's go through the plugin. First, we need to register a class transform, which
is done via the ``register_transform`` function in ``MANAGER``. It takes the node
type and function as parameters. We need to change a class, so we use ``scoped_nodes.Class``.
We also pass a ``transform`` function which does the actual transformation.

``transform`` function is simple as well. If the class is ``WarningMessage`` then we
add the attributes to its locals (we are not bothered about type of attributes, so setting
them as class will do. But we could set them to any type we want). That's it.

Note: We don't need to do anything in the ``register`` function of the plugin since we
are not modifying anything in the linter itself.

Lets run Pylint with this plugin and see:

.. sourcecode:: bash

  amitdev$ pylint -E --load-plugins warning_plugin Lib/warnings.py
  amitdev$

All the false positives associated with ``WarningMessage`` are now gone. This is just
an example, any code transformation can be done by plugins. See `nodes`_ and `scoped_nodes`_
for details about all node types that can be transformed.

.. _`warnings.py`: http://hg.python.org/cpython/file/2.7/Lib/warnings.py
.. _`scoped_nodes`: https://bitbucket.org/logilab/astroid/src/64026ffc0d94fe09e4bdc2bf5efaab29444645e7/scoped_nodes.py?at=default
.. _`nodes`: https://bitbucket.org/logilab/astroid/src/64026ffc0d94fe09e4bdc2bf5efaab29444645e7/nodes.py?at=default
.. _`lint`: https://bitbucket.org/logilab/pylint/src/f2acea7b640def0237513f66e3de5fa3de73f2de/lint.py?at=default