
Pylint output
-------------

Output options
''''''''''''''''''''''''''''
Output by default is written to stdout. The simplest way to output to a file is
with the ``--output=<filename>`` option.

The default format for the output is raw text. You can change this by passing
pylint the ``--output-format=<value>`` option. Possible values are: ``text``, ``json``,
``parseable``, ``colorized`` and ``msvs`` (for Visual Studio).

Multiple output formats can be used at the same time by passing
a comma-separated list of formats to ``--output-format``.
This output can be redirected to a file by giving a filename after a colon.

For example, to save a json report to ``somefile.json`` and print
a colorized report to stdout at the same time:
::

  --output-format=json:somefile.json,colorized

Finally, it is possible to invoke pylint programmatically with a
reporter initialized with a custom stream:

::

  pylint_output = StringIO() # Custom open stream
  reporter = text.TextReporter(pylint_output)
  Run(["test_file.py"], reporter=reporter, do_exit=False)
  print(pylint_output.getvalue()) # Retrieve and print the text report

The reporter can accept any stream object as as parameter. In this example,
the stream outputs to a file:

::

  with open("report.out", "w") as f:
    reporter = text.TextReporter(f)
    Run(["test_file.py"], reporter=reporter, do_exit=False)

This would be useful to capture pylint output in an open stream which
can be passed onto another program.

Custom message formats
''''''''''''''''''''''''''''

You can customize the exact way information are displayed using the
`--msg-template=<format string>` option. The `format string` uses the
`Python new format syntax`_ and the following fields are available :

path
    relative path to the file
abspath
    absolute path to the file
line
    line number
column
    column number
end_line
    line number of the end of the node
end_column
    column number of the end of the node
module
    module name
obj
    object within the module (if any)
msg
    text of the message
msg_id
    the message code (eg. I0011)
symbol
    symbolic name of the message (eg. locally-disabled)
C
    one letter indication of the message category
category
    fullname of the message category

For example, the former (pre 1.0) default format can be obtained with::

  pylint --msg-template='{msg_id}:{line:3d},{column}: {obj}: {msg}'

A few other examples:

* the default format::

    {path}:{line}:{column}: {msg_id}: {msg} ({symbol})

* Visual Studio compatible format (former 'msvs' output format)::

    {path}({line}): [{msg_id}{obj}] {msg}

* Parseable (Emacs and all, former 'parseable' output format) format::

    {path}:{line}: [{msg_id}({symbol}), {obj}] {msg}

The ``--msg-template`` option can only be combined with text-based reporters (``--output-format`` either unspecified or one of: parseable, colorized or msvs).
If both ``--output-format`` and ``--msg-template`` are specified, the ``--msg-template`` option will take precedence over the default line format defined by the reporter class.

If ``end_line`` or ``end_column`` are ``None``, they will be represented as an empty string
by the default ``TextReporter``.

.. _Python new format syntax: https://docs.python.org/2/library/string.html#formatstrings

Source code analysis section
''''''''''''''''''''''''''''

For each python module, Pylint will first display a few '*' characters followed
by the name of the module. Then, a number of messages with the following format:
::

  MESSAGE_TYPE: LINE_NUM:[OBJECT:] MESSAGE

You can get another output format, useful since it's recognized by
most editors or other development tools using the ``--output-format=parseable``
option.

The message type can be:

  * [I]nformational messages that Pylint emits (do not contribute to your analysis score)
  * [R]efactor for a "good practice" metric violation
  * [C]onvention for coding standard violation
  * [W]arning for stylistic problems, or minor programming issues
  * [E]rror for important programming issues (i.e. most probably bug)
  * [F]atal for errors which prevented further processing

Sometimes the line of code which caused the error is displayed with
a caret pointing to the error. This may be generalized in future
versions of Pylint.

Example (extracted from a run of Pylint on itself...):

::

  ************* Module pylint.checkers.format
  W: 50: Too long line (86/80)
  W:108: Operator not followed by a space
       print >>sys.stderr, 'Unable to match %r', line
              ^
  W:141: Too long line (81/80)
  W: 74:searchall: Unreachable code
  W:171:FormatChecker.process_tokens: Redefining built-in (type)
  W:150:FormatChecker.process_tokens: Too many local variables (20/15)
  W:150:FormatChecker.process_tokens: Too many branches (13/12)


Reports section
'''''''''''''''

Following the analysis message, Pylint can display a set of reports,
each one focusing on a particular aspect of the project, such as number
of messages by categories, modules dependencies. These features can
be enabled through the ``--reports=y`` option, or its shorthand
version ``-rn``.

For instance, the metrics report displays summaries gathered from the
current run.

  * the number of processed modules
  * for each module, the percentage of errors and warnings
  * the total number of errors and warnings
  * percentage of classes, functions and modules with docstrings, and
    a comparison from the previous run
  * percentage of classes, functions and modules with correct name
    (according to the coding standard), and a comparison from the
    previous run
  * a list of external dependencies found in the code, and where they appear

Score section
'''''''''''''

Finally, Pylint displays a global evaluation score for the code, rated out of a
maximum score of 10.0. This output can be suppressed through the ``--score=n``
option, or its shorthand version ``-sn``.

The evaluation formula can be overridden with the
``--evaluation=<python_expression>`` option.
