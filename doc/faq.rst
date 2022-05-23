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

3.1 Where is the persistent data stored to compare between successive runs?
---------------------------------------------------------------------------

Analysis data are stored as a pickle file in a directory which is
localized using the following rules:

* value of the PYLINTHOME environment variable if set

* "pylint" subdirectory of the user's XDG_CACHE_HOME if the environment variable is set, otherwise

        - Linux: "~/.cache/pylint"

        - Mac OS X: "~/Library/Caches/pylint"

        - Windows: "C:\Users\<username>\AppData\Local\pylint"

* ".pylint.d" directory in the current directory


3.2 How do I find the option name corresponding to a specific command line option?
----------------------------------------------------------------------------------

You can generate a sample configuration file with ``--generate-toml-config``.
Every option present on the command line before this will be included in
the toml file

For example::

    pylint --disable=bare-except,invalid-name --class-rgx='[A-Z][a-z]+' --generate-toml-config

4. Message Control
==================

4.1 How to disable a particular message in a particular way ?
-------------------------------------------------------------

Check the :ref:`message control documentation<message_control>`.

4.2 Do I have to remember all these numbers?
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
<all-configurations-options>`.

4.7 Why are there a bunch of messages disabled by default?
----------------------------------------------------------

pylint does have some messages disabled by default, either because
they are prone to false positives or that they are opinionated enough
for not being included as default messages.

You can see the plugin you need to explicitly :ref:`load in the technical reference
<user_guide/checkers/extensions:optional checkers>`.

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
