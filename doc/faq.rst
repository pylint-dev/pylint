.. -*- coding: utf-8 -*-

.. _faq:

==========================
Frequently Asked Questions
==========================

How do I install Pylint?
------------------------

Everything should be explained on :ref:`installation`.

What kind of versioning system does Pylint use?
-----------------------------------------------

Pylint uses git. To get the latest version of Pylint from the repository, simply invoke ::

    git clone https://github.com/PyCQA/pylint

.. _git: https://git-scm.com/


3. Running Pylint
=================

3.1 Can I give pylint a file as an argument instead of a module?
----------------------------------------------------------------

Pylint expects the name of a package or module as its argument. As a
convenience, you can give it a file name if it's possible to guess a module name from
the file's path using the python path. Some examples:

"pylint mymodule.py" should always work since the current working
directory is automatically added on top of the python path

"pylint directory/mymodule.py" will work if "directory" is a python
package (i.e. has an __init__.py file), an implicit namespace package
or if "directory" is in the python path.

"pylint /whatever/directory/mymodule.py" will work if either:

    - "/whatever/directory" is in the python path

    - your cwd is "/whatever/directory"

    - "directory" is a python package and "/whatever" is in the python
          path

        - "directory" is an implicit namespace package and is in the python path.

    - "directory" is a python package and your cwd is "/whatever" and so
          on...

3.2 Where is the persistent data stored to compare between successive runs?
---------------------------------------------------------------------------

Analysis data are stored as a pickle file in a directory which is
localized using the following rules:

* value of the PYLINTHOME environment variable if set

* "pylint" subdirectory of the user's XDG_CACHE_HOME if the environment variable is set, otherwise

        - Linux: "~/.cache/pylint"

        - Mac OS X: "~/Library/Caches/pylint"

        - Windows: "C:\Users\<username>\AppData\Local\pylint"

* ".pylint.d" directory in the current directory


3.3 How do I find the option name corresponding to a specific command line option?
----------------------------------------------------------------------------------

You can generate a sample configuration file with ``--generate-toml-config``.
Every option present on the command line before this will be included in
the toml file

For example::

    pylint --disable=bare-except,invalid-name --class-rgx='[A-Z][a-z]+' --generate-toml-config

3.5 I need to run pylint over all modules and packages in my project directory.
-------------------------------------------------------------------------------

By default the ``pylint`` command only accepts a list of python modules and packages. Using a
directory which is not a package results in an error::

    pylint mydir
    ************* Module mydir
    mydir/__init__.py:1:0: F0010: error while code parsing: Unable to load file mydir/__init__.py:
    [Errno 2] No such file or directory: 'mydir/__init__.py' (parse-error)

To execute pylint over all modules and packages under the directory, the ``--recursive=y`` option must
be provided. This option makes ``pylint`` attempt to discover all modules (files ending with ``.py`` extension)
and all packages (all directories containing a ``__init__.py`` file).
Those modules and packages are then analyzed::

    pylint --recursive=y mydir

When ``--recursive=y`` option is used, modules and packages are also accepted as parameters::

    pylint --recursive=y mydir mymodule mypackage

4. Message Control
==================

4.1 How to disable a particular message?
----------------------------------------

For just a single line, add ``#pylint: disable=some-message,another-one`` at the end of
the desired line of code. Since Pylint 2.10 you can also use ``#pylint: disable-next=...``
on the line just above the problem. ``...`` in the following example is short for the
list of messages you want to disable.

For larger amounts of code, you can add ``#pylint: disable=...`` at the block level
to disable messages for the entire block. It's possible to re-enable a message for the
remainder of the block with ``#pylint: enable=...``. A block is either a scope (say a
function, a module) or a multiline statement (try, finally, if statements, for loops).
Note: It's currently impossible to `disable inside an else block`_.

Read :ref:`message-control` for details and examples.

.. _`disable inside an else block`: https://github.com/PyCQA/pylint/issues/872

4.2 Is there a way to disable a message for a particular module only?
---------------------------------------------------------------------

Yes, you can disable or enable (globally disabled) messages at the
module level by adding the corresponding option in a comment at the
top of the file: ::

    # pylint: disable=wildcard-import, method-hidden
    # pylint: enable=too-many-lines

4.3 How can I tell Pylint to never check a given module?
--------------------------------------------------------

Add ``#pylint: skip-file`` at the beginning of the module.

In order to ease finding which modules are ignored an Information-level message
`file-ignored` is emitted.

4.4 Do I have to remember all these numbers?
--------------------------------------------

No, you can use symbolic names for messages::

    # pylint: disable=fixme, line-too-long


4.5 I have a callback function where I have no control over received arguments. How do I avoid getting unused argument warnings?
--------------------------------------------------------------------------------------------------------------------------------

Prefix (ui) the callback's name by `cb_`, as in cb_onclick(...). By
doing so arguments usage won't be checked. Another solution is to
use one of the names defined in the "dummy-variables" configuration
variable for unused argument ("_" and "dummy" by default).

4.6 What is the format of the configuration file?
-------------------------------------------------

Pylint uses ConfigParser from the standard library to parse the configuration
file.  It means that if you need to disable a lot of messages, you can use
any formatting accepted by ConfigParser, e.g.

.. code-block:: ini

    [MAIN]
    output-format = colorized

    [Messages Control]
    disable=method-hidden,too-many-lines,wildcard-import

.. code-block:: ini

    [Messages Control]
    disable =
        method-hidden
        too-many-lines
        wildcard-import

Alternatively, if you use ``pyproject.toml``, e.g.

.. code-block:: toml

    [tool.pylint.main]
    output-format = "colorized"

    [tool.pylint.messages_control]
    disable = [
        "method-hidden",
        "too-many-lines",
        "wildcard-import",
    ]

See also the :ref:`exhaustive list of possible options
<user_guide/configuration/all-options:all pylint options>`.

4.7 Why are there a bunch of messages disabled by default?
----------------------------------------------------------

pylint does have some messages disabled by default, either because
they are prone to false positives or that they are opinionated enough
for not being included as default messages.

You can see the plugin you need to explicitly :ref:`load in the technical reference
<technical_reference/extensions:optional pylint checkers in the extensions module>`.

4.8 I am using another popular linter alongside pylint. Which messages should I disable to avoid duplicates?
------------------------------------------------------------------------------------------------------------

pycodestyle_: unneeded-not, line-too-long, unnecessary-semicolon, trailing-whitespace, missing-final-newline, bad-indentation, multiple-statements, bare-except, wrong-import-position

pyflakes_: undefined-variable, unused-import, unused-variable

mccabe_: too-many-branches

pydocstyle_: missing-module-docstring, missing-class-docstring, missing-function-docstring

pep8-naming_: invalid-name, bad-classmethod-argument, bad-mcs-classmethod-argument, no-self-argument

isort_: wrong-import-order

flake8-import-order_: wrong-import-order

.. _`pycodestyle`: https://github.com/PyCQA/pycodestyle
.. _`pyflakes`: https://github.com/PyCQA/pyflakes
.. _`mccabe`: https://github.com/PyCQA/mccabe
.. _`pydocstyle`: https://github.com/PyCQA/pydocstyle
.. _`pep8-naming`: https://github.com/PyCQA/pep8-naming
.. _`isort`: https://github.com/pycqa/isort
.. _`flake8-import-order`: https://github.com/PyCQA/flake8-import-order


5. Classes and Inheritance
==========================

5.1 When is Pylint considering a class as an abstract class?
------------------------------------------------------------

A class is considered as an abstract class if at least one of its
methods is doing nothing but raising ``NotImplementedError``.

5.2 How do I avoid "access to undefined member" messages in my mixin classes?
-----------------------------------------------------------------------------

You should add the ``no-member`` message to your ``ignored-checks-for-mixins`` option
and name your mixin class with a name which ends with "Mixin" or "mixin" (default)
or change the default value by changing the ``mixin-class-rgx`` option.


6. Troubleshooting
==================

6.1 Pylint gave my code a negative rating out of ten. That can't be right!
--------------------------------------------------------------------------

Prior to Pylint 2.13.0, the score formula used by default had no lower
bound. The new default score formula is ::

    max(0, 0 if fatal else 10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10))

If your project contains a configuration file created by an earlier version of
Pylint, you can set ``evaluation`` to the above expression to get the new
behavior. Likewise, since negative values are still technically supported,
``evaluation`` can be set to a version of the above expression that does not
enforce a floor of zero.
