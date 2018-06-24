================
 Running Pylint
================

Invoking Pylint
---------------

Pylint is meant to be called from the command line. The usage is ::

   pylint [options] modules_or_packages

You should give Pylint the name of a python package or module, or some number
of packages or modules. Pylint
``will not import`` this package or module, though uses Python internals
to locate them and as such is subject to the same rules and configuration.
You should pay attention to your ``PYTHONPATH``, since it is a common error
to analyze an installed version of a module instead of the
development version.

It is also possible to analyze python files, with a few
restrictions. The thing to keep in mind is that Pylint will try to
convert the file name to a module name, and only be able to process
the file if it succeeds.  ::

  pylint mymodule.py

should always work since the current working
directory is automatically added on top of the python path ::

  pylint directory/mymodule.py

will work if ``directory`` is a python package (i.e. has an __init__.py
file or it is an implicit namespace package) or if "directory" is in the
python path.

For more details on this see the :ref:`faq`.

It is also possible to call Pylint from another python program,
thanks to ``Run()`` function in ``pylint.lint`` module,
assuming Pylint options are stored in a list of strings ``pylint_options``, as:

.. sourcecode:: python

  import pylint.lint
  pylint_opts = ['--version']
  pylint.lint.Run(pylint_opts)

To silently run Pylint on a ``module_name.py`` module,
and get its standard output and error:

.. sourcecode:: python

  from pylint import epylint as lint
  (pylint_stdout, pylint_stderr) = lint.py_run('module_name.py', return_std=True)


Command line options
--------------------

First of all, we have two basic (but useful) options.

--version             show program's version number and exit
-h, --help            show help about the command line options

Pylint is architectured around several checkers. you can disable a specific
checker or some of its messages or messages categories by specifying
``--disable=<symbol>``. If you want to enable only some checkers or some
message symbols, first use ``--disable=all`` then
``--enable=<symbol>`` with <symbol> being a comma separated list of checker
names and message symbols. See the list of available features for a
description of provided checkers with their functionalities.
The ``--disable`` and ``--enable`` options can be used with comma separated lists
mixing checkers, message ids and categories like ``-d C,W,no-error,design``

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
#. ``.pylintrc`` in the current working directory
#. If the current working directory is in a Python module, Pylint searches \
   up the hierarchy of Python modules until it finds a ``pylintrc`` file. \
   This allows you to specify coding standards on a module-by-module \
   basis.  Of course, a directory is judged to be a Python module if it \
   contains an ``__init__.py`` file.
#. The file named by environment variable ``PYLINTRC``
#. if you have a home directory which isn't ``/root``:

   #. ``.pylintrc`` in your home directory
   #. ``.config/pylintrc`` in your home directory

#. ``/etc/pylintrc``

The ``--generate-rcfile`` option will generate a commented configuration file
on standard output according to the current configuration and exit. This
includes:

* Any configuration file found as explained above
* Options appearing before ``--generate-rcfile`` on the Pylint command line

Of course you can also start with the default values and hand tune the
configuration.

Other useful global options include:

--ignore=<file[,file...]>  Add files or directories to the blacklist. They
                           should be base names, not paths.
--output-format=<format>   Select output format (text, json, custom).
--msg-template=<template>  Modify text output message template.
--list-msgs                Generate pylint's messages.
--full-documentation       Generate pylint's full documentation, in reST
                             format.

Parallel execution
------------------

It is possible to speed up the execution of Pylint. If the running computer
has more CPUs than one, then the files for checking could be spread on all
cores via Pylints's sub-processes.
This functionality is exposed via ``-j`` command line parameter.
If the provided number is 0, then the total number of CPUs will be used.

Example::

  pylint -j 4 mymodule1.py mymodule2.py mymodule3.py mymodule4.py

This will spawn 4 parallel Pylint sub-process, where each provided module will
be checked in parallel. Discovered problems by checkers are not displayed
immediately. They are shown just after completing checking a module.

There are some limitations in running checks in parallel in current
implementation. It is not possible to use custom plugins
(i.e. ``--load-plugins`` option), nor it is not possible to use
initialization hooks (i.e. ``--init-hook`` option).

This will spawn 4 parallel Pylint subprocesses, each provided module being checked
by one or another subprocess.


Exit codes
----------

Pylint returns bit-encoded exit codes. If applicable the table lists related
stderr stream message output.

=========  =========================  ==========================================
exit code  meaning                    stderr stream message
=========  =========================  ==========================================
0          no error
1          fatal message issued
2          error message issued
4          warning message issued
8          refactor message issued
16         convention message issued
32         usage error                - "internal error while receiving results\
                                        from child linter" "Error occurred,
                                        stopping the linter."
                                      - "<return of linter.help()>"
                                      - "Jobs number <#> should be greater \
                                        than 0"
=========  =========================  ==========================================
