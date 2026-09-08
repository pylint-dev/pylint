.. _continuous-integration:

Installation with multiple interpreters
=======================================

Pylint runs inside a real Python interpreter. For most projects, the most reliable
way to check code that supports multiple Python versions is therefore to run Pylint
with the oldest Python version that the project supports. This makes the parser,
standard library, and import environment match the project's compatibility floor.

Sometimes the lint environment intentionally uses a newer interpreter. For example,
a pre-commit configuration might standardize all development tools on Python 3.13
while the project still supports Python 3.10. In that case, set ``py-version`` to
the oldest supported version::

    [tool.pylint.main]
    py-version = "3.10"

The equivalent command-line option is ``--py-version=3.10``. Without an explicit
value, ``py-version`` defaults to the version of Python that runs Pylint.

``py-version`` tells version-aware checks which Python features are available to
every supported interpreter. For example, it prevents Pylint from suggesting a
refactoring that requires a version newer than Python 3.10 and allows the
unsupported-version checker to report syntax that Python 3.10 cannot use. It does
not switch the interpreter that runs Pylint or emulate that interpreter's complete
standard library and runtime behavior, so running Pylint on the oldest supported
version remains preferable when practical.

Pylint does not guarantee that ``py-version`` will continue to support every
end-of-life Python release indefinitely. If current Pylint cannot analyse the
project's oldest supported release, the best available fallback may be an older
Pylint that still runs on that interpreter, without the fixes and features added
to later Pylint releases.
