.. -*- coding: utf-8 -*-

==============
 Introduction
==============

What is Pylint?
---------------

Pylint is a tool that checks for errors in Python code, tries to enforce a
coding standard and looks for `code smells`_. It can also look for certain type
errors, it can recommend suggestions about how particular blocks
can be refactored and can offer you details about the code's complexity.

Other similar projects would include pychecker_ (now defunct), pyflakes_,
flake8_, and mypy_. The default coding style used by Pylint is close to `PEP 8`_.

Pylint will display a number of messages as it analyzes the code and it can
also be used for displaying some statistics about the number of warnings and
errors found in different files. The messages are classified under various
categories such as errors and warnings.

Last but not least, the code is given an overall mark, based on the number and
severity of the warnings and errors.

.. _pychecker: https://pypi.org/project/PyChecker/
.. _pyflakes: https://github.com/PyCQA/pyflakes
.. _flake8: https://gitlab.com/pycqa/flake8/
.. _mypy: https://github.com/python/mypy
.. _`PEP 8`: https://peps.python.org/pep-0008/
.. _`Guido's style guide`: https://www.python.org/doc/essays/styleguide/
.. _`refactoring book`: https://www.refactoring.com/
.. _`code smells`: https://martinfowler.com/bliki/CodeSmell.html

What Pylint is not?
-------------------

What Pylint says is not to be taken as gospel and Pylint isn't smarter than you
are: it may warn you about things that you have conscientiously done.

Pylint tries hard to report as few false positives as possible for errors, but
it may be too verbose with warnings. That's for example because it tries to
detect things that may be dangerous in a context, but are not in others, or
because it checks for some things that you don't care about. Generally, you
shouldn't expect Pylint to be totally quiet about your code, so don't
necessarily be alarmed if it gives you a hell lot of messages for your project!

The best way to tackle pylint's verboseness is to:

* enable or disable the messages or message categories that you want to be
  activated or not for when pylint is analyzing your code.
  This can be done easily through a command line flag. For instance, disabling
  all convention messages is simple as a ``--disable=C`` option added to pylint
  command.

* manage the configuration through a configuration file. With the option
  ``generate-toml-config`` you can create a piece of ``.toml`` text to put
  in your ``pyproject.toml`` file.
