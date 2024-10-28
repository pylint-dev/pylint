Good APIs don’t have many positional parameters. For almost all API,
comprehensibility suffers beyond a handful of arguments.

Positional arguments work well for cases where the the use cases are
self-evident, such as unittest's ``assertEqual(first, second, "assert msg")``
or ``enumerate(fruits, 4)`` (The second arg of ``enumerate`` is seldom used,
so maybe you'd already prefer to read ``enumerate(fruits, start=4)``).
There are few exceptions where 4 or more positional parameters make sense,
for example ``rgba(1.0, 0.5, 0.3, 1.0)`` because it uses a very well known and
well established convention and using keywords all the time would be a waste
of time.
