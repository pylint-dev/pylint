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
problem on the code-quality@python.org mailing list or using the discord server https://discord.gg/kFebW799.

The code-quality mailing list is also a nice place to provide feedback about
Pylint, since it is shared with other tools that aim at improving the quality of
python code.

Note that if you don't find something you have expected in Pylint's issue
tracker, it may be because it is an issue with one of its dependencies, namely
astroid:

* https://github.com/PyCQA/astroid

.. _Mailing lists:

Discord server
--------------

https://discord.gg/Egy6P8AMB5

Mailing lists
-------------

You can subscribe to this mailing list at
https://mail.python.org/mailman/listinfo/code-quality

Archives are available at
https://mail.python.org/pipermail/code-quality/

Archives before April 2013 are available at
https://lists.logilab.org/pipermail/python-projects/


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

  * Pylint is very well tested, with a high code coverage.
    It has two types of tests, usual unittests and functional tests.

    The usual unittests can be found under `/pylint/test` directory and they can
    be used for testing almost anything Pylint related. But for the ease
    of testing Pylint's messages, we also have the concept of functional tests.

  * You should also run all the tests to ensure that your change isn't a
    breaking one. You can run the tests using the tox_ package, as in::

      python -m tox
      python -m tox -epy36 # for Python 3.6 suite only
      python -m tox -epylint # for running Pylint over Pylint's codebase
      python -m tox -eformatting # for running formatting checks over Pylint's codebase

  * It's usually a good idea to run tox_ with ``--recreate``. This is needed because
    the tox environment might use an older version of astroid_, which can cause various failures
    when you are running against the latest pylint::

     python -m tox --recreate # The entire tox environment is going to be recreated


  * To run only a specific test suite, use a pattern for the test filename
    (**without** the ``.py`` extension), as in::

      python -m tox -e py36 -- -k test_functional
      python -m tox -e py36 -- -k  \*func\*

  * Since we just use pytest_ to run the tests, you can also use it as well,
    although we highly recommend using tox_ instead::

      pytest pylint -k test_functional

  * ``pylint`` uses black_ and isort_ among other Python autoformatters.
    We have a pre-commit hook which should take care of the autoformatting for
    you. To enable it, do the following:

     * install ``pre-commit`` using ``pip install pre-commit``

     * then run ``pre-commit install`` in the ``pylint`` root directory to enable the git hooks.

- Add a short entry to the ChangeLog describing the change, except for internal
  implementation only changes. Not usually required, but for changes other than small
  bugs we also add a couple of sentences in the release document for that release,
  (`What's New` section). For the release document we usually write some more details,
  and it is also a good place to offer examples on how the new change is supposed to work.

- Add a short entry in :file:`doc/whatsnew/VERSION.rst`.

- Add yourself to the `CONTRIBUTORS` file, flag yourself appropriately
  (if in doubt, you're a ``contributor``).

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

You can also use ``# +n: [`` with n an integer if the above syntax would make the line too long or other reasons::

    # +1: [empty-comment]
    #

If you need special control over Pylint's flag, you can also create a .rc file, which
can have sections of Pylint's configuration.

During development, it's sometimes helpful to run all functional tests in your
current environment in order to have faster feedback. Run from Pylint root directory with::

    python tests/test_functional.py

You can use all the options you would use for pytest, for example `-k "test_functional[len_checks]"`.
If required the .txt file can be re-generated from the current output by appending
`--update-functional-output` to the command line::

    python tests/test_functional.py --update-functional-output -k "test_functional[len_checks]"

.. _`Closing issues via commit messages`: https://help.github.com/articles/closing-issues-via-commit-messages/
.. _`About pull requests`: https://help.github.com/articles/using-pull-requests/
.. _tox: https://tox.readthedocs.io/en/latest/
.. _pytest: https://pytest.readthedocs.io/en/latest/
.. _black: https://github.com/ambv/black
.. _isort: https://github.com/timothycrosley/isort
.. _astroid: https://github.com/pycqa/astroid


Tips for Getting Started with Pylint Development
------------------------------------------------
* Read the :ref:`technical-reference`. It gives a short walk through of the pylint
  codebase and will help you identify where you will need to make changes
  for what you are trying to implement.

* :func:`astroid.extract_node` is your friend. Most checkers are AST based,
  so you will likely need to interact with :mod:`astroid`.
  A short example of how to use :func:`astroid.extract_node` is given
  :ref:`here <astroid_extract_node>`.

* When fixing a bug for a specific check, search the code for the warning
  message to find where the warning is raised,
  and therefore where the logic for that code exists.


Building the documentation
----------------------------

We use **tox** for building the documentation::

  $ tox -e docs
