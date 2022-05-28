.. _faq:

==========================
Frequently Asked Questions
==========================

How do I install Pylint?
------------------------

.. This is a copy paste of Install in the README do not modify one without modifying the other

For command line use, pylint is installed with::

    pip install pylint

It can also be integrated in most editors or IDEs. More information can be found in
:ref:`the installation guide <installation>`.

How do I contribute to Pylint?
------------------------------

.. This is a copy paste of Contributing in the README do not modify one without modifying the other

We welcome all forms of contributions such as updates for documentation, new code, checking issues for duplicates or telling us
that we can close them, confirming that issues still exist, `creating issues because
you found a bug or want a feature`_, etc. Everything is much appreciated!

Please follow the `code of conduct`_ and check `the Contributor Guides`_ if you want to
make a code contribution.

.. _creating issues because you found a bug or want a feature: https://pylint.pycqa.org/en/latest/contact.html#bug-reports-feedback
.. _code of conduct: https://github.com/PyCQA/pylint/blob/main/CODE_OF_CONDUCT.md
.. _the Contributor Guides: https://pylint.pycqa.org/en/latest/development_guide/contribute.html

Does Pylint follow a versioning scheme?
----------------------------------------

See :ref:`upgrading pylint in the installation guide <upgrading_pylint>`.

How do I find the name corresponding to a specific command line option?
-----------------------------------------------------------------------

You can generate a sample configuration file with ``--generate-toml-config``.
Every option present on the command line before this will be included in
the toml file

For example::

    pylint --disable=bare-except,invalid-name --class-rgx='[A-Z][a-z]+' --generate-toml-config

How to disable a particular message?
------------------------------------

Read :ref:`message-control` for details and examples.

Pylint gave my code a negative rating out of ten. That can't be right!
----------------------------------------------------------------------

Prior to Pylint 2.13.0, the score formula used by default had no lower
bound. The new default score formula is ::

    max(0, 0 if fatal else 10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10))

If your project contains a configuration file created by an earlier version of
Pylint, you can set ``evaluation`` to the above expression to get the new
behavior. Likewise, since negative values are still technically supported,
``evaluation`` can be set to a version of the above expression that does not
enforce a floor of zero.

How do I avoid getting unused argument warnings for API I do not control?
-------------------------------------------------------------------------

Prefix (ui) the callback's name by `cb_` (callback), as in cb_onclick(...). By
doing so arguments usage won't be checked. Another solution is to
use one of the names defined in the "dummy-variables" configuration
variable for unused argument ("_" and "dummy" by default).

What is the format of the configuration file?
---------------------------------------------

The configuration file can be an ``ini`` or ``toml`` file. See the :ref:`exhaustive list of possible options <all-options>`.

Why are there a bunch of messages disabled by default?
------------------------------------------------------

Either because they are prone to false positives or that they are opinionated enough
to not be included as default messages.

You can see the plugin you need to explicitly :ref:`load in the technical reference
<user_guide/checkers/extensions:optional checkers>`.

Which messages should I disable to avoid duplicates if I use other popular linters ?
------------------------------------------------------------------------------------

pycodestyle_: unneeded-not, line-too-long, unnecessary-semicolon, trailing-whitespace, missing-final-newline, bad-indentation, multiple-statements, bare-except, wrong-import-position

pyflakes_: undefined-variable, unused-import, unused-variable

mccabe_: too-many-branches

pydocstyle_: missing-module-docstring, missing-class-docstring, missing-function-docstring

pep8-naming_: invalid-name, bad-classmethod-argument, bad-mcs-classmethod-argument, no-self-argument

isort_ and flake8-import-order_: wrong-import-order

.. _`pycodestyle`: https://github.com/PyCQA/pycodestyle
.. _`pyflakes`: https://github.com/PyCQA/pyflakes
.. _`mccabe`: https://github.com/PyCQA/mccabe
.. _`pydocstyle`: https://github.com/PyCQA/pydocstyle
.. _`pep8-naming`: https://github.com/PyCQA/pep8-naming
.. _`isort`: https://github.com/pycqa/isort
.. _`flake8-import-order`: https://github.com/PyCQA/flake8-import-order

How do I avoid "access to undefined member" messages in my mixin classes?
-------------------------------------------------------------------------

You should add the ``no-member`` message to your ``ignored-checks-for-mixins`` option
and name your mixin class with a name which ends with "Mixin" or "mixin" (default)
or change the default value by changing the ``mixin-class-rgx`` option.

Where is the persistent data stored to compare between successive runs?
-----------------------------------------------------------------------

Analysis data are stored as a pickle file in a directory which is
localized using the following rules:

* value of the PYLINTHOME environment variable if set
* "pylint" subdirectory of the user's XDG_CACHE_HOME if the environment variable is set, otherwise
    - Linux: "~/.cache/pylint"
    - macOS: "~/Library/Caches/pylint"
    - Windows: "C:\Users\<username>\AppData\Local\pylint"
* ".pylint.d" directory in the current directory
