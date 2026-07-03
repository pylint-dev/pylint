One of your pylint plugins cannot be loaded. There's nothing to change in
your code, but your pylint configuration or installation has an issue.

For example, there might be a typo. The following config::

    [MAIN]
    load-plugins = pylint.extensions.bad_biultin

Should be::

    [MAIN]
    load-plugins = pylint.extensions.bad_builtin

Or the plugin you added is not importable in your environment.
