.. _writing_tests:

Writing tests
=============

Pylint uses three types of tests: unittests, functional tests and primer tests.

- :ref:`unittests <writing_unittests>` can be found in ``pylint/tests``. Unless you're working on pylint's
  internal you're probably not going to have to write any.
- :ref:`Global functional tests <writing_functional_tests>`  can be found in the ``pylint/tests/functional``. They are
  mainly used to test whether Pylint emits the correct messages.
- :ref:`Configuration's functional tests <writing_config_functional_tests>`  can be found in the
  ``pylint/tests/config/functional``. They are used to test Pylint's configuration loading.
- :ref:`Primer tests <primer_tests>` you can suggest a new external repository to check but there's nothing to do
  most of the time.

.. _writing_unittests:

Unittest tests
--------------

Most other tests reside in the '/pylint/test' directory. These unittests can be used to test
almost all functionality within Pylint. A good step before writing any new unittests is to look
at some tests that test a similar functionality. This can often help write new tests.

If your new test requires any additional files you can put those in the
``/pylint/test/regrtest_data`` directory. This is the directory we use to store any data needed for
the unittests.



.. _writing_functional_tests:

Functional tests
----------------

These are located under ``/pylint/test/functional`` and they are formed of multiple
components. First, each Python file is considered to be a test case and it
should be accompanied by a ``.txt`` file, having the same name. The ``.txt`` file contains the ``pylint`` messages
that are supposed to be emitted by the given test file.

In your ``.py`` test file, each line for which Pylint is supposed to emit a message
has to be annotated with a comment following this pattern ``# [message_symbol]``, as in::

    a, b, c = 1 # [unbalanced-tuple-unpacking]

If multiple messages are expected on the same line, then this syntax can be used::

    a, b, c = 1.test # [unbalanced-tuple-unpacking, no-member]

You can also use  ``# +n: [`` where ``n`` is an integer to deal with special cases, e.g., where the above regular syntax makes the line too long::

    A = 5
    # +1: [singleton-comparison]
    B = A == None  # The test will look for the `singleton-comparison` message in this line

If you need special control over Pylint's configuration, you can also create a ``.rc`` file, which
can set sections of Pylint's configuration.
The ``.rc`` file can also contain a section ``[testoptions]`` to pass options for the functional
test runner. The following options are currently supported:

- "min_pyver": Minimal python version required to run the test
- "max_pyver": Python version from which the test won't be run. If the last supported version is 3.9 this setting should be set to 3.10.
- "min_pyver_end_position": Minimal python version required to check the end_line and end_column attributes of the message
- "requires": Packages required to be installed locally to run the test
- "except_implementations": List of python implementations on which the test should not run
- "exclude_platforms": List of operating systems on which the test should not run

**Functional test file locations**

For existing checkers, new test cases should preferably be appended to the existing test file.
For new checkers, a new file ``new_checker_message.py`` should be created (Note the use of
underscores). This file should then be placed in the ``test/functional/n`` sub-directory.

Some additional notes:

- If the checker is part of an extension the test should go in ``test/functional/ext/extension_name``
- If the test is a regression test it should go in ``test/r/regression`` or ``test/r/regression_02``.
  The file name should start with ``regression_``.
- For some sub-directories, such as ``test/functional/u``, there are additional sub-directories (``test/functional/u/use``).
  Please check if your test file should be placed in any of these directories. It should be placed there
  if the sub-directory name matches the word before the first underscore of your test file name.

The folder structure is enforced when running the test suite, so you might be directed to put the file
in a different sub-directory.

**Running and updating functional tests**

During development, it's sometimes helpful to run all functional tests in your
current environment in order to have faster feedback. Run from Pylint root directory with::

    python tests/test_functional.py

You can use all the options you would use for pytest_, for example ``-k "test_functional[len_checks]"``.
Furthermore, if required the .txt file with expected messages can be regenerated based
on the the current output by appending ``--update-functional-output`` to the command line::

    python tests/test_functional.py --update-functional-output -k "test_functional[len_checks]"


.. _writing_config_functional_tests:

Functional tests for configurations
-----------------------------------

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


.. _tox: https://tox.wiki/en/latest/
.. _pytest: https://docs.pytest.org/en/latest/
.. _pytest-cov: https://pypi.org/project/pytest-cov/
.. _astroid: https://github.com/pylint-dev/astroid
