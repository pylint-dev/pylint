Update ``pyreverse`` to differentiate between aggregations and compositions.
``pyreverse`` checks if it's an Instance or a Call of an object via method parameters (via type hints)
to decide if it's a composition or an aggregation.

Refs #6543
