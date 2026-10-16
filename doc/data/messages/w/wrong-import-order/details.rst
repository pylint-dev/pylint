Pylint uses ``isort`` to classify imports into standard library,
third-party, first-party, and local import groups.

``isort`` detects first-party imports by looking for packages relative to
the current working directory. As a result, running pylint from different
directories can change how the same import is classified.

For example, with the following project layout::

    project/
        src/
            my_package/
                __init__.py
                module.py

An import of ``my_package`` in ``module.py`` may be treated as first-party
when pylint is run from ``project/src``, but as third-party when pylint is
run from ``project``.

If this warning fires, or fails to fire, inconsistently between runs, set
``known-first-party`` in your pylint configuration to make the
classification deterministic::

    [tool.pylint.imports]
    known-first-party = ["my_package"]
