Trailing pragmas understood by other common tooling (``# type: ignore``,
``# noqa``, ``# pragma: no cover``) are no longer counted toward the line
length, so a line is not flagged as ``line-too-long`` solely because of such a
pragma. This mirrors the existing behaviour for Pylint's own ``# pylint:``
pragmas.

Closes #10172
