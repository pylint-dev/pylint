.. _contributor_install:

Contributor installation
========================

Basic installation
------------------

Pylint is developed using the git_ distributed version control system.

You can clone Pylint using ::

  git clone https://github.com/pylint-dev/pylint

Before you start testing your code, you need to install your source-code package locally.
Suppose you just cloned pylint with the previous ``git clone`` command. To set up your
environment for testing, open a terminal and run::

    cd pylint
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements_test_min.txt
    pip install -e .

This ensures your testing environment is similar to Pylint's testing environment on GitHub.

**Optionally** (Because there's an auto-fix if you open a merge request): We have
pre-commit hooks which should take care of the autoformatting for you before each
commit. To enable it, run ``pre-commit install`` in the ``pylint`` root directory.

**Even more optionally**: You can enable slow on push hooks with ``pre-commit install --install-hooks -t pre-push``.
It will do slow checks like checking that the generated documentation is up to date
before each push.

Astroid installation
--------------------

If you're testing new changes in astroid you need to also clone astroid_ and install
with an editable installation alongside pylint as follows::

    # Suppose you're in the pylint directory
    git clone https://github.com/pylint-dev/astroid.git
    python3 -m pip install -e astroid/

You're now using the local astroid in pylint and can control the version with git for example::

    cd astroid/
    git switch my-astroid-dev-branch

.. _pytest-cov: https://pypi.org/project/pytest-cov/
.. _astroid: https://github.com/pylint-dev/astroid
.. _git: https://git-scm.com/
