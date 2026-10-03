The available methods and variables used in ``exec()`` may introduce a security hole.
You can restrict the use of these variables and methods by passing optional globals
and locals parameters (dictionaries) to the ``exec()`` method.

However, use of ``exec()`` is still insecure if you allow some functions like
``__import__`` or ``open``. For example, consider the following call that writes a
file to the user's system and then execute code unrestrained by the ``allowed_globals``,
or ``allowed_locals`` parameters:

.. code-block:: python

    import textwrap


    def forbid_print(*args):
        raise ValueError("This is raised when a print is used")


    allowed_globals = {
        "__builtins__": {
            "__import__": __builtins__.__import__,
            "open": __builtins__.open,
            "print": forbid_print,
        }
    }

    exec(
        textwrap.dedent(
            """
        import textwrap

        with open("nefarious.py", "w") as f:
            f.write(textwrap.dedent('''
                def connive():
                    print("Here's some code as nefarious as imaginable")
            '''))

        import nefarious

        nefarious.connive()  # This will NOT raise a ValueError
        """
        ),
        allowed_globals,
    )


The import is used only for readability of the example in this case but it could
import a dangerous functions:

- ``subprocess.run('echo "print(\"Hello, World!\")" > nefarious.py'``
- ``pathlib.Path("nefarious.py").write_file("print(\"Hello, World!\")")``
- ``os.system('echo "print(\"Hello, World!\")" > nefarious.py')``
- ``logging.basicConfig(filename='nefarious.py'); logging.error('print("Hello, World!")')``
- etc.
