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

.. image:: https://results.pre-commit.ci/badge/github/PyCQA/pylint/main.svg
   :target: https://results.pre-commit.ci/latest/github/PyCQA/pylint/main
   :alt: pre-commit.ci status

.. |tideliftlogo| image:: https://raw.githubusercontent.com/PyCQA/pylint/main/doc/media/Tidelift_Logos_RGB_Tidelift_Shorthand_On-White.png
   :width: 200
   :alt: Tidelift

.. list-table::
   :widths: 10 100

   * - |tideliftlogo|
     - Professional support for pylint is available as part of the `Tidelift
       Subscription`_.  Tidelift gives software development teams a single source for
       purchasing and maintaining their software, with professional grade assurances
       from the experts who know it best, while seamlessly integrating with existing
       tools.

.. _Tidelift Subscription: https://tidelift.com/subscription/pkg/pypi-pylint?utm_source=pypi-pylint&utm_medium=referral&utm_campaign=readme

Documentation
=============

Please check `the full documentation`_.

.. _`the full documentation`: https://pylint.pycqa.org/

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

- :ref:`pyreverse <pyreverse>` (standalone tool that generates package and class diagrams.)
- :ref:`symilar <symilar>`  (duplicate code finder that is also integrated in pylint)
- :ref:`epylint <pylint_in_flymake>` (Emacs and Flymake compatible Pylint)

Install
-------

Pylint can be simply installed by running::

    pip install pylint

If you are using Python 3.7.2+, upgrade to get full support for your version::

    pip install pylint --upgrade

If you want to install from a source distribution, extract the tarball and run
the following command ::

    python setup.py install


Do make sure to do the same for astroid, which is used internally by pylint.

For debian and rpm packages, use your usual tools according to your Linux distribution.

More information about installation and available distribution format
can be found here_.

Testing
-------

You should be able to install our tests dependencies with::

    pip install -r requirements_test.txt

You can then use pytest_ directly. If you want to run tests on a specific portion of the
code with pytest_ and your local python version::

    # ( pip install pytest-cov )
    python3 -m pytest
    # Everything in tests/message with coverage for the relevant code:
    python3 -m pytest tests/message/ --cov=pylint.message
    coverage html
    # Only the functional test "missing_kwoa_py3":
    python3 -m pytest "tests/test_functional.py::test_functional[missing_kwoa_py3]"

You can also *optionally* install tox_. To run the test suite for a particular
Python version, with tox you can do::

    tox -e py39

To run individual tests with ``tox``, you can do::

    tox -e py37 -- -k name_of_the_test

If you're testing new changes in astroid you need to clone astroid_ and install
with an editable installation as follows::

    git clone https://github.com/PyCQA/astroid.git
    cd astroid
    python3 -m pip install -e .

Show your usage
-----------------

You can place this badge in your README to let others know your project uses pylint.

    .. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
        :target: https://github.com/PyCQA/pylint

Use the badge in your project's README.md (or any other Markdown file)::

    [![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)

Use the badge in your project's README.rst (or any other rst file)::

    .. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
        :target: https://github.com/PyCQA/pylint


If you use GitHub Actions, and one of your CI workflows begins with "name: pylint", you
can use GitHub's `workflow status badges <https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge#using-the-workflow-file-name>`_
to show an up-to-date indication of whether pushes to your default branch pass pylint.
For more detailed information, check the documentation.

.. _here: https://pylint.pycqa.org/en/latest/user_guide/installation.html
.. _tox: https://tox.readthedocs.io/en/latest/
.. _pytest: https://docs.pytest.org/en/latest/
.. _pytest-benchmark: https://pytest-benchmark.readthedocs.io/en/latest/index.html
.. _pytest-cov: https://pypi.org/project/pytest-cov/
.. _astroid: https://github.com/PyCQA/astroid

License
-------

pylint is, with a few exceptions listed below, `GPLv2 <https://github.com/PyCQA/pylint/blob/main/LICENSE>`_.

The icon files are licensed under the `CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0/>`_ license:

- `doc/logo.png <https://raw.githubusercontent.com/PyCQA/pylint/main/doc/logo.png>`_
- `doc/logo.svg <https://raw.githubusercontent.com/PyCQA/pylint/main/doc/logo.svg>`_
