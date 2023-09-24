==============
 Contributing
==============

.. _repository:

Finding something to do
-----------------------

Want to contribute to pylint? There's a lot of things you can do.
Here's a list of links you can check depending on what you want to do:

- `Asking a question on discord`_, or `on github`_
- `Opening an issue`_
- `Making the documentation better`_
- `Making the error message better`_
- `Reproducing bugs and confirming that issues are valid`_
- `Investigating or debugging complicated issues`_
- `Designing or specifying a solution`_
- `Giving your opinion on ongoing discussion`_
- `Fixing bugs and crashes`_
- `Fixing false positives`_
- `Creating new features or fixing false negatives`_
- `Reviewing pull requests`_

.. _`Asking a question on discord`: https://discord.com/invite/qYxpadCgkx
.. _`on github`: https://github.com/pylint-dev/pylint/issues/new/choose
.. _`Opening an issue`: https://github.com/pylint-dev/pylint/issues/new?assignees=&labels=Needs+triage+%3Ainbox_tray%3A&template=BUG-REPORT.yml
.. _`Making the documentation better`: https://github.com/pylint-dev/pylint/issues?q=is%3Aopen+is%3Aissue+label%3A%22Documentation+%3Agreen_book%3A%22
.. _`Making the error message better`: https://github.com/pylint-dev/pylint/issues?q=is%3Aopen%20is%3Aissue%20project%3Apylint-dev%2Fpylint%2F4
.. _`Reproducing bugs and confirming that issues are valid`: https://github.com/pylint-dev/pylint/issues?q=is%3Aopen+is%3Aissue+label%3A%22Needs+reproduction+%3Amag%3A%22%2C%22Cannot+reproduce+%F0%9F%A4%B7%22
.. _`Investigating or debugging complicated issues`: https://github.com/pylint-dev/pylint/issues?q=is%3Aopen+is%3Aissue+label%3A%22Needs+investigation+%F0%9F%94%AC%22
.. _`Designing or specifying a solution`: https://github.com/pylint-dev/pylint/issues?q=is%3Aopen+is%3Aissue+label%3A%22Needs+design+proposal+%3Alock%3A%22%2C%22Needs+specification+%3Aclosed_lock_with_key%3A%22
.. _`Giving your opinion on ongoing discussion`: https://github.com/pylint-dev/pylint/issues?q=is%3Aopen+is%3Aissue+label%3A%22Needs+decision+%3Alock%3A%22
.. _`Fixing bugs and crashes`: https://github.com/pylint-dev/pylint/issues?q=is%3Aopen+is%3Aissue+label%3A%22Bug+%3Abeetle%3A%22%2C%22Crash+%F0%9F%92%A5%22
.. _`Fixing false positives`: https://github.com/pylint-dev/pylint/issues?q=is%3Aopen+is%3Aissue+label%3A%22False+Positive+%F0%9F%A6%9F%22
.. _`Creating new features or fixing false negatives`: https://github.com/pylint-dev/pylint/issues?q=is%3Aopen+is%3Aissue+label%3A%22False+Negative+%F0%9F%A6%8B%22%2C%22Enhancement+%E2%9C%A8%22
.. _`Reviewing pull requests`: https://github.com/pylint-dev/pylint/pulls?q=is%3Aopen+is%3Apr+label%3A%22Needs+review+%F0%9F%94%8D%22


If you are a pylint maintainer there's also:

- `Triaging issues`_
- `Labeling issues that do not have an actionable label yet`_
- `Preparing the next patch release`_
- `Checking stale pull requests status`_

.. _`Triaging issues`: https://github.com/pylint-dev/pylint/issues?q=is%3Aopen+is%3Aissue+label%3A%22Needs+triage+%3Ainbox_tray%3A%22
.. _`Labeling issues that do not have an actionable label yet`: https://github.com/pylint-dev/pylint/issues?q=is%3Aopen+is%3Aissue+-label%3A%22Needs+astroid+Brain+%F0%9F%A7%A0%22+-label%3A%22Needs+astroid+update%22+-label%3A%22Needs+backport%22+-label%3A%22Needs+decision+%3Alock%3A%22+-label%3A%22Needs+investigation+%F0%9F%94%AC%22+-label%3A%22Needs+PR%22+-label%3A%22Needs+reproduction+%3Amag%3A%22+-label%3A%22Needs+review+%F0%9F%94%8D%22+-label%3A%22Needs+triage+%3Ainbox_tray%3A%22+-label%3A%22Waiting+on+author%22+-label%3A%22Work+in+progress%22+-label%3AMaintenance+sort%3Aupdated-desc+-label%3A%22Needs+specification+%3Aclosed_lock_with_key%3A%22+-label%3A%22Needs+design+proposal+%3Alock%3A%22
.. _`Preparing the next patch release`: https://github.com/pylint-dev/pylint/issues?q=is%3Aopen+is%3Aissue+label%3A%22Needs+backport%22
.. _`Checking stale pull requests status`: https://github.com/pylint-dev/pylint/pulls?q=is%3Aopen+is%3Apr+label%3A%22Work+in+progress%22%2C%22Needs+astroid+update%22%2C%22Waiting+on+author%22


Creating a pull request
-----------------------

Got a change for Pylint?  Below are a few steps you should take to make sure
your patch gets accepted:

- You must use at least Python 3.8 for development of Pylint as it gives
  you access to the latest ``ast`` parser and some pre-commit hooks do not
  support python 3.7.

- Install the dev dependencies, see :ref:`contributor_install`.

- Use our test suite and write new tests, see :ref:`contributor_testing`.

.. keep this in sync with the description of PULL_REQUEST_TEMPLATE.md!

- Document your change, if it is a non-trivial one:

  * A maintainer might label the issue ``skip-news`` if the change does not need to be in the changelog.
  * Otherwise, create a news fragment with ``towncrier create <IssueNumber>.<type>`` which will be
    included in the changelog. ``<type>`` can be one of the types defined in `./towncrier.toml`.
    If necessary you can write details or offer examples on how the new change is supposed to work.
  * Generating the doc is done with ``tox -e docs``

- Send a pull request from GitHub (see `About pull requests`_ for more insight about this topic).

- Write comprehensive commit messages and/or a good description of what the PR does.
  Relate your change to an issue in the tracker if such an issue exists (see
  `Closing issues via commit messages`_ of the GitHub documentation for more
  information on this)

- Keep the change small, separate the consensual changes from the opinionated one.

  * Don't hesitate to open multiple PRs if the change requires it. If your review is so
    big it requires to actually plan and allocate time to review, it's more likely
    that it's going to go stale.
  * Maintainers might have multiple 5 to 10 minutes review windows per day, Say while waiting
    for their teapot to boil, or for their partner to recover from their hilarious nerdy joke,
    but only one full hour review time per week, if at all.

- If you used multiple emails or multiple names when contributing, add your mails
  and preferred name in the ``script/.contributors_aliases.json`` file.

.. _`Closing issues via commit messages`: https://github.blog/2013-01-22-closing-issues-via-commit-messages/
.. _`About pull requests`: https://support.github.com/features/pull-requests
.. _tox: https://tox.readthedocs.io/en/latest/
.. _pytest: https://docs.pytest.org/en/latest/
.. _black: https://github.com/psf/black
.. _isort: https://github.com/PyCQA/isort
.. _astroid: https://github.com/pylint-dev/astroid


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
