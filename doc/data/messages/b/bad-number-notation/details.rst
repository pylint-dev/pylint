There's 3 options associated with this message:

- ``number-notation-style``: can be left empty (allow all three, the default), ``scientific``, ``engineering``, or ``underscore``
- ``number-notation-threshold`` (default to 1e6)
- ``suggest-int-underscore`` (default no): suggest PEP 515 underscore grouping for integer literals above the threshold

This check covers notation form only. Float-precision concerns —
overflow, underflow, more digits than float can represent — are handled
by the separate ``bad-float-precision`` check.
