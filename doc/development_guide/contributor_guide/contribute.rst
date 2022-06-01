.. -*- coding: utf-8 -*-

==============
 Contributing
==============

.. _repository:

Got a change for Pylint?  Below are a few steps you should take to make sure
your patch gets accepted:

- We recommend using Python 3.8 or higher for development of Pylint as it gives
  you access to the latest ``ast`` parser.
- Install the dev dependencies, see :ref:`contributor_install`.
- Use our test suite and write new tests, see :ref:`contributor_testing`.
- Add an entry to the change log describing the change in `doc/whatsnew/2/2.15/index.rst`
  (or ``doc/whatsnew/2/2.14/full.rst`` if the change needs backporting in 2.14).
  If necessary you can write details or offer examples on how the new change is supposed to work.

- Document your change, if it is a non-trivial one.

- If you used multiple emails or multiple names when contributing, add your mails
  and preferred name in the ``script/.contributors_aliases.json`` file.

- Write a comprehensive commit message

- Relate your change to an issue in the tracker if such an issue exists (see
  `Closing issues via commit messages`_ of the GitHub documentation for more
  information on this)

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

* ``astroid.extract_node`` is your friend. Most checkers are AST based,
  so you will likely need to interact with ``astroid``.
  A short example of how to use ``astroid.extract_node`` is given
  :ref:`here <astroid_extract_node>`.

* When fixing a bug for a specific check, search the code for the warning
  message to find where the warning is raised,
  and therefore where the logic for that code exists.

* When adding a new checker class you can use the :file:`get_unused_message_id_category.py`
  script in :file:`./script` to get a message id that is not used by
  any of the other checkers.

Building the documentation
----------------------------

You can use the makefile in the doc directory with ``make html`` to build the
documentation. To test smaller changes you can consider ``build-html``, which skips some checks but will be faster::

  $ cd doc
  $ make install-dependencies
  $ make build-html

We're reusing generated files for speed, use ``make clean`` when you want to start from scratch.

How to choose the target version ?
----------------------------------

Choose depending on the kind of change you're doing:

.. include:: patch_release.rst
.. include:: minor_release.rst
.. include:: major_release.rst
