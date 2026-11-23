.. _linter-aggregators:

Installation with a linter aggregator
=====================================

Several tools bundle pylint with other linters, so you can get pylint as part of a
larger suite instead of installing and configuring it yourself:

- `Prospector <https://prospector.landscape.io/>`_ runs pylint along with other python
  analysis tools and merges everything into a single report.
- `Pylama <https://github.com/klen/pylama>`_ is a code audit tool wrapping pylint and
  several other python linters behind one command.
- `MegaLinter <https://megalinter.io/>`_ is a continuous integration oriented aggregator
  covering many languages, that `runs pylint out of the box
  <https://megalinter.io/latest/descriptors/python_pylint/>`_.
- `Super-Linter <https://github.com/super-linter/super-linter>`_ is a GitHub Action
  bundling linters for many languages, pylint included.

Code quality platforms such as `Codacy <https://www.codacy.com/>`_,
`Code Climate <https://codeclimate.com/>`_ and
`SonarQube <https://www.sonarsource.com/products/sonarqube/>`_ can also run pylint or
import its reports.

All those integrations are maintained by third parties: the pylint version they ship
and the options they expose are up to them, so refer to their own documentation.
