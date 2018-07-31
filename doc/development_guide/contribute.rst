.. -*- coding: utf-8 -*-

==============
 Contributing
==============

.. _bug reports, feedback:

Bug reports, feedback
---------------------

You think you have found a bug in Pylint? Well, this may be the case
since Pylint is under heavy development!

Please take the time to check if it is already in the issue tracker at
https://github.com/PyCQA/pylint

If you cannot find it in the tracker, create a new issue there or discuss your
problem on the code-quality@python.org mailing list.

The code-quality mailing list is also a nice place to provide feedback about
Pylint, since it is shared with other tools that aim at improving the quality of
python code.

Note that if you don't find something you have expected in Pylint's
issue tracker, it may be because it is an issue with one of its dependencies, namely
astroid:

* https://github.com/PyCQA/astroid

.. _Mailing lists:

Mailing lists
-------------

You can subscribe to this mailing list at
http://mail.python.org/mailman/listinfo/code-quality

Archives are available at
http://mail.python.org/pipermail/code-quality/

Archives before April 2013 are available at
http://lists.logilab.org/pipermail/python-projects/


.. _repository:

Repository
----------

Pylint is developed using the git_ distributed version control system.

You can clone Pylint and its dependencies from ::

  git clone https://github.com/PyCQA/pylint
  git clone https://github.com/PyCQA/astroid

.. _git: https://git-scm.com/

Got a change for Pylint?  Below are a few steps you should take to make sure
your patch gets accepted.

- Test your code

  * Pylint is very well tested, with a high good code coverage.
    It has two types of tests, usual unittests and functional tests.

    The usual unittests can be found under `/pylint/test` directory and they can
    be used for testing almost anything Pylint related. But for the ease
    of testing Pylint's messages, we also have the concept of functional tests.

  * You should also run all the tests to ensure that your change isn't
    breaking one. You can run the tests using the tox_ package, as in::

      python -m tox
      python -m tox -epy36 # for Python 3.6 suite only
      python -m tox -epylint # for running Pylint over Pylint's codebase

  * To run only a specific test suite, use a pattern for the test filename
    (**without** the ``.py`` extension), as in::

      python -m tox -e py36 -- -k test_functional
      python -m tox -e py36 -- -k  \*func\*

  * Since we just use pytest_ to run the tests, you can also use it as well,
    although we highly recommend using tox_ instead::

      pytest pylint -k test_functional


- Add a short entry to the ChangeLog describing the change, except for internal
  implementation only changes. Not usually required, but for changes other than small
  bugs we also add a couple of sentences in the release document for that release,
  (`What's New` section). For the release document we usually write some more details,
  and it is also a good place to offer examples on how the new change is supposed to work.

- Add yourself to the `CONTRIBUTORS` file, if you are not already there.

- Write a comprehensive commit message

- Relate your change to an issue in the tracker if such an issue exists (see
  `Closing issues via commit messages`_ of the GitHub documentation for more
  information on this)

- Document your change, if it is a non-trivial one.

- Send a pull request from GitHub (see `About pull requests`_ for more insight
  about this topic)


.. _functional_tests:

Functional Tests
----------------

These are residing under '/pylint/test/functional' and they are formed of multiple
components. First, each Python file is considered to be a test case and it
should be accompanied by a .txt file, having the same name, with the messages
that are supposed to be emitted by the given test file.

In the Python file, each line for which Pylint is supposed to emit a message
has to be annotated with a comment in the form ``# [message_symbol]``, as in::

    a, b, c = 1 # [unbalanced-tuple-unpacking]

If multiple messages are expected on the same line, then this syntax can be used::

    a, b, c = 1.test # [unbalanced-tuple-unpacking, no-member]

The syntax of the .txt file has to be this::

    symbol:line_number:function_or_class:Expected message

For example, this is a valid message line::

    abstract-class-instantiated:79:main:Abstract class 'BadClass' with abstract methods instantiated

If the Python file is expected to not emit any errors, then the .txt file has to be empty.
If you need special control over Pylint's flag, you can also create a .rc file, which
can have sections of Pylint's configuration.

During development, it's sometimes helpful to run all functional tests in your
current environment in order to have faster feedback. Run with::

    python pylint/test/test_functional.py

.. _`Closing issues via commit messages`: https://help.github.com/articles/closing-issues-via-commit-messages/
.. _`About pull requests`: https://help.github.com/articles/using-pull-requests/
.. _tox: http://tox.readthedocs.io/en/latest/
.. _pytest: http://pytest.readthedocs.io/en/latest/


Tips for Getting Started with Pylint Development
------------------------------------------------
* Read the :ref:`technical-reference`. It gives a short walkthrough of the pylint
  codebase and will help you identify where you will need to make changes
  for what you are trying to implement.

* :func:`astroid.extract_node` is your friend. Most checkers are AST based,
  so you will likely need to interact with :mod:`astroid`.
  A short example of how to use :func:`astroid.extract_node` is given
  :ref:`here <astroid_extract_node>`.

* When fixing a bug for a specific check, search the code for the warning
  message to find where the warning is raised,
  and therefore where the logic for that code exists.
