By default, detection of implicit string concatenation of line jumps is disabled.
Hence the following code will not trigger this rule:

.. code-block:: python

    SEQ = ('a', 'b'
                'c')

In order to detect this case, you must enable `check-str-concat-over-line-jumps`:

.. code-block:: toml

    [STRING_CONSTANT]
    check-str-concat-over-line-jumps = true

However, the drawback of this setting is that it will trigger false positive
for string parameters passed on multiple lines in function calls:

.. code-block:: python

    warnings.warn(
        "rotate() is deprecated and will be removed in a future release. "
        "Use the rotation() context manager instead.",
        DeprecationWarning,
        stacklevel=3,
    )

No message will be emitted, though, if you clarify the wanted concatenation with parentheses:

.. code-block:: python

    warnings.warn(
        (
            "rotate() is deprecated and will be removed in a future release. "
            "Use the rotation() context manager instead."
        ),
        DeprecationWarning,
        stacklevel=3,
    )
