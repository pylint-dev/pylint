.. -*- coding: utf-8 -*-

==============
 Contributing
==============

.. _repository:

Repository
----------

Pylint is developed using the git_ distributed version control system.

You can clone Pylint and its dependencies from ::

  git clone https://github.com/PyCQA/pylint
  git clone https://github.com/PyCQA/astroid

.. _git: https://git-scm.com/

Got a change for Pylint?  Below are a few steps you should take to make sure
your patch gets accepted. We recommend using Python 3.8 or higher for development
of Pylint as it gives you access to the latest ``ast`` parser.

- Test your code

  For more information on how to use our test suite and write new tests see :ref:`testing`.

- ``pylint`` uses black_ and isort_ among other Python auto-formatters.
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

- If you used multiple emails or multiple names when contributing, add your mails
  and preferred name in the ``script/.contributors_aliases.json`` file.

- Write a comprehensive commit message

- Relate your change to an issue in the tracker if such an issue exists (see
  `Closing issues via commit messages`_ of the GitHub documentation for more
  information on this)

- Document your change, if it is a non-trivial one.

- Send a pull request from GitHub (see `About pull requests`_ for more insight
  about this topic)

.. _`Closing issues via commit messages`: https://github.blog/2013-01-22-closing-issues-via-commit-messages/
.. _`About pull requests`: https://support.github.com/features/pull-requests
.. _tox: https://tox.readthedocs.io/en/latest/
.. _pytest: https://docs.pytest.org/en/latest/
.. _black: https://github.com/psf/black
.. _isort: https://github.com/PyCQA/isort
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

* When adding a new checker class you can use the :file:`get_unused_message_id_category.py`
  script in :file:`./script` to get a message id that is not used by
  any of the other checkers.

Building the documentation
----------------------------

We use **tox** for building the documentation::

  $ tox -e docs
