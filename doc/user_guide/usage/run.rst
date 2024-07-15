================
 Running Pylint
================

On module packages or directories
---------------------------------

Pylint is meant to be called from the command line. The usage is ::

   pylint [options] modules_or_packages

By default the ``pylint`` command only accepts a list of python modules and packages.
On versions below 2.15, specifying a directory that is not an explicit package
(with ``__init__.py``) results in an error::

    pylint mydir
    ************* Module mydir
    mydir/__init__.py:1:0: F0010: error while code parsing: Unable to load file mydir/__init__.py:
    [Errno 2] No such file or directory: 'mydir/__init__.py' (parse-error)

Thus, on versions before 2.15 using the ``--recursive=y`` option allows for linting a namespace package::

    pylint --recursive=y mydir mymodule mypackage

This option makes ``pylint`` attempt to discover all modules (files ending with ``.py`` extension)
and all explicit packages (all directories containing a ``__init__.py`` file).

Pylint **will not import** this package or module, but it does use Python internals
to locate them and as such is subject to the same rules and configuration.
You should pay attention to your ``PYTHONPATH``, since it is a common error
to analyze an installed version of a module instead of the development version.

On files
--------

It is also possible to analyze Python files, with a few restrictions. As a convenience,
you can give it a file name if it's possible to guess a module name from the file's
path using the python path. Some examples:

``pylint mymodule.py`` should always work since the current working
directory is automatically added on top of the python path

``pylint directory/mymodule.py`` will work if: ``directory`` is a python
package (i.e. has an ``__init__.py`` file), an implicit namespace package
or if ``directory`` is in the python path.

With implicit namespace packages
--------------------------------

If the analyzed sources use implicit namespace packages (PEP 420), the source root(s) should
be specified using the ``--source-roots`` option. Otherwise, the package names are
detected incorrectly, since implicit namespace packages don't contain an ``__init__.py``.

Globbing support
----------------

It is also possible to specify both directories and files using globbing patterns::

   pylint [options] packages/*/src

Command line options
--------------------

.. _run_command_line:

First of all, we have two basic (but useful) options.

--version             show program's version number and exit
-h, --help            show help about the command line options

Pylint is architected around several checkers. You can disable a specific
checker or some of its messages or message categories by specifying
``--disable=<symbol>``. If you want to enable only some checkers or some
message symbols, first use ``--disable=all`` then
``--enable=<symbol>`` with ``<symbol>`` being a comma-separated list of checker
names and message symbols. See the list of available features for a
description of provided checkers with their functionalities.
The ``--disable`` and ``--enable`` options can be used with comma-separated lists
mixing checkers, message ids and categories like ``-d C,W,no-error,design``

It is possible to disable all messages with ``--disable=all``. This is
useful to enable only a few checkers or a few messages by first
disabling everything, and then re-enabling only what you need.

Each checker has some specific options, which can take either a yes/no
value, an integer, a python regular expression, or a comma-separated
list of values (which are generally used to override a regular
expression in special cases). For a full list of options, use ``--help``

Specifying all the options suitable for your setup and coding
standards can be tedious, so it is possible to use a configuration file to
specify the default values.  You can specify a configuration file on the
command line using the ``--rcfile`` option.  Otherwise, Pylint searches for a
configuration file in the following order and uses the first one it finds:

#. ``pylintrc`` in the current working directory
#. ``pylintrc.toml`` in the current working directory,
   providing it has at least one ``tool.pylint.`` section.
#. ``.pylintrc`` in the current working directory
#. ``.pylintrc.toml`` in the current working directory,
   providing it has at least one ``tool.pylint.`` section.
#. ``pyproject.toml`` in the current working directory,
   providing it has at least one ``tool.pylint.`` section.
   The ``pyproject.toml`` must prepend section names with ``tool.pylint.``,
   for example ``[tool.pylint.'MESSAGES CONTROL']``. They can also be passed
   in on the command line.
#. ``setup.cfg`` in the current working directory,
   providing it has at least one ``pylint.`` section
#. ``tox.ini`` in the current working directory,
   providing it has at least one ``pylint.`` section
#. Pylint will search for the ``pyproject.toml`` file up the directories hierarchy
   unless it's found, or a ``.git``/``.hg`` directory is found, or the file system root
   is approached.
#. If the current working directory is in a Python package, Pylint searches \
   up the hierarchy of Python packages until it finds a ``pylintrc`` file. \
   This allows you to specify coding standards on a module-by-module \
   basis.  Of course, a directory is judged to be a Python package if it \
   contains an ``__init__.py`` file.
#. The file named by environment variable ``PYLINTRC``
#. if you have a home directory which isn't ``/root``:

   #. ``.pylintrc`` in your home directory
   #. ``.config/pylintrc`` in your home directory

#. ``/etc/pylintrc``

The ``--generate-toml-config`` option will generate a commented configuration file
on standard output according to the current configuration and exit. This
includes:

* Any configuration file found as explained above
* Options appearing before ``--generate-toml-config`` on the Pylint command line

Of course you can also start with the default values and hand-tune the
configuration.

Other useful global options include:

--ignore=<file[,file...]>  Files or directories to be skipped. They should be
                           base names, not paths.
--output-format=<format>   Select output format (text, json, custom).
--msg-template=<template>  Modify text output message template.
--list-msgs                Generate pylint's messages.
--list-msgs-enabled        Display a list of what messages are enabled and
                           disabled with the given configuration.
--full-documentation       Generate pylint's full documentation, in reST
                             format.

Parallel execution
------------------

It is possible to speed up the execution of Pylint. If the running computer
has more CPUs than one, then the work for checking all files could be spread across all
cores via Pylints's sub-processes.

This functionality is exposed via the ``-j`` command-line parameter.
If the provided number is 0, then the total number of CPUs will be autodetected and used.

Example::

  pylint -j 4 mymodule1.py mymodule2.py mymodule3.py mymodule4.py

This will spawn 4 parallel Pylint sub-process, where each provided module will
be checked in parallel. Discovered problems by checkers are not displayed
immediately. They are shown just after checking a module is complete.

You can also do your own parallelization by launching pylint multiple times on subsets
of your files (like ``pre-commit`` with the default ``require_serial=false`` does).
Be aware, though: pylint should analyse all your code at once in order to best infer
the actual values that result from calls. If only some of the files are given, pylint
might miss a particular value's type and produce inferior inference for the subset.
It can also be unexpectedly different when the file set changes because the new
slicing can change the inference. So, don't do this if correctness and determinism
are important to you.

Exit codes
----------

Pylint returns bit-encoded exit codes.

=========  =========================
exit code  meaning
=========  =========================
0          no error
1          fatal message issued
2          error message issued
4          warning message issued
8          refactor message issued
16         convention message issued
32         usage error
=========  =========================

For example, an exit code of ``20`` means there was at least one warning message (4)
and at least one convention message (16) and nothing else.
