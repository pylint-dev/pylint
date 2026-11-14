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
  example, the fix of ``use-a-generator`` turns
  ``any([apple > 2 for apple in basket])`` into
  ``any(apple > 2 for apple in basket)``. ``any`` then stops at the first big
  apple and never looks at the others, which is faster, but different if looking
  at an apple does something. Fixes that rely on inference are unsafe too,
  because inference can be wrong. Unsafe fixes are applied only when you ask for
  them:

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
   unfixable = ["use-a-generator"]

Only the enabled messages are fixed, so you can also fix a single kind of message:

.. code-block:: console

   pylint --disable=all --enable=use-a-generator --fix --unsafe-fixes fruits.py

``pylint --help-msg=<message>`` and the page of each message tell you whether
it can be fixed, and why its fix is safe or unsafe.

Fixes in the JSON output
------------------------

With ``--output-format=json2``, a message with a fix has a ``fix`` entry, for
safe, unsafe and suggested fixes alike. Editors can use it to offer a quick fix.

For example, for ``if any([apple > 2 for apple in basket]):`` on line 2:

.. code-block:: json

   {
       "symbol": "use-a-generator",
       "line": 2,
       "column": 3,
       "fix": {
           "description": "Use a generator instead of a list comprehension",
           "applicability": "unsafe",
           "edits": [
               {
                   "line": 2,
                   "column": 7,
                   "endLine": 2,
                   "endColumn": 8,
                   "newText": ""
               },
               {
                   "line": 2,
                   "column": 37,
                   "endLine": 2,
                   "endColumn": 38,
                   "newText": ""
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
