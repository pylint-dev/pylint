
Transform plugins
^^^^^^^^^^^^^^^^^

Why write a plugin?
-------------------

Pylint is a static analysis tool and Python is a dynamically typed language.
So there will be cases where Pylint cannot analyze files properly (this problem
can happen in statically typed languages also if reflection or dynamic
evaluation is used).

The plugins are a way to tell Pylint how to handle such cases,
since only the user would know what needs to be done. They are usually operating
on the AST level, by modifying or changing it in a way which can ease its
understanding by Pylint.

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

We can write a transform plugin to tell Pylint how to analyze this properly.

One way to fix our example with a plugin would be to transform the ``WarningMessage`` class,
by setting the attributes so that Pylint can see them. This can be done by
registering a transform function. We can transform any node in the parsed AST like
Module, Class, Function etc. In our case we need to transform a class. It can be done so:

.. sourcecode:: python

  import astroid
  from astroid import MANAGER

  def register(linter):
    # Needed for registering the plugin.
    pass

  def transform(cls):
    if cls.name == 'WarningMessage':
      import warnings
      for f in warnings.WarningMessage._WARNING_DETAILS:
        cls.locals[f] = [astroid.Class(f, None)]

  MANAGER.register_transform(astroid.Class, transform)

Let's go through the plugin. First, we need to register a class transform, which
is done via the ``register_transform`` function in ``MANAGER``. It takes the node
type and function as parameters. We need to change a class, so we use ``astroid.Class``.
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
an example, any code transformation can be done by plugins. 

See `astroid/brain`_ for real life examples of transform plugins.

.. _`warnings.py`: http://hg.python.org/cpython/file/2.7/Lib/warnings.py
.. _`astroid/brain`: https://github.com/PyCQA/astroid/tree/master/astroid/brain
