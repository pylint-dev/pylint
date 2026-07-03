
.. _badge:

Show your usage
---------------

You can place this badge in your README to let others know your project uses pylint.

    .. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
        :target: https://github.com/pylint-dev/pylint

Use the badge in your project's README.md (or any other Markdown file)::

    [![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

Use the badge in your project's README.rst (or any other rst file)::

    .. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
        :target: https://github.com/pylint-dev/pylint


If you use GitHub Actions, and one of your CI workflows begins with "name: pylint", you
can use GitHub's `workflow status badges <https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge#using-the-workflow-file-name>`_
to show an up-to-date indication of whether pushes to your default branch pass pylint.
For more detailed information, check the documentation.
