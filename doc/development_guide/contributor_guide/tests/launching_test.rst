Launching tests
===============

pytest
------

Since we use pytest_ to run the tests, you can also use it on its own.
We do recommend using the tox_ command though::

    pytest tests/ -k test_functional

You can use pytest_ directly. If you want to run tests on a specific portion of the
code with pytest_ and your local python version::

    python3 -m pytest


Everything in tests/message with coverage for the relevant code (require `pytest-cov`_)::

    python3 -m pytest tests/message/ --cov=pylint.message
    coverage html

Only the functional test "missing_kwoa_py3"::

    python3 -m pytest "tests/test_functional.py::test_functional[missing_kwoa_py3]"

tox
---

You can also *optionally* install tox_ and run our tests using the tox_ package, as in::

    python -m tox
    python -m tox -epy313 # for Python 3.13 suite only
    python -m tox -epylint # for running Pylint over Pylint's codebase
    python -m tox -eformatting # for running formatting checks over Pylint's codebase

It's usually a good idea to run tox_ with ``--recreate``. This flag tells tox_ to re-download
all dependencies before running the tests. This can be important when a new version of
astroid_ or any of the other dependencies has been published::

    python -m tox --recreate # The entire tox environment will be recreated
    python -m tox --recreate -e py310 # The python 3.10 tox environment will be recreated


To run only a specific test suite, use a pattern for the test filename
(**without** the ``.py`` extension), as in::

    python -m tox -e py310 -- -k test_functional
    python -m tox -e py310 -- -k  \*func\*
    python -m tox --recreate -e py310 -- -k test_functional # With recreation of the environment


.. _primer_tests:

Primer tests
------------

Pylint also uses what we refer to as ``primer`` tests. These are tests that are run automatically
in our Continuous Integration and check whether any changes in Pylint lead to crashes or fatal errors
on the ``stdlib``, and also assess a pull request's impact on the linting of a selection of external
repositories by posting the diff against ``pylint``'s current output as a comment.

To run the primer test for the ``stdlib``, which only checks for crashes and fatal errors, you can add
``--primer-stdlib`` to the pytest_ command. For example::

    pytest -m primer_stdlib --primer-stdlib

To produce the output generated on Continuous Integration for the linting of external repositories,
run these commands::

    python tests/primer/__main__.py prepare --clone
    python tests/primer/__main__.py run --type=pr

To fully simulate the process on Continuous Integration, you should then checkout ``main``, and
then run these commands::

    python tests/primer/__main__.py run --type=main
    python tests/primer/__main__.py compare

The list of repositories is created on the basis of three criteria: 1) projects need to use a diverse
range of language features, 2) projects need to be well maintained and 3) projects should not have a codebase
that is too repetitive. This guarantees a good balance between speed of our CI and finding potential bugs.

You can find the latest list of repositories and any relevant code for these tests in the ``tests/primer``
directory.

.. _pytest-cov: https://pypi.org/project/pytest-cov/
.. _astroid: https://github.com/pylint-dev/astroid
