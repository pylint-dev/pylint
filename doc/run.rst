================
 Running Pylint
================

Invoking Pylint
---------------

Pylint is meant to be called from the command line. The usage is ::

   pylint [options] module_or_package

You should give Pylint the name of a python package or module. Pylint
will ``import`` this package or module, so you should pay attention to
your ``PYTHONPATH``, since it is a common error to analyze an
installed version of a module instead of the development version.

It is also possible to analyze python files, with a few
restrictions. The thing to keep in mind is that Pylint will try to
convert the file name to a module name, and only be able to process
the file if it succeeds.  ::

  pylint mymodule.py

should always work since the current working
directory is automatically added on top of the python path ::

  pylint directory/mymodule.py

will work if "directory" is a python package (i.e. has an __init__.py
file) or if "directory" is in the python path.

For more details on this see the Frequently Asked Questions.

You can also start a thin gui around Pylint (require TkInter) by
typing ::

  pylint-gui

This should open a window where you can enter the name of the package
or module to check, at Pylint messages will be displayed in the user
interface.

It is also possible to call Pylint from an other python program,
thanks to ``py_run()`` function in ``lint`` module,
assuming Pylint options are stored in ``pylint_options`` string, as:

.. sourcecode:: python

  from pylint import epylint as lint
  lint.py_run(pylint_options)

To silently run Pylint on a ``module_name.py`` module,
and get its standart output and error:

.. sourcecode:: python

  from pylint import epylint as lint
  (pylint_stdout, pylint_stderr) = lint.py_run('module_name.py', True)


Command line options
--------------------

First of all, we have two basic (but useful) options.

--version             show program's version number and exit
-h, --help            show help about the command line options

Pylint is architectured around several checkers. By default all
checkers are enabled. You can disable a specific checker or some of its
messages or messages categories by specifying
``--disable=<id>``. If you want to enable only some checkers or some
message ids, first use ``--disable=all`` then
``--enable=<id>`` with <id> being a comma separated list of checker
names and message identifiers. See the list of available features for a
description of provided checkers with their functionalities.
The ``--disable`` and ``--enable`` options can be used with comma separated lists
mixing checkers, message ids and categories like ``-d C,W,E0611,design``

It is possible to disable all messages with ``--disable=all``. This is
useful to enable only a few checkers or a few messages by first
disabling everything, and then re-enabling only what you need.

Each checker has some specific options, which can take either a yes/no
value, an integer, a python regular expression, or a comma separated
list of values (which are generally used to override a regular
expression in special cases). For a full list of options, use ``--help``

Specifying all the options suitable for your setup and coding
standards can be tedious, so it is possible to use a configuration file to
specify the default values.  You can specify a configuration file on the 
command line using the ``--rcfile`` option.  Otherwise, Pylint searches for a
configuration file in the following order and uses the first one it finds:

#. ``pylintrc`` in the current working directory
#. If the current working directory is in a Python module, Pylint searches \
   up the hierarchy of Python modules until it finds a ``pylintrc`` file. \
   This allows you to specify coding standards on a module-by-module \
   basis.  Of course, a directory is judged to be a Python module if it \
   contains an ``__init__.py`` file.
#. The file named by environment variable ``PYLINTRC``
#. ``.pylintrc`` in your home directory, unless you have no home directory or \
   your home directory is ``/root``
#. ``.pylintrc`` in the current working directory
#. ``/etc/pylintrc``

The ``--generate-rcfile`` option will generate a commented configuration file
on standard output according to the current configuration and exit. This
includes:

* Any configuration file found as explained above
* Options appearing before ``--generate-rcfile`` on the Pylint command line

Of course you can also start with the default values and hand tune the
configuration. 

Other useful global options include:

--ignore=file              Add <file> (may be a directory) to the black
                             list. It should be a base name, not a path.
                             You may set this option multiple times.
--persistent=y_or_n        Pickle collected data for later comparisons.
--output-format=<format>   Select output format (text, html, custom).
--msg-template=<template>  Modifiy text output message template.
--list-msgs                Generate pylint's messages.
--full-documentation       Generate pylint's full documentation, in reST 
                             format.


