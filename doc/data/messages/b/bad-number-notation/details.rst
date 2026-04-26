There's 3 options associated with this message:

- ``number-notation-style``: can be left empty (allow all three, the default), ``scientific``, ``engineering``, or ``underscore``
- ``number-notation-threshold`` (default to 1e6)
- ``suggest-int-underscore`` (default no): suggest PEP 515 underscore grouping for integer literals above the threshold

Beyond notation form, the check also flags literals that float can't
represent faithfully — overflow (``1.5e500`` evaluates to ``math.inf``),
underflow (``1e-1000`` evaluates to ``0.0``), and literals exceeding the
~15 significant digit guarantee of ``float64``. For these cases the
suggestion list always includes ``decimal.Decimal("...")`` as a
precision-preserving alternative, alongside the runtime-equivalent
literal (``math.inf`` or ``0.0``) when the source is meant to convey
infinity or zero.
