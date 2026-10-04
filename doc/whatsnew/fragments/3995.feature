Support for the ``NO_COLOR`` and ``FORCE_COLOR`` environment variables has been added.
When running pylint, the reporter that writes to stdout is switched between ``text``
and ``colorized`` according to the requested mode.
The order is: ``NO_COLOR`` > ``FORCE_COLOR`` > ``--output-format=...``.

Closes #3995
