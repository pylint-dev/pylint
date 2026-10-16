.. _autofix:

Fixing messages automatically
=============================

Some messages come with a fix: pylint knows how to change the code so that the
message goes away. You can ask pylint to apply these fixes for you.

.. warning::

   ``--fix`` rewrites your files. Commit your work first, so you can look at
   the changes with ``git diff`` and undo them if you don't like them.

Applying the fixes
------------------

.. code-block:: console

   pylint --fix fruits.py

Pylint applies the fixes, lints the fixed files again (a fix can make a new
message appear, which may have its own fix), and stops when nothing changes.
Then it reports the messages that are left, as usual.

The fixes change as little code as possible and don't try to follow your code
style. Run your code formatter, like ``black`` or ``ruff format``, after
``pylint --fix``.

To see what would change without touching any file, print a diff:

.. code-block:: console

   pylint --fix-diff fruits.py

With ``--fix-diff``, the exit code is 1 when there is something to fix, and 0
otherwise.

Safe and unsafe fixes
---------------------

Every fix says how sure pylint is about it:

* A **safe** fix keeps the meaning of the code. ``--fix`` applies only these.
* An **unsafe** fix may change what the code does, or remove a comment. For
  example, replacing ``len(basket) == 0`` with ``not basket`` is right for a
  list, but not for every kind of object. Pylint also relies on inference to
  guess the type of ``basket``, and inference can be wrong. Unsafe fixes are
  applied only when you ask for them:

  .. code-block:: console

     pylint --fix --unsafe-fixes fruits.py

* Some fixes are only **suggestions**. They are never applied, but tools such as
  editors can show them to you.

A safe fix that would remove or replace a comment is always treated as unsafe.

When fixes are available but were not applied, pylint tells you how to apply
them at the end of its output.

Choosing which messages are fixed
---------------------------------

To never apply the fixes of some messages, list them in the ``unfixable``
option, by symbol or id:

.. code-block:: toml

   [tool.pylint.main]
   unfixable = ["consider-using-in"]

Only the enabled messages are fixed, so you can also fix a single kind of message:

.. code-block:: console

   pylint --disable=all --enable=consider-using-in --fix fruits.py

``pylint --help-msg=<message>`` tells you whether a message can be fixed.

Fixes in the JSON output
------------------------

With ``--output-format=json2``, a message with a fix has a ``fix`` entry, for
safe, unsafe and suggested fixes alike. Editors can use it to offer a quick fix.

.. code-block:: json

   {
       "symbol": "compare-length-to-zero",
       "line": 3,
       "column": 3,
       "fix": {
           "description": "Use 'not' to check if the collection is empty",
           "applicability": "unsafe",
           "edits": [
               {
                   "line": 3,
                   "column": 3,
                   "endLine": 3,
                   "endColumn": 22,
                   "newText": "not basket"
               }
           ]
       }
   }

Lines start at 1. Columns use the same unit as the ``column`` of the message:
they count UTF-8 bytes from the start of the line. All the edits of a fix must
be applied together.

Limitations
-----------

* Code read from the standard input (``--from-stdin``) cannot be fixed.
* A file with a syntax error is never fixed.
* If the fixes of a file produce invalid code, pylint leaves the file unchanged
  and asks you to report the bug.
