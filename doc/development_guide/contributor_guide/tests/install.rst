Installation
============

Before you start testing your code, you need to install your source-code package locally.
Suppose you have cloned pylint into a directory, say ``my-pylint``.
To set up your environment for testing, open a terminal and run::

    cd my-pylint
    pip install -r requirements_test_min.txt

This ensures your testing environment is similar to Pylint's testing environment on GitHub.

If you're testing new changes in astroid you need to clone astroid_ and install
with an editable installation as follows::

    git clone https://github.com/PyCQA/astroid.git
    cd astroid
    python3 -m pip install -e .

If you want to check the coverage locally, consider using `pytest-cov`_::

    python3 -m pip install pytest-cov

.. _pytest-cov: https://pypi.org/project/pytest-cov/
.. _astroid: https://github.com/pycqa/astroid
