Support for ``NO_COLOR`` and ``FORCE_COLOR`` (and ``PY_COLORS``, as an alias to ``FORCE_COLOR``) environment variables has been added.
When running `pylint`, the reporter that reports to ``stdout`` will be modified according to the requested mode.
The order is: ``NO_COLOR`` > ``FORCE_COLOR``, ``PY_COLORS`` > ``--output=...``.

Closes #3995 (https://github.com/pylint-dev/pylint/issues/3995).
