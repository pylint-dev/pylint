The available methods and variables used in ``exec()`` may introduce a security hole.
You can restrict the use of these variables and methods by passing optional globals
and locals parameters (dictionaries) to the ``exec()`` method.

However, use of ``exec`` is still insecure. For example, consider the following call
that writes a file to the user's system and then execute code unrestrained by the ``allowed_globals``,
or ``allowed_locals`` parameters:

.. code-block:: python

    import textwrap
    allowed_globals = {"__builtins__": None}
    exec(
        textwrap.dedent("""
        import textwrap

        with open("nefarious.py", "w") as f:
            f.write(textwrap.dedent('''
                def connive():
                    print("Here's some code as nefarious as imaginable")
            '''))

        import nefarious
        nefarious.connive()
        """),
        # allowed_globals,
    )
