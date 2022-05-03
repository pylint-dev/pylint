This message applies to callables of Python's stdlib which can be replaced by a ``with`` statement.
It is suppressed in the following cases:

- the call is located inside a context manager
- the call result is returned from the enclosing function
- the call result is used in a ``with`` statement itself
