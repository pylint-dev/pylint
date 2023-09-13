One of your options is not recognized. There's nothing to change in
your code, but your pylint configuration or the way you launch
pylint needs to be modified.

For example you might be launching pylint with the following ``toml`` configuration::

    [tool.pylint]
    jars = "10"

When the following should be used::

    [tool.pylint]
    jobs = "10"

This warning was released in pylint 2.14: bad options were silently failing before.
