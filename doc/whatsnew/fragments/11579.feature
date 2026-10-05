``dangerous-default-value`` now also reports function calls used as default argument values,
for example ``def f(key=uuid4())``. Default values are evaluated once, when the function is
defined, not on every call. Calls to immutable builtins are allowed and the new
``allowed-default-calls`` option extends the list.

Refs #11579
