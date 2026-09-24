Two new ``BaseChecker`` methods supplement ``add_message``:

* ``add_message_at_node(msgid, node, args=None, confidence=UNDEFINED)``, a faster path
  for the common case using an AST node. Avoids doing check on optional parameters like
  ``line``/``col_offset``/``end_lineno``/``end_col_offset`` that ``add_message`` carries
  for non-AST callers.

* ``add_message_at_location(msgid, *, module: str, filepath = None, line = None,
  col_offset = None, end_lineno = None, end_col_offset = None,  args = None,
  confidence = UNDEFINED)`` emits a message at an explicit location instead of
  deriving it from a node. This is the only way to define module and filepath as
  ``add_message`` didn't provide them. Useful for cross-module findings like
  ``duplicate-code``.

Refs #10894
