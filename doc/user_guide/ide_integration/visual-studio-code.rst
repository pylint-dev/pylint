Integrate Pylint with Visual Studio Code
========================================

Command-line arguments and configuration files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See :ref:`Pylint command line arguments <run_command_line>` for general switches.
Command line arguments can be used to load Pylint plugins, such as that for Django:

::

    "python.linting.pylintArgs": ["--load-plugins", "pylint_django"]

Options can also be specified in a ``pylintrc`` or ``.pylintrc`` file in
the workspace folder, as described on :ref:`Pylint command line arguments <run_command_line>`/

To control which Pylint messages are shown, add the following contents
to an options file:

.. code:: ini

    [MESSAGES CONTROL]

    # Enable the message, report, category or checker with the given id(s). You can
    # either give multiple identifier separated by comma (,) or put this option
    # multiple time.
    #enable=

    # Disable the message, report, category or checker with the given id(s). You
    # can either give multiple identifier separated by comma (,) or put this option
    # multiple time (only on the command line, not in the configuration file where
    # it should appear only once).
    #disable=

Message category mapping
~~~~~~~~~~~~~~~~~~~~~~~~

The Python extension maps Pylint message categories to VS Code
categories through the following settings. If desired, change the
setting to change the mapping.

+----------------------+-----------------------------------+------------------+
| Pylint category      | Applicable setting                | VS Code category |
|                      | (python.linting.)                 | mapping          |
+======================+===================================+==================+
| convention           | pylintCategorySeverity.convention | Information      |
+----------------------+-----------------------------------+------------------+
| refactor             | pylintCategorySeverity.refactor   | Hint             |
+----------------------+-----------------------------------+------------------+
| warning              | pylintCategorySeverity.warning    | Warning          |
+----------------------+-----------------------------------+------------------+
| error                | pylintCategorySeverity.error      | Error            |
+----------------------+-----------------------------------+------------------+
| fatal                | pylintCategorySeverity.fatal      | Error            |
+----------------------+-----------------------------------+------------------+
