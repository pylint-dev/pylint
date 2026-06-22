When using ``raise ... from original_exception``, Python automatically displays
the original exception in the traceback with the message "The above exception
was the direct cause of the following exception". Including the original
exception in the new message is therefore redundant.

**With redundant message (bad):**

.. code-block:: python

    try:
        raise ValueError("Invalid format in config.yaml")
    except ValueError as e:
        raise RuntimeError(f"Failed to load config: {e}") from e

.. code-block:: text

    Traceback (most recent call last):
      File "example.py", line 2, in load_config
        raise ValueError("Invalid format in config.yaml")
    ValueError: Invalid format in config.yaml

    The above exception was the direct cause of the following exception:

    Traceback (most recent call last):
      File "example.py", line 4, in load_config
        raise RuntimeError(f"Failed to load config: {e}") from e
    RuntimeError: Failed to load config: Invalid format in config.yaml

**Without redundant message (good):**

.. code-block:: python

    try:
        raise ValueError("Invalid format in config.yaml")
    except ValueError as e:
        raise RuntimeError("Failed to load config") from e

.. code-block:: text

    Traceback (most recent call last):
      File "example.py", line 2, in load_config
        raise ValueError("Invalid format in config.yaml")
    ValueError: Invalid format in config.yaml

    The above exception was the direct cause of the following exception:

    Traceback (most recent call last):
      File "example.py", line 4, in load_config
        raise RuntimeError("Failed to load config") from e
    RuntimeError: Failed to load config

The exception chaining mechanism ensures all context is preserved without
message duplication.
