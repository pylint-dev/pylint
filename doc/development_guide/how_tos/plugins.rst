.. -*- coding: utf-8 -*-

.. _plugins:

How To Write a Pylint Plugin
============================

Pylint provides support for writing two types of extensions.
First, there is the concept of **checkers**,
which can be used for finding problems in your code.
Secondly, there is also the concept of **transform plugin**,
which represents a way through which the inference and
the capabilities of Pylint can be enhanced
and tailored to a particular module, library of framework.

In general, a plugin is a module which should have a function ``register``,
which takes an instance of ``pylint.lint.PyLinter`` as input.

A plugin can optionally define a function, ``load_configuration``,
which takes an instance of ``pylint.lint.PyLinter`` as input. This
function is called after Pylint loads configuration from configuration
file and command line interface. This function should load additional
plugin specific configuration to Pylint.

So a basic hello-world plugin can be implemented as:

.. sourcecode:: python

  # Inside hello_plugin.py
  from typing import TYPE_CHECKING

  import astroid

  if TYPE_CHECKING:
      from pylint.lint import PyLinter


  def register(linter: "PyLinter") -> None:
    """This required method auto registers the checker during initialization.

    :param linter: The linter to register the checker to.
    """
    print('Hello world')


We can run this plugin by placing this module in the PYTHONPATH and invoking
**pylint** as:

.. sourcecode:: bash

  $ pylint -E --load-plugins hello_plugin foo.py
  Hello world

We can extend hello-world plugin to ignore some specific names using
``load_configuration`` function:

.. sourcecode:: python

  # Inside hello_plugin.py
  from typing import TYPE_CHECKING

  import astroid

  if TYPE_CHECKING:
      from pylint.lint import PyLinter


  def register(linter: "PyLinter") -> None:
    """This required method auto registers the checker during initialization.

    :param linter: The linter to register the checker to.
    """
    print('Hello world')

  def load_configuration(linter):

    name_checker = get_checker(linter, NameChecker)
    # We consider as good names of variables Hello and World
    name_checker.config.good_names += ('Hello', 'World')

    # We ignore bin directory
    linter.config.black_list += ('bin',)

Depending if we need a **transform plugin** or a **checker**, this might not
be enough. For the former, this is enough to declare the module as a plugin,
but in the case of the latter, we need to register our checker with the linter
object, by calling the following inside the ``register`` function::

    linter.register_checker(OurChecker(linter))

For more information on writing a checker see :ref:`write_a_checker`.

.. _reporter_plugin_options:

Options for a reporter plugin
-----------------------------

A plugin can also add a reporter, with ``linter.register_reporter``. A reporter
can't define options itself. To give it options, register a checker that holds
the options and checks nothing. The reporter reads them from
``self.linter.config``:

.. sourcecode:: python

  # Inside severity_plugin.py
  from typing import TYPE_CHECKING

  from pylint.checkers import BaseChecker
  from pylint.reporters import BaseReporter

  if TYPE_CHECKING:
      from pylint.lint import PyLinter
      from pylint.message import Message
      from pylint.reporters.ureports.nodes import Section


  class SeverityOptions(BaseChecker):
      """Holds the options of SeverityReporter. It checks nothing."""

      name = "severity-reporter"
      options = (
          (
              "severity",
              {
                  "default": "MAJOR",
                  "type": "string",
                  "metavar": "<severity>",
                  "help": "Severity written before every message.",
              },
          ),
      )


  class SeverityReporter(BaseReporter):
      """Writes one line per message, starting with the severity."""

      name = "severity"

      def handle_message(self, msg: "Message") -> None:
          severity = self.linter.config.severity
          self.writeln(f"{severity} {msg.path}:{msg.line} {msg.symbol}")

      def _display(self, layout: "Section") -> None:
          pass


  def register(linter: "PyLinter") -> None:
      linter.register_checker(SeverityOptions(linter))
      linter.register_reporter(SeverityReporter)

The option then works like any other, on the command line:

.. sourcecode:: bash

  $ pylint --load-plugins=severity_plugin --output-format=severity --severity=MINOR my_module.py
  MINOR my_module.py:1 missing-module-docstring
  MINOR my_module.py:1 unused-import

or in a configuration file, in the section named after the checker:

.. sourcecode:: ini

  [SEVERITY-REPORTER]
  severity=CRITICAL
