Startup and the Linter Class
----------------------------
The two main classes in :mod:`pylint.lint` are
:class:`.pylint.lint.Run` and :class:`.pylint.lint.PyLinter`.

The :class:`.pylint.lint.Run` object is responsible for starting up pylint.
It does some basic checking of the given command line options to
find the initial hook to run,
find the config file to use,
and find which plugins have been specified.
It can then create the master :class:`.pylint.lint.PyLinter` instance
and initialise it with the config file and plugins that were discovered
when preprocessing the command line options.
Finally the :class:`.pylint.lint.Run` object launches any child linters
for parallel jobs, and starts the linting process.

The :class:`.pylint.lint.PyLinter` is responsible for coordinating the
linting process.
It parses the configuration and provides it for the checkers and other plugins,
it handles the messages emitted by the checkers,
it handles the output reporting,
and it launches the checkers.
