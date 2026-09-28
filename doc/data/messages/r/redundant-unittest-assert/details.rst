Directly asserting a string literal will always pass, and comparing two
literals has an outcome that is already fixed by the source. The solution
is to test something that could fail, or not assert at all.

For assertions using ``assert`` there are similar messages: :ref:`assert-on-string-literal <assert-on-string-literal>` and :ref:`assert-on-tuple <assert-on-tuple>`.
