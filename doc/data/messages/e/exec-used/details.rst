The available methods and variables used in ``exec()`` may introduce a security hole.
You can restrict the use of these variables and methods by passing optional globals
and locals parameters (dictionaries) to the ``exec()`` method.

However, use of ``exec`` is still insecure. For example, consider the following call
that writes a file to the user's system:

.. code-block:: python

    exec("""\nwith open("file.txt", "w", encoding="utf-8") as file:\n file.write("# code as nefarious as imaginable")\n""")
