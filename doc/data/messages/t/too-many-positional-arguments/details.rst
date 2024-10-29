Good function signatures don’t have many positional parameters. For almost all
interfaces, comprehensibility suffers beyond a handful of arguments.

Positional arguments work well for cases where the the use cases are
self-evident, such as unittest's ``assertEqual(first, second, "assert msg")``
or ``zip(fruits, vegetables)``.

There are a few exceptions where four or more positional parameters make sense,
for example ``rgba(1.0, 0.5, 0.3, 1.0)``, because it uses a very well-known and
well-established convention, and using keywords all the time would be a waste
of time.
