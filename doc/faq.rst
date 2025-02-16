.. _faq:

==========================
Frequently Asked Questions
==========================

How do I install Pylint?
------------------------

.. include:: short_text_installation.rst

How do I contribute to Pylint?
------------------------------

.. include:: short_text_contribute.rst


Does Pylint follow a versioning scheme?
----------------------------------------

See :ref:`upgrading pylint in the installation guide <upgrading_pylint>`.

How do I find the name corresponding to a specific command line option?
-----------------------------------------------------------------------

See :ref:`the configuration documentation <all-configurations-options>`.

What is the format of the configuration file?
---------------------------------------------

The configuration file can be an ``ini`` or ``toml`` file. See the :ref:`exhaustive list of possible options <all-options>`.

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


Why are there a bunch of messages disabled by default?
------------------------------------------------------

Either because they are prone to false positives or that they are opinionated enough
to not be included as default messages.

You can see the plugin you need to explicitly :ref:`load in the technical reference
<user_guide/checkers/extensions:optional checkers>`.

I want to run pylint on each keystroke in my IDE. How do I do that?
---------------------------------------------------------------------

Pylint full suite of checks will never be fast enough to run on every keystroke.
However, some IDEs can run pylint  when the IDE opens or saves files.
See, for example, the `Microsoft plugin for VS Code`_.


That said, pylint is best suited for linting on save for small projects, for continuous
integration jobs, or a git ``pre-push`` hook for big projects. The larger your repository
is, the slower pylint will be.

If you want to make pylint faster for this type of use case, you can use the ``--errors-only``
option, which will remove all the refactor, convention, and warning checks. You can also disable
checks with inherently high complexity that need to analyse the full code base like
``duplicate-code`` or ``cyclic-import`` (this list is not exhaustive).

.. _`Microsoft plugin for VS Code`: https://github.com/microsoft/vscode-pylint#readme

Why do I have non-deterministic results when I try to parallelize pylint ?
--------------------------------------------------------------------------

pylint should analyse all your code at once in order to best infer the
actual values that result from calls. If only some of the files are given, pylint might
miss a particular value's type and produce inferior inference for the subset. Parallelization
of pylint is not easy; we also discourage the use of the ``-j`` option if this matters to you.


Which messages should I disable to avoid duplicates if I use other popular linters ?
------------------------------------------------------------------------------------

pycodestyle_: bad-indentation, bare-except, line-too-long, missing-final-newline, multiple-statements, singleton-comparison, trailing-newlines, trailing-whitespace, unnecessary-negation, unnecessary-semicolon, wrong-import-position

pyflakes_: undefined-variable, unused-import, unused-variable

mccabe_: too-many-branches

pydocstyle_: missing-module-docstring, missing-class-docstring, missing-function-docstring

pep8-naming_: invalid-name, bad-classmethod-argument, bad-mcs-classmethod-argument, no-self-argument

isort_ and flake8-import-order_: ungrouped-imports, wrong-import-order

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

How does the website pylint dot org relate to this project?
-----------------------------------------------------------

Historically, pylint dot org served as the primary website for Pylint. However,
we no longer have access to the domain. The current owners are monetizing
this by displaying advertisements alongside outdated documentation without
contributing to pylint at all. For the latest and official Pylint documentation,
please visit `pylint.readthedocs.io <https://pylint.readthedocs.io/en/stable/>`_.

Please see `issue 8934 <https://github.com/pylint-dev/pylint/issues/8934>`_
for more details.
