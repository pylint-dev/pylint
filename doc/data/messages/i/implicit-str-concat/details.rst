By default, detection of implicit string concatenation of line jumps is disabled.
Hence the following code will not trigger this rule:
Hence the following code will not trigger this rule:

.. code-block:: python

    SEQ = ('a', 'b'
                'c')

In order to detect this case, you must enable `check-str-concat-over-line-jumps`:

.. code-block:: toml

    [STRING_CONSTANT]
    check-str-concat-over-line-jumps = yes
