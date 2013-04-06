
Pylint output
-------------

The default format for the output is raw text. You can change this by passing
pylint the ``--output-format=<value>`` option. Possible values are: parseable,
colorized, msvs (visual studio) and html.

There are several sections in pylint's output.

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

Following the analysis message, Pylint will display a set of reports,
each one focusing on a particular aspect of the project, such as number
of messages by categories, modules dependencies...

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

Also, a global evaluation for the code is computed.
