.. -*- coding: utf-8 -*-
.. _testing:

==============
 Testing
==============

.. _test_your_code:

Test your code!
----------------

Pylint is very well tested and has a high code coverage. New contributions are not accepted
unless they include tests.
Pylint uses two types of tests: unittests and functional tests.

  - The unittests can be found in the ``/pylint/test`` directory and they can
    be used for testing almost anything Pylint related.

  - The functional tests can be found in the ``/pylint/test/functional`` directory. They are
    mainly used to test whether Pylint emits the correct messages.

Before writing a new test it is often a good idea to ensure that your change isn't
breaking a current test. You can run our tests using the tox_ package, as in::

    python -m tox
    python -m tox -epy36 # for Python 3.6 suite only
    python -m tox -epylint # for running Pylint over Pylint's codebase
    python -m tox -eformatting # for running formatting checks over Pylint's codebase

It's usually a good idea to run tox_ with ``--recreate``. This flag tells tox_ to redownload
all dependencies before running the tests. This can be important when a new version of
astroid_ or any of the other dependencies has been published::

    python -m tox --recreate # The entire tox environment will be recreated
    python -m tox --recreate -e py310 # The python 3.10 tox environment will be recreated


To run only a specific test suite, use a pattern for the test filename
(**without** the ``.py`` extension), as in::

    python -m tox -e py310 -- -k test_functional
    python -m tox -e py310 -- -k  \*func\*
    python -m tox --recreate -e py310 -- -k test_functional # With recreation of the environment

Since we use pytest_ to run the tests, you can also use it on its own.
We do recommend using the tox_ command though::

    pytest pylint -k test_functional

Writing functional tests
------------------------

These are residing under ``/pylint/test/functional`` and they are formed of multiple
components. First, each Python file is considered to be a test case and it
should be accompanied by a .txt file, having the same name, with the messages
that are supposed to be emitted by the given test file.

In the Python file, each line for which Pylint is supposed to emit a message
has to be annotated with a comment in the form ``# [message_symbol]``, as in::

    a, b, c = 1 # [unbalanced-tuple-unpacking]

If multiple messages are expected on the same line, then this syntax can be used::

    a, b, c = 1.test # [unbalanced-tuple-unpacking, no-member]

You can also use ``# +n: [`` with n an integer if the above syntax would make the line too long or other reasons::

    # +1: [empty-comment]
    #

If you need special control over Pylint's configuration, you can also create a .rc file, which
can have sections of Pylint's configuration.
The .rc file can also contain a section ``[testoptions]`` to pass options for the functional
test runner. The following options are currently supported:

    "min_pyver": Minimal python version required to run the test
    "max_pyver": Maximum python version required to run the test
    "min_pyver_end_position": Minimal python version required to check the end_line and end_column attributes of the message
    "requires": Packages required to be installed locally to run the test
    "except_implementations": List of python implementations on which the test should not run
    "exclude_platforms": List of operating systems on which the test should not run

During development, it's sometimes helpful to run all functional tests in your
current environment in order to have faster feedback. Run from Pylint root directory with::

    python tests/test_functional.py

You can use all the options you would use for pytest_, for example ``-k "test_functional[len_checks]"``.
Furthermore, if required the .txt file with expected messages can be regenerated based
on the the current output by appending ``--update-functional-output`` to the command line::

    python tests/test_functional.py --update-functional-output -k "test_functional[len_checks]"

Writing unittest tests
------------------------

Most other tests reside in the '/pylint/test' directory. These unittests can be used to test
almost all functionality within Pylint. A good step before writing any new unittests is to look
at some tests that test a similar funcitionality. This can often help write new tests.

If your new test requires any additional files you can put those in the
``/pylint/test/regrtest_data`` directory. This is the directory we use to store any data needed for
the unittests.


Writing functional tests for configurations
-------------------------------------------

To test the different ways to configure Pylint there is also a small functional test framework
for configuration files. These tests can be found in the '/pylint/test/config' directory.

To create a new test create a new file with an unused name in the directory of that type
of configuration file. Subsequently add a ``filename.result.json`` file with 'filename'
being the same name as your configuration file. This file should record
what the configuration should be **compared to the standard configuration**.

For example, if the configuration should add a warning to the list of disabled messages
and you changed the configuration for ``job`` to 10 instead of the default 1 the
``.json`` file should include::

    "functional_append": {
        "disable": [["a-message-to-be-added"],]
    }
    "jobs": 10,

Similarly if a message should be removed you can add the following to the ``.json`` file::

    "functional_remove": {
        "disable": [["a-message-to-be-removed"],]
    }

If a configuration is incorrect and should lead to a crash or warning being emitted you can
specify this by adding a ``.out`` file. This file should have the following name
``name_of_configuration_testfile.error_code.out``. So, if your test is called ``bad_configuration.toml``
and should exit with exit code 2 the ``.out`` file should be named ``bad_configuration.2.out``.
The content of the ``.out`` file should have a similar pattern as a normal Pylint output. Note that the
module name should be ``{abspath}`` and the file name ``{relpath}``.

Primer tests
-------------------------------------------

Pylint also uses what we refer to as ``primer`` tests. These are tests that are run automatically
in our Continuous Integration and check whether any changes in Pylint lead to crashes or fatal errors
on the ``stdlib`` and a selection of external repositories.

To run the ``primer`` tests you can add either ``--primer-stdlib`` or ``--primer-external`` to the
pytest_ command. If you want to only run the ``primer`` you can add either of their marks, for example::

    pytest -m primer_external --primer-external

The list of repositories is created on the basis of three criteria: 1) projects need to use a diverse
range of language features, 2) projects need to be well maintained and 3) projects should not have a codebase
that is too repetitive. This guarantees a good balance between speed of our CI and finding potential bugs.

You can find the latest list of repositories and any relevant code for these tests in the ``tests/primer``
directory.

.. _tox: https://tox.readthedocs.io/en/latest/
.. _pytest: https://pytest.readthedocs.io/en/latest/
.. _astroid: https://github.com/pycqa/astroid
