.. -*- coding: utf-8 -*-

How To Write a Pylint Plugin
============================

Pylint provides support for writing two types of extensions.
First, there is the concept of **checkers**,
which can be used for finding problems in your code.
Secondly, there is also the concept of **transform plugin**,
which represents a way through which the inference and
the capabilities of Pylint can be enhanced
and tailored to a particular module, library of framework.

In general, a plugin is a module which should have a function ``register``,
which takes an instance of ``pylint.lint.PyLinter`` as input.

So a basic hello-world plugin can be implemented as:

.. sourcecode:: python

  # Inside hello_plugin.py
  def register(linter):
    print 'Hello world'

We can run this plugin by placing this module in the PYTHONPATH and invoking
**pylint** as:

.. sourcecode:: bash

  $ pylint -E --load-plugins hello_plugin foo.py
  Hello world

Depending if we need a **transform plugin** or a **checker**, this might not
be enough. For the former, this is enough to declare the module as a plugin,
but in the case of the latter, we need to register our checker with the linter
object, by calling the following inside the ``register`` function::

    linter.register_checker(OurChecker(linter))

For more information on writing a checker see :ref:`write_a_checker`.
