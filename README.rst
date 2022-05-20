Pylint
======

.. image:: https://github.com/PyCQA/pylint/actions/workflows/tests.yaml/badge.svg?branch=main
    :target: https://github.com/PyCQA/pylint/actions

.. image:: https://coveralls.io/repos/github/PyCQA/pylint/badge.svg?branch=main
    :target: https://coveralls.io/github/PyCQA/pylint?branch=main

.. image:: https://img.shields.io/pypi/v/pylint.svg
    :alt: Pypi Package version
    :target: https://pypi.python.org/pypi/pylint

.. image:: https://readthedocs.org/projects/pylint/badge/?version=latest
    :target: https://pylint.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/PyCQA/pylint

.. image:: https://results.pre-commit.ci/badge/github/PyCQA/pylint/main.svg
   :target: https://results.pre-commit.ci/latest/github/PyCQA/pylint/main
   :alt: pre-commit.ci status

.. |tideliftlogo| image:: https://raw.githubusercontent.com/PyCQA/pylint/main/doc/media/Tidelift_Logos_RGB_Tidelift_Shorthand_On-White.png
   :width: 200
   :alt: Tidelift

What is pylint ?
================

.. Do not modify this without also modifying doc/index.rst

Pylint is a `static code analyser`_ for Python 2 or 3. The latest version supports Python
3.7.2 and above.

.. _`static code analyser`: https://en.wikipedia.org/wiki/Static_code_analysis

Pylint analyses your code without actually running it. It checks for errors, enforces a coding
standard, looks for `code smells`_, and can make suggestions about how the code could be refactored.

.. _`code smells`: https://martinfowler.com/bliki/CodeSmell.html

Pylint can infer actual values from your code using its internal code representation (astroid).
If your code is ``import logging as argparse``, Pylint will know that ``argparse.error(...)``
is in fact a logging call and not an argparse call.

Pylint isn't smarter than you: it may warn you about things that you have
conscientiously done or checks for some things that you don't care about.
During adoption, especially in a legacy project where pylint was never enforced,
it's best to start with the ``--errors-only`` flag, then disable
convention and refactor message with ``--disable=C,R`` and progressively
re-evaluate and re-enable messages as your priorities evolve.

Pylint ships with three additional tools:

- pyreverse_ (standalone tool that generates package and class diagrams.)
- symilar_  (duplicate code finder that is also integrated in pylint)
- epylint_ (Emacs and Flymake compatible Pylint)

.. Enf of do not modify this without also modifying doc/index.rst

.. _pyreverse: https://pylint.pycqa.org/en/latest/pyreverse.html
.. _symilar: https://pylint.pycqa.org/en/latest/symilar.html
.. _epylint: https://pylint.pycqa.org/en/latest/user_guide/ide_integration/flymake-emacs.html

Install
-------

.. Do not modify anything here, modify doc/user_guide/installation.rst instead

For command line use, pylint is installed with::

    pip install pylint

It can also be integrated in most editors or IDE. More information can be found
`in the documentation`_.

.. _in the documentation: https://pylint.pycqa.org/en/latest/user_guide/installation.html

Documentation
=============

Please check `the full documentation`_.

.. _`the full documentation`: https://pylint.pycqa.org/

Contributing
------------

We welcome all contributions, doc, code, checking issues for duplicate or telling us
that we can close them, confirming that it's still an issue, `creating issues because
you found a bug or want a feature`_... everything helps !

Please follow the `code of conduct`_ and check `the contribution documentation`_ if you want to
make a code contribution.

.. _creating issues because you found a bug or want a feature: https://pylint.pycqa.org/en/latest/contact.html#bug-reports-feedback
.. _code of conduct: https://github.com/Pierre-Sassoulas/pylint/blob/main/CODE_OF_CONDUCT.md
.. _the contribution documentation: https://pylint.pycqa.org/en/latest/development_guide/contribute.html


Show your usage
-----------------

You can place this badge in your README to let others know your project uses pylint.

    .. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
        :target: https://github.com/PyCQA/pylint

See how in `the badge documentation`_.

.. _the badge documentation: https://pylint.pycqa.org/en/latest/user_guide/badge.html

License
-------

pylint is, with a few exceptions listed below, `GPLv2 <https://github.com/PyCQA/pylint/blob/main/LICENSE>`_.

The icon files are licensed under the `CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0/>`_ license:

- `doc/logo.png <https://raw.githubusercontent.com/PyCQA/pylint/main/doc/logo.png>`_
- `doc/logo.svg <https://raw.githubusercontent.com/PyCQA/pylint/main/doc/logo.svg>`_

Support
-------

Please check `the contact information`_ in the documentation.

.. _`the contact information`: https://pylint.pycqa.org/en/latest/contact.html

.. list-table::
   :widths: 10 100

   * - |tideliftlogo|
     - Professional support for pylint is available as part of the `Tidelift
       Subscription`_.  Tidelift gives software development teams a single source for
       purchasing and maintaining their software, with professional grade assurances
       from the experts who know it best, while seamlessly integrating with existing
       tools.

.. _Tidelift Subscription: https://tidelift.com/subscription/pkg/pypi-pylint?utm_source=pypi-pylint&utm_medium=referral&utm_campaign=readme
