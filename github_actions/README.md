# GitHub Action for running pylint commands

Each time that new code is pushed into your repo, you can have a [pylint](https://docs.pylint.org) command automatically run.

Example workflow:
* Put the following text into a file named `.github/main.workflow` in your repo):
```hcl
workflow "on push" {
  on = "push"
  resolves = ["GitHub Action for pylint"]
}

action "GitHub Action for pylint" {
  uses = "PyCQA/pylint/github_actions@master"
  args = "pylint"
}
```
Or to add other pylint options to __args =__ above.

$ __pylint -h__
```
Usage:  pylint [options] modules_or_packages

  Check that module(s) satisfy a coding standard (and more !).

    pylint --help

  Display this help message and exit.

    pylint --help-msg <msg-id>[,<msg-id>]

  Display help messages about given message identifiers and exit.


Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  --long-help           more verbose help.

  Master:
    --rcfile=<file>     Specify a configuration file.
    --init-hook=<code>  Python code to execute, usually for sys.path
                        manipulation such as pygtk.require().
    -E, --errors-only   In error mode, checkers without error messages are
                        disabled and for others, only the ERROR messages are
                        displayed, and no reports are done by default.
    --py3k              In Python 3 porting mode, all checkers will be
                        disabled and only messages emitted by the porting
                        checker will be displayed.
    -v, --verbose       In verbose mode, extra non-checker-related info will
                        be displayed.
    --ignore=<file>[,<file>...]
                        Add files or directories to the blacklist. They should
                        be base names, not paths. [current: CVS]
    --ignore-patterns=<pattern>[,<pattern>...]
                        Add files or directories matching the regex patterns
                        to the blacklist. The regex matches against base
                        names, not paths. [current: none]
    --persistent=<y_or_n>
                        Pickle collected data for later comparisons. [current:
                        yes]
    --load-plugins=<modules>
                        List of plugins (as comma separated values of python
                        modules names) to load, usually to register additional
                        checkers. [current: none]
    -j <n-processes>, --jobs=<n-processes>
                        Use multiple processes to speed up Pylint. Specifying
                        0 will auto-detect the number of processors available
                        to use. [current: 1]
    --limit-inference-results=<number-of-results>
                        Control the amount of potential inferred values when
                        inferring a single object. This can help the
                        performance when dealing with large functions or
                        complex, nested conditions.  [current: 100]
    --extension-pkg-whitelist=<pkg[,pkg]>
                        A comma-separated list of package or module names from
                        where C extensions may be loaded. Extensions are
                        loading into the active Python interpreter and may run
                        arbitrary code. [current: none]
    --suggestion-mode=<yn>
                        When enabled, pylint would attempt to guess common
                        misconfiguration and emit user-friendly hints instead
                        of false-positive error messages. [current: yes]
    --exit-zero         Always return a 0 (non-error) status code, even if
                        lint errors are found. This is primarily useful in
                        continuous integration scripts.

  Commands:
    --help-msg=<msg-id>
                        Display a help message for the given message id and
                        exit. The value may be a comma separated list of
                        message ids.
    --list-msgs         Generate pylint's messages.
    --list-conf-levels  Generate pylint's confidence levels.
    --full-documentation
                        Generate pylint's full documentation.
    --generate-rcfile   Generate a sample configuration file according to the
                        current configuration. You can put other options
                        before this one to get them in the generated
                        configuration.

  Messages control:
    --confidence=<levels>
                        Only show warnings with the listed confidence levels.
                        Leave empty to show all. Valid levels: HIGH,
                        INFERENCE, INFERENCE_FAILURE, UNDEFINED. [current:
                        none]
    -e <msg ids>, --enable=<msg ids>
                        Enable the message, report, category or checker with
                        the given id(s). You can either give multiple
                        identifier separated by comma (,) or put this option
                        multiple time (only on the command line, not in the
                        configuration file where it should appear only once).
                        See also the "--disable" option for examples.
    -d <msg ids>, --disable=<msg ids>
                        Disable the message, report, category or checker with
                        the given id(s). You can either give multiple
                        identifiers separated by comma (,) or put this option
                        multiple times (only on the command line, not in the
                        configuration file where it should appear only once).
                        You can also use "--disable=all" to disable everything
                        first and then reenable specific checks. For example,
                        if you want to run only the similarities checker, you
                        can use "--disable=all --enable=similarities". If you
                        want to run only the classes checker, but have no
                        Warning level messages displayed, use "--disable=all
                        --enable=classes --disable=W".

  Reports:
    -f <format>, --output-format=<format>
                        Set the output format. Available formats are text,
                        parseable, colorized, json and msvs (visual studio).
                        You can also give a reporter class, e.g.
                        mypackage.mymodule.MyReporterClass. [current: text]
    -r <y_or_n>, --reports=<y_or_n>
                        Tells whether to display a full report or only the
                        messages. [current: no]
    --evaluation=<python_expression>
                        Python expression which should return a note less than
                        10 (10 is the highest note). You have access to the
                        variables errors warning, statement which respectively
                        contain the number of errors / warnings messages and
                        the total number of statements analyzed. This is used
                        by the global evaluation report (RP0004). [current:
                        10.0 - ((float(5 * error + warning + refactor +
                        convention) / statement) * 10)]
    -s <y_or_n>, --score=<y_or_n>
                        Activate the evaluation score. [current: yes]
    --msg-template=<template>
                        Template used to display messages. This is a python
                        new-style format string used to format the message
                        information. See doc for all details.
```
