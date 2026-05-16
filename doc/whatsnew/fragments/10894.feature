A new ``BaseChecker.add_message_at_location`` method lets checkers emit a message at an explicit location (``module``, ``filepath``, ``line``, ``col_offset``, ...) instead of deriving it from an AST node. This is useful for cross-module findings like ``duplicate-code``.

Refs #10894
