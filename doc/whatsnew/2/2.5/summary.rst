:Release: 2.5
:Date: 2020-04-27


Summary -- Release highlights
=============================


New checkers
============

* A new check ``isinstance-second-argument-not-valid-type`` was added.

   This check is emitted whenever **pylint** finds a call to the ``isinstance``
   function with a second argument that is not a type. Such code is likely
   unintended as it will cause a TypeError to be thrown at runtime error.

* A new check ``assert-on-string-literal`` was added.

   This check is emitted whenever **pylint** finds an assert statement
   with a string literal as its first argument. Such assert statements
   are probably unintended as they will always pass.

* A new check ``f-string-without-interpolation`` was added.

   This check is emitted whenever **pylint** detects the use of an
   f-string without having any interpolated values in it, which means
   that the f-string can be a normal string.

* Multiple checks for invalid return types of protocol functions were added:

   * ``invalid-bool-returned``: ``__bool__`` did not return a bool
   * ``invalid-index-returned``: ``__index__`` did not return an integer
   * ``invalid-repr-returned)``: ``__repr__`` did not return a string
   * ``invalid-str-returned)``: ``__str__`` did not return a string
   * ``invalid-bytes-returned)``: ``__bytes__`` did not return a string
   * ``invalid-hash-returned)``: ``__hash__`` did not return an integer
   * ``invalid-length-hint-returned)``: ``__length_hint__`` did not return a non-negative integer
   * ``invalid-format-returned)``: ``__format__`` did not return a string
   * ``invalid-getnewargs-returned)``: ``__getnewargs__`` did not return a tuple
   * ``invalid-getnewargs-ex-returned)``: ``__getnewargs_ex__`` did not return a tuple of the form (tuple, dict)

* A new check ``inconsistent-quotes`` was added.

   This check is emitted when quotes delimiters (``"`` and ``'``) are not used
   consistently throughout a module.  It allows avoiding unnecessary escaping,
   allowing, for example, ``"Don't error"`` in a module in which single-quotes
   otherwise delimit strings so that the single quote in ``Don't`` doesn't need to be escaped.

* A new check ``non-str-assignment-to-dunder-name`` was added to ensure that only strings are assigned to ``__name__`` attributes.


Other Changes
=============

* Configuration can be read from a setup.cfg or pyproject.toml file in the current directory.
  A setup.cfg must prepend pylintrc section names with ``pylint.``, for example ``[pylint.MESSAGES CONTROL]``.
  A pyproject.toml file must prepend section names with ``tool.pylint.``, for example ``[tool.pylint.'MESSAGES CONTROL']``.
  These files can also be passed in on the command line.

* Add new ``good-names-rgx`` and ``bad-names-rgx`` to enable permitting or disallowing of names via regular expressions

  To enable better handling of permitted/disallowed names, we added two new config options: good-names-rgxs: a comma-
  separated list of regexes, that if a name matches will be exempt from naming-checking. bad-names-rgxs: a comma-
  separated list of regexes, that if a name matches will be always marked as a disallowed name.

* Mutable ``collections.*`` are now flagged as dangerous defaults.

* Add new ``--fail-under`` flag for setting the threshold for the score to fail overall tests. If the score is over the fail-under threshold, pylint will complete SystemExit with value 0 to indicate no errors.

* Added a new option ``notes-rgx`` to make fixme warnings more flexible. Now either ``notes`` or ``notes-rgx`` option can be used to detect fixme warnings.

* Non-ASCII characters are now allowed by ``invalid-name``.

* ``pylint`` no longer emits ``invalid-name`` for non-constants found at module level.

  Pylint was considering all module level variables as constants, which is not what PEP 8 is actually mandating.

* A new check ``non-ascii-name`` was added to detect identifiers with non-ASCII characters.

* Overloaded typing functions no longer trigger ``no-self-use``, ``unused-argument``, ``missing-docstring`` and similar checks
  that assumed that overloaded functions are normal functions.

* ``python -m pylint`` can no longer be made to import files from the local directory.

* A new command ``--list-extensions`` was added.

  This command lists all extensions present in ``pylint.extensions``.

* Various false positives have been fixed which you can read more about in the Changelog files.

* Multiple types of string formatting are allowed in logging functions.

The ``logging-fstring-interpolation`` message has been brought back to allow
multiple types of string formatting to be used.
The type of formatting to use is chosen through enabling and disabling messages
rather than through the logging-format-style option.
The fstr value of the logging-format-style option is not valid.
