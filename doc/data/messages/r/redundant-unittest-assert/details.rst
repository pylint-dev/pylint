Directly asserting a string literal will always pass. The solution is to
test something that could fail, or not assert at all.

For assertions using ``assert`` there are similar messages: :ref:`assert-on-string-literal` and :ref:`assert-on-tuple`.
