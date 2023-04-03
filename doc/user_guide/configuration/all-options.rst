

.. This file is auto-generated. Make any changes to the associated
.. docs extension in 'doc/exts/pylint_options.py'.

.. _all-options:

Standard Checkers
^^^^^^^^^^^^^^^^^


.. _main-options:

``Main`` **Checker**
--------------------
--analyse-fallback-blocks
"""""""""""""""""""""""""
*Analyse import fallback blocks. This can be used to support both Python 2 and 3 compatible code, which means that the block might have code that exists only in one or another interpreter, leading to false positives when analysed.*

**Default:**  ``False``


--clear-cache-post-run
""""""""""""""""""""""
*Clear in-memory caches upon conclusion of linting. Useful if running pylint in a server-like mode.*

**Default:**  ``False``


--confidence
""""""""""""
*Only show warnings with the listed confidence levels. Leave empty to show all. Valid levels: HIGH, CONTROL_FLOW, INFERENCE, INFERENCE_FAILURE, UNDEFINED.*

**Default:**  ``['HIGH', 'CONTROL_FLOW', 'INFERENCE', 'INFERENCE_FAILURE', 'UNDEFINED']``


--disable
"""""""""
*Disable the message, report, category or checker with the given id(s). You can either give multiple identifiers separated by comma (,) or put this option multiple times (only on the command line, not in the configuration file where it should appear only once). You can also use "--disable=all" to disable everything first and then re-enable specific checks. For example, if you want to run only the similarities checker, you can use "--disable=all --enable=similarities". If you want to run only the classes checker, but have no Warning level messages displayed, use "--disable=all --enable=classes --disable=W".*

**Default:**  ``()``


--enable
""""""""
*Enable the message, report, category or checker with the given id(s). You can either give multiple identifier separated by comma (,) or put this option multiple time (only on the command line, not in the configuration file where it should appear only once). See also the "--disable" option for examples.*

**Default:**  ``()``


--evaluation
""""""""""""
*Python expression which should return a score less than or equal to 10. You have access to the variables 'fatal', 'error', 'warning', 'refactor', 'convention', and 'info' which contain the number of messages in each category, as well as 'statement' which is the total number of statements analyzed. This score is used by the global evaluation report (RP0004).*

**Default:**  ``max(0, 0 if fatal else 10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10))``


--exit-zero
"""""""""""
*Always return a 0 (non-error) status code, even if lint errors are found. This is primarily useful in continuous integration scripts.*

**Default:**  ``False``


--extension-pkg-allow-list
""""""""""""""""""""""""""
*A comma-separated list of package or module names from where C extensions may be loaded. Extensions are loading into the active Python interpreter and may run arbitrary code.*

**Default:**  ``[]``


--extension-pkg-whitelist
"""""""""""""""""""""""""
*A comma-separated list of package or module names from where C extensions may be loaded. Extensions are loading into the active Python interpreter and may run arbitrary code. (This is an alternative name to extension-pkg-allow-list for backward compatibility.)*

**Default:**  ``[]``


--fail-on
"""""""""
*Return non-zero exit code if any of these messages/categories are detected, even if score is above --fail-under value. Syntax same as enable. Messages specified are enabled, while categories only check already-enabled messages.*

**Default:** ``""``


--fail-under
""""""""""""
*Specify a score threshold under which the program will exit with error.*

**Default:**  ``10``


--from-stdin
""""""""""""
*Interpret the stdin as a python script, whose filename needs to be passed as the module_or_package argument.*

**Default:**  ``False``


--ignore
""""""""
*Files or directories to be skipped. They should be base names, not paths.*

**Default:**  ``('CVS',)``


--ignore-paths
""""""""""""""
*Add files or directories matching the regular expressions patterns to the ignore-list. The regex matches against paths and can be in Posix or Windows format. Because '\\' represents the directory delimiter on Windows systems, it can't be used as an escape character.*

**Default:**  ``[]``


--ignore-patterns
"""""""""""""""""
*Files or directories matching the regular expression patterns are skipped. The regex matches against base names, not paths. The default value ignores Emacs file locks*

**Default:**  ``(re.compile('^\\.#'),)``


--ignored-modules
"""""""""""""""""
*List of module names for which member attributes should not be checked (useful for modules/projects where namespaces are manipulated during runtime and thus existing member attributes cannot be deduced by static analysis). It supports qualified module names, as well as Unix pattern matching.*

**Default:**  ``()``


--jobs
""""""
*Use multiple processes to speed up Pylint. Specifying 0 will auto-detect the number of processors available to use, and will cap the count on Windows to avoid hangs.*

**Default:**  ``1``


--limit-inference-results
"""""""""""""""""""""""""
*Control the amount of potential inferred values when inferring a single object. This can help the performance when dealing with large functions or complex, nested conditions.*

**Default:**  ``100``


--load-plugins
""""""""""""""
*List of plugins (as comma separated values of python module names) to load, usually to register additional checkers.*

**Default:**  ``()``


--msg-template
""""""""""""""
*Template used to display messages. This is a python new-style format string used to format the message information. See doc for all details.*

**Default:** ``""``


--output-format
"""""""""""""""
*Set the output format. Available formats are text, parseable, colorized, json and msvs (visual studio). You can also give a reporter class, e.g. mypackage.mymodule.MyReporterClass.*

**Default:**  ``text``


--persistent
""""""""""""
*Pickle collected data for later comparisons.*

**Default:**  ``True``


--py-version
""""""""""""
*Minimum Python version to use for version dependent checks. Will default to the version used to run pylint.*

**Default:**  ``(3, 10)``


--recursive
"""""""""""
*Discover python modules and packages in the file system subtree.*

**Default:**  ``False``


--reports
"""""""""
*Tells whether to display a full report or only the messages.*

**Default:**  ``False``


--score
"""""""
*Activate the evaluation score.*

**Default:**  ``True``


--source-roots
""""""""""""""
*Add paths to the list of the source roots. Supports globbing patterns. The source root is an absolute path or a path relative to the current working directory used to determine a package namespace for modules located under the source root.*

**Default:**  ``()``


--suggestion-mode
"""""""""""""""""
*When enabled, pylint would attempt to guess common misconfiguration and emit user-friendly hints instead of false-positive error messages.*

**Default:**  ``True``


--unsafe-load-any-extension
"""""""""""""""""""""""""""
*Allow loading of arbitrary C extensions. Extensions are imported into the active Python interpreter and may run arbitrary code.*

**Default:**  ``False``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.main]
   analyse-fallback-blocks = false

   clear-cache-post-run = false

   confidence = ["HIGH", "CONTROL_FLOW", "INFERENCE", "INFERENCE_FAILURE", "UNDEFINED"]

   disable = ["consider-using-augmented-assign"]

   enable = []

   evaluation = "max(0, 0 if fatal else 10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10))"

   exit-zero = false

   extension-pkg-allow-list = []

   extension-pkg-whitelist = []

   fail-on = []

   fail-under = 10

   from-stdin = false

   ignore = ["CVS"]

   ignore-paths = []

   ignore-patterns = ["^\\.#"]

   ignored-modules = []

   jobs = 1

   limit-inference-results = 100

   load-plugins = []

   msg-template = ""

   # output-format =

   persistent = true

   py-version = [3, 10]

   recursive = false

   reports = false

   score = true

   source-roots = []

   suggestion-mode = true

   unsafe-load-any-extension = false



.. raw:: html

   </details>


.. _basic-options:

``Basic`` **Checker**
---------------------
--argument-naming-style
"""""""""""""""""""""""
*Naming style matching correct argument names.*

**Default:**  ``snake_case``


--argument-rgx
""""""""""""""
*Regular expression matching correct argument names. Overrides argument-naming-style. If left empty, argument names will be checked with the set naming style.*

**Default:**  ``None``


--attr-naming-style
"""""""""""""""""""
*Naming style matching correct attribute names.*

**Default:**  ``snake_case``


--attr-rgx
""""""""""
*Regular expression matching correct attribute names. Overrides attr-naming-style. If left empty, attribute names will be checked with the set naming style.*

**Default:**  ``None``


--bad-names
"""""""""""
*Bad variable names which should always be refused, separated by a comma.*

**Default:**  ``('foo', 'bar', 'baz', 'toto', 'tutu', 'tata')``


--bad-names-rgxs
""""""""""""""""
*Bad variable names regexes, separated by a comma. If names match any regex, they will always be refused*

**Default:** ``""``


--class-attribute-naming-style
""""""""""""""""""""""""""""""
*Naming style matching correct class attribute names.*

**Default:**  ``any``


--class-attribute-rgx
"""""""""""""""""""""
*Regular expression matching correct class attribute names. Overrides class-attribute-naming-style. If left empty, class attribute names will be checked with the set naming style.*

**Default:**  ``None``


--class-const-naming-style
""""""""""""""""""""""""""
*Naming style matching correct class constant names.*

**Default:**  ``UPPER_CASE``


--class-const-rgx
"""""""""""""""""
*Regular expression matching correct class constant names. Overrides class-const-naming-style. If left empty, class constant names will be checked with the set naming style.*

**Default:**  ``None``


--class-naming-style
""""""""""""""""""""
*Naming style matching correct class names.*

**Default:**  ``PascalCase``


--class-rgx
"""""""""""
*Regular expression matching correct class names. Overrides class-naming-style. If left empty, class names will be checked with the set naming style.*

**Default:**  ``None``


--const-naming-style
""""""""""""""""""""
*Naming style matching correct constant names.*

**Default:**  ``UPPER_CASE``


--const-rgx
"""""""""""
*Regular expression matching correct constant names. Overrides const-naming-style. If left empty, constant names will be checked with the set naming style.*

**Default:**  ``None``


--docstring-min-length
""""""""""""""""""""""
*Minimum line length for functions/classes that require docstrings, shorter ones are exempt.*

**Default:**  ``-1``


--function-naming-style
"""""""""""""""""""""""
*Naming style matching correct function names.*

**Default:**  ``snake_case``


--function-rgx
""""""""""""""
*Regular expression matching correct function names. Overrides function-naming-style. If left empty, function names will be checked with the set naming style.*

**Default:**  ``None``


--good-names
""""""""""""
*Good variable names which should always be accepted, separated by a comma.*

**Default:**  ``('i', 'j', 'k', 'ex', 'Run', '_')``


--good-names-rgxs
"""""""""""""""""
*Good variable names regexes, separated by a comma. If names match any regex, they will always be accepted*

**Default:** ``""``


--include-naming-hint
"""""""""""""""""""""
*Include a hint for the correct naming format with invalid-name.*

**Default:**  ``False``


--inlinevar-naming-style
""""""""""""""""""""""""
*Naming style matching correct inline iteration names.*

**Default:**  ``any``


--inlinevar-rgx
"""""""""""""""
*Regular expression matching correct inline iteration names. Overrides inlinevar-naming-style. If left empty, inline iteration names will be checked with the set naming style.*

**Default:**  ``None``


--method-naming-style
"""""""""""""""""""""
*Naming style matching correct method names.*

**Default:**  ``snake_case``


--method-rgx
""""""""""""
*Regular expression matching correct method names. Overrides method-naming-style. If left empty, method names will be checked with the set naming style.*

**Default:**  ``None``


--module-naming-style
"""""""""""""""""""""
*Naming style matching correct module names.*

**Default:**  ``snake_case``


--module-rgx
""""""""""""
*Regular expression matching correct module names. Overrides module-naming-style. If left empty, module names will be checked with the set naming style.*

**Default:**  ``None``


--name-group
""""""""""""
*Colon-delimited sets of names that determine each other's naming style when the name regexes allow several styles.*

**Default:**  ``()``


--no-docstring-rgx
""""""""""""""""""
*Regular expression which should only match function or class names that do not require a docstring.*

**Default:**  ``re.compile('^_')``


--property-classes
""""""""""""""""""
*List of decorators that produce properties, such as abc.abstractproperty. Add to this list to register other decorators that produce valid properties. These decorators are taken in consideration only for invalid-name.*

**Default:**  ``('abc.abstractproperty',)``


--typealias-rgx
"""""""""""""""
*Regular expression matching correct type alias names. If left empty, type alias names will be checked with the set naming style.*

**Default:**  ``None``


--typevar-rgx
"""""""""""""
*Regular expression matching correct type variable names. If left empty, type variable names will be checked with the set naming style.*

**Default:**  ``None``


--variable-naming-style
"""""""""""""""""""""""
*Naming style matching correct variable names.*

**Default:**  ``snake_case``


--variable-rgx
""""""""""""""
*Regular expression matching correct variable names. Overrides variable-naming-style. If left empty, variable names will be checked with the set naming style.*

**Default:**  ``None``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.basic]
   argument-naming-style = "snake_case"

   # argument-rgx =

   attr-naming-style = "snake_case"

   # attr-rgx =

   bad-names = ["foo", "bar", "baz", "toto", "tutu", "tata"]

   bad-names-rgxs = []

   class-attribute-naming-style = "any"

   # class-attribute-rgx =

   class-const-naming-style = "UPPER_CASE"

   # class-const-rgx =

   class-naming-style = "PascalCase"

   # class-rgx =

   const-naming-style = "UPPER_CASE"

   # const-rgx =

   docstring-min-length = -1

   function-naming-style = "snake_case"

   # function-rgx =

   good-names = ["i", "j", "k", "ex", "Run", "_"]

   good-names-rgxs = []

   include-naming-hint = false

   inlinevar-naming-style = "any"

   # inlinevar-rgx =

   method-naming-style = "snake_case"

   # method-rgx =

   module-naming-style = "snake_case"

   # module-rgx =

   name-group = []

   no-docstring-rgx = "^_"

   property-classes = ["abc.abstractproperty"]

   # typealias-rgx =

   # typevar-rgx =

   variable-naming-style = "snake_case"

   # variable-rgx =



.. raw:: html

   </details>


.. _classes-options:

``Classes`` **Checker**
-----------------------
--check-protected-access-in-special-methods
"""""""""""""""""""""""""""""""""""""""""""
*Warn about protected attribute access inside special methods*

**Default:**  ``False``


--defining-attr-methods
"""""""""""""""""""""""
*List of method names used to declare (i.e. assign) instance attributes.*

**Default:**  ``('__init__', '__new__', 'setUp', 'asyncSetUp', '__post_init__')``


--exclude-protected
"""""""""""""""""""
*List of member names, which should be excluded from the protected access warning.*

**Default:**  ``('_asdict', '_fields', '_replace', '_source', '_make', 'os._exit')``


--valid-classmethod-first-arg
"""""""""""""""""""""""""""""
*List of valid names for the first argument in a class method.*

**Default:**  ``('cls',)``


--valid-metaclass-classmethod-first-arg
"""""""""""""""""""""""""""""""""""""""
*List of valid names for the first argument in a metaclass class method.*

**Default:**  ``('mcs',)``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.classes]
   check-protected-access-in-special-methods = false

   defining-attr-methods = ["__init__", "__new__", "setUp", "asyncSetUp", "__post_init__"]

   exclude-protected = ["_asdict", "_fields", "_replace", "_source", "_make", "os._exit"]

   valid-classmethod-first-arg = ["cls"]

   valid-metaclass-classmethod-first-arg = ["mcs"]



.. raw:: html

   </details>


.. _design-options:

``Design`` **Checker**
----------------------
--exclude-too-few-public-methods
""""""""""""""""""""""""""""""""
*List of regular expressions of class ancestor names to ignore when counting public methods (see R0903)*

**Default:**  ``[]``


--ignored-parents
"""""""""""""""""
*List of qualified class names to ignore when counting class parents (see R0901)*

**Default:**  ``()``


--max-args
""""""""""
*Maximum number of arguments for function / method.*

**Default:**  ``5``


--max-attributes
""""""""""""""""
*Maximum number of attributes for a class (see R0902).*

**Default:**  ``7``


--max-bool-expr
"""""""""""""""
*Maximum number of boolean expressions in an if statement (see R0916).*

**Default:**  ``5``


--max-branches
""""""""""""""
*Maximum number of branch for function / method body.*

**Default:**  ``12``


--max-complexity
""""""""""""""""
*McCabe complexity cyclomatic threshold*

**Default:**  ``10``


--max-locals
""""""""""""
*Maximum number of locals for function / method body.*

**Default:**  ``15``


--max-parents
"""""""""""""
*Maximum number of parents for a class (see R0901).*

**Default:**  ``7``


--max-public-methods
""""""""""""""""""""
*Maximum number of public methods for a class (see R0904).*

**Default:**  ``20``


--max-returns
"""""""""""""
*Maximum number of return / yield for function / method body.*

**Default:**  ``6``


--max-statements
""""""""""""""""
*Maximum number of statements in function / method body.*

**Default:**  ``50``


--min-public-methods
""""""""""""""""""""
*Minimum number of public methods for a class (see R0903).*

**Default:**  ``2``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.design]
   exclude-too-few-public-methods = []

   ignored-parents = []

   max-args = 5

   max-attributes = 7

   max-bool-expr = 5

   max-branches = 12

   max-complexity = 10

   max-locals = 15

   max-parents = 7

   max-public-methods = 20

   max-returns = 6

   max-statements = 50

   min-public-methods = 2



.. raw:: html

   </details>


.. _exceptions-options:

``Exceptions`` **Checker**
--------------------------
--overgeneral-exceptions
""""""""""""""""""""""""
*Exceptions that will emit a warning when caught.*

**Default:**  ``('builtins.BaseException', 'builtins.Exception')``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.exceptions]
   overgeneral-exceptions = ["builtins.BaseException", "builtins.Exception"]



.. raw:: html

   </details>


.. _format-options:

``Format`` **Checker**
----------------------
--expected-line-ending-format
"""""""""""""""""""""""""""""
*Expected format of line ending, e.g. empty (any line ending), LF or CRLF.*

**Default:** ``""``


--ignore-long-lines
"""""""""""""""""""
*Regexp for a line that is allowed to be longer than the limit.*

**Default:**  ``^\s*(# )?<?https?://\S+>?$``


--indent-after-paren
""""""""""""""""""""
*Number of spaces of indent required inside a hanging or continued line.*

**Default:**  ``4``


--indent-string
"""""""""""""""
*String used as indentation unit. This is usually "    " (4 spaces) or "\t" (1 tab).*

**Default:**  ``    ``


--max-line-length
"""""""""""""""""
*Maximum number of characters on a single line.*

**Default:**  ``100``


--max-module-lines
""""""""""""""""""
*Maximum number of lines in a module.*

**Default:**  ``1000``


--single-line-class-stmt
""""""""""""""""""""""""
*Allow the body of a class to be on the same line as the declaration if body contains single statement.*

**Default:**  ``False``


--single-line-if-stmt
"""""""""""""""""""""
*Allow the body of an if to be on the same line as the test if there is no else.*

**Default:**  ``False``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.format]
   expected-line-ending-format = ""

   ignore-long-lines = "^\\s*(# )?<?https?://\\S+>?$"

   indent-after-paren = 4

   indent-string = "    "

   max-line-length = 100

   max-module-lines = 1000

   single-line-class-stmt = false

   single-line-if-stmt = false



.. raw:: html

   </details>


.. _imports-options:

``Imports`` **Checker**
-----------------------
--allow-any-import-level
""""""""""""""""""""""""
*List of modules that can be imported at any level, not just the top level one.*

**Default:**  ``()``


--allow-reexport-from-package
"""""""""""""""""""""""""""""
*Allow explicit reexports by alias from a package __init__.*

**Default:**  ``False``


--allow-wildcard-with-all
"""""""""""""""""""""""""
*Allow wildcard imports from modules that define __all__.*

**Default:**  ``False``


--deprecated-modules
""""""""""""""""""""
*Deprecated modules which should not be used, separated by a comma.*

**Default:**  ``()``


--ext-import-graph
""""""""""""""""""
*Output a graph (.gv or any supported image format) of external dependencies to the given file (report RP0402 must not be disabled).*

**Default:** ``""``


--import-graph
""""""""""""""
*Output a graph (.gv or any supported image format) of all (i.e. internal and external) dependencies to the given file (report RP0402 must not be disabled).*

**Default:** ``""``


--int-import-graph
""""""""""""""""""
*Output a graph (.gv or any supported image format) of internal dependencies to the given file (report RP0402 must not be disabled).*

**Default:** ``""``


--known-standard-library
""""""""""""""""""""""""
*Force import order to recognize a module as part of the standard compatibility libraries.*

**Default:**  ``()``


--known-third-party
"""""""""""""""""""
*Force import order to recognize a module as part of a third party library.*

**Default:**  ``('enchant',)``


--preferred-modules
"""""""""""""""""""
*Couples of modules and preferred modules, separated by a comma.*

**Default:**  ``()``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.imports]
   allow-any-import-level = []

   allow-reexport-from-package = false

   allow-wildcard-with-all = false

   deprecated-modules = []

   ext-import-graph = ""

   import-graph = ""

   int-import-graph = ""

   known-standard-library = []

   known-third-party = ["enchant"]

   preferred-modules = []



.. raw:: html

   </details>


.. _logging-options:

``Logging`` **Checker**
-----------------------
--logging-format-style
""""""""""""""""""""""
*The type of string formatting that logging methods do. `old` means using % formatting, `new` is for `{}` formatting.*

**Default:**  ``old``


--logging-modules
"""""""""""""""""
*Logging modules to check that the string format arguments are in logging function parameter format.*

**Default:**  ``('logging',)``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.logging]
   logging-format-style = "old"

   logging-modules = ["logging"]



.. raw:: html

   </details>


.. _method_args-options:

``Method_args`` **Checker**
---------------------------
--timeout-methods
"""""""""""""""""
*List of qualified names (i.e., library.method) which require a timeout parameter e.g. 'requests.api.get,requests.api.post'*

**Default:**  ``('requests.api.delete', 'requests.api.get', 'requests.api.head', 'requests.api.options', 'requests.api.patch', 'requests.api.post', 'requests.api.put', 'requests.api.request')``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.method_args]
   timeout-methods = ["requests.api.delete", "requests.api.get", "requests.api.head", "requests.api.options", "requests.api.patch", "requests.api.post", "requests.api.put", "requests.api.request"]



.. raw:: html

   </details>


.. _miscellaneous-options:

``Miscellaneous`` **Checker**
-----------------------------
--notes
"""""""
*List of note tags to take in consideration, separated by a comma.*

**Default:**  ``('FIXME', 'XXX', 'TODO')``


--notes-rgx
"""""""""""
*Regular expression of note tags to take in consideration.*

**Default:** ``""``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.miscellaneous]
   notes = ["FIXME", "XXX", "TODO"]

   notes-rgx = ""



.. raw:: html

   </details>


.. _refactoring-options:

``Refactoring`` **Checker**
---------------------------
--max-nested-blocks
"""""""""""""""""""
*Maximum number of nested blocks for function / method body*

**Default:**  ``5``


--never-returning-functions
"""""""""""""""""""""""""""
*Complete name of functions that never returns. When checking for inconsistent-return-statements if a never returning function is called then it will be considered as an explicit return statement and no message will be printed.*

**Default:**  ``('sys.exit', 'argparse.parse_error')``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.refactoring]
   max-nested-blocks = 5

   never-returning-functions = ["sys.exit", "argparse.parse_error"]



.. raw:: html

   </details>


.. _similarities-options:

``Similarities`` **Checker**
----------------------------
--ignore-comments
"""""""""""""""""
*Comments are removed from the similarity computation*

**Default:**  ``True``


--ignore-docstrings
"""""""""""""""""""
*Docstrings are removed from the similarity computation*

**Default:**  ``True``


--ignore-imports
""""""""""""""""
*Imports are removed from the similarity computation*

**Default:**  ``True``


--ignore-signatures
"""""""""""""""""""
*Signatures are removed from the similarity computation*

**Default:**  ``True``


--min-similarity-lines
""""""""""""""""""""""
*Minimum lines number of a similarity.*

**Default:**  ``4``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.similarities]
   ignore-comments = true

   ignore-docstrings = true

   ignore-imports = true

   ignore-signatures = true

   min-similarity-lines = 4



.. raw:: html

   </details>


.. _spelling-options:

``Spelling`` **Checker**
------------------------
--max-spelling-suggestions
""""""""""""""""""""""""""
*Limits count of emitted suggestions for spelling mistakes.*

**Default:**  ``4``


--spelling-dict
"""""""""""""""
*Spelling dictionary name. Available dictionaries: en (aspell), en_AU (aspell), en_CA (aspell), en_GB (aspell), en_US (aspell).*

**Default:** ``""``


--spelling-ignore-comment-directives
""""""""""""""""""""""""""""""""""""
*List of comma separated words that should be considered directives if they appear at the beginning of a comment and should not be checked.*

**Default:**  ``fmt: on,fmt: off,noqa:,noqa,nosec,isort:skip,mypy:``


--spelling-ignore-words
"""""""""""""""""""""""
*List of comma separated words that should not be checked.*

**Default:** ``""``


--spelling-private-dict-file
""""""""""""""""""""""""""""
*A path to a file that contains the private dictionary; one word per line.*

**Default:** ``""``


--spelling-store-unknown-words
""""""""""""""""""""""""""""""
*Tells whether to store unknown words to the private dictionary (see the --spelling-private-dict-file option) instead of raising a message.*

**Default:**  ``n``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.spelling]
   max-spelling-suggestions = 4

   spelling-dict = ""

   spelling-ignore-comment-directives = "fmt: on,fmt: off,noqa:,noqa,nosec,isort:skip,mypy:"

   spelling-ignore-words = ""

   spelling-private-dict-file = ""

   spelling-store-unknown-words = false



.. raw:: html

   </details>


.. _string-options:

``String`` **Checker**
----------------------
--check-quote-consistency
"""""""""""""""""""""""""
*This flag controls whether inconsistent-quotes generates a warning when the character used as a quote delimiter is used inconsistently within a module.*

**Default:**  ``False``


--check-str-concat-over-line-jumps
""""""""""""""""""""""""""""""""""
*This flag controls whether the implicit-str-concat should generate a warning on implicit string concatenation in sequences defined over several lines.*

**Default:**  ``False``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.string]
   check-quote-consistency = false

   check-str-concat-over-line-jumps = false



.. raw:: html

   </details>


.. _typecheck-options:

``Typecheck`` **Checker**
-------------------------
--contextmanager-decorators
"""""""""""""""""""""""""""
*List of decorators that produce context managers, such as contextlib.contextmanager. Add to this list to register other decorators that produce valid context managers.*

**Default:**  ``['contextlib.contextmanager']``


--generated-members
"""""""""""""""""""
*List of members which are set dynamically and missed by pylint inference system, and so shouldn't trigger E1101 when accessed. Python regular expressions are accepted.*

**Default:**  ``()``


--ignore-mixin-members
""""""""""""""""""""""
*Tells whether missing members accessed in mixin class should be ignored. A class is considered mixin if its name matches the mixin-class-rgx option.*

**Default:**  ``True``


--ignore-none
"""""""""""""
*Tells whether to warn about missing members when the owner of the attribute is inferred to be None.*

**Default:**  ``True``


--ignore-on-opaque-inference
""""""""""""""""""""""""""""
*This flag controls whether pylint should warn about no-member and similar checks whenever an opaque object is returned when inferring. The inference can return multiple potential results while evaluating a Python object, but some branches might not be evaluated, which results in partial inference. In that case, it might be useful to still emit no-member and other checks for the rest of the inferred objects.*

**Default:**  ``True``


--ignored-checks-for-mixins
"""""""""""""""""""""""""""
*List of symbolic message names to ignore for Mixin members.*

**Default:**  ``['no-member', 'not-async-context-manager', 'not-context-manager', 'attribute-defined-outside-init']``


--ignored-classes
"""""""""""""""""
*List of class names for which member attributes should not be checked (useful for classes with dynamically set attributes). This supports the use of qualified names.*

**Default:**  ``('optparse.Values', 'thread._local', '_thread._local', 'argparse.Namespace')``


--missing-member-hint
"""""""""""""""""""""
*Show a hint with possible names when a member name was not found. The aspect of finding the hint is based on edit distance.*

**Default:**  ``True``


--missing-member-hint-distance
""""""""""""""""""""""""""""""
*The minimum edit distance a name should have in order to be considered a similar match for a missing member name.*

**Default:**  ``1``


--missing-member-max-choices
""""""""""""""""""""""""""""
*The total number of similar names that should be taken in consideration when showing a hint for a missing member.*

**Default:**  ``1``


--mixin-class-rgx
"""""""""""""""""
*Regex pattern to define which classes are considered mixins.*

**Default:**  ``.*[Mm]ixin``


--signature-mutators
""""""""""""""""""""
*List of decorators that change the signature of a decorated function.*

**Default:**  ``[]``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.typecheck]
   contextmanager-decorators = ["contextlib.contextmanager"]

   generated-members = []

   ignore-mixin-members = true

   ignore-none = true

   ignore-on-opaque-inference = true

   ignored-checks-for-mixins = ["no-member", "not-async-context-manager", "not-context-manager", "attribute-defined-outside-init"]

   ignored-classes = ["optparse.Values", "thread._local", "_thread._local", "argparse.Namespace"]

   missing-member-hint = true

   missing-member-hint-distance = 1

   missing-member-max-choices = 1

   mixin-class-rgx = ".*[Mm]ixin"

   signature-mutators = []



.. raw:: html

   </details>


.. _variables-options:

``Variables`` **Checker**
-------------------------
--additional-builtins
"""""""""""""""""""""
*List of additional names supposed to be defined in builtins. Remember that you should avoid defining new builtins when possible.*

**Default:**  ``()``


--allow-global-unused-variables
"""""""""""""""""""""""""""""""
*Tells whether unused global variables should be treated as a violation.*

**Default:**  ``True``


--allowed-redefined-builtins
""""""""""""""""""""""""""""
*List of names allowed to shadow builtins*

**Default:**  ``()``


--callbacks
"""""""""""
*List of strings which can identify a callback function by name. A callback name must start or end with one of those strings.*

**Default:**  ``('cb_', '_cb')``


--dummy-variables-rgx
"""""""""""""""""""""
*A regular expression matching the name of dummy variables (i.e. expected to not be used).*

**Default:**  ``_+$|(_[a-zA-Z0-9_]*[a-zA-Z0-9]+?$)|dummy|^ignored_|^unused_``


--ignored-argument-names
""""""""""""""""""""""""
*Argument names that match this expression will be ignored.*

**Default:**  ``re.compile('_.*|^ignored_|^unused_')``


--init-import
"""""""""""""
*Tells whether we should check for unused import in __init__ files.*

**Default:**  ``False``


--redefining-builtins-modules
"""""""""""""""""""""""""""""
*List of qualified module names which can have objects that can redefine builtins.*

**Default:**  ``('six.moves', 'past.builtins', 'future.builtins', 'builtins', 'io')``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.variables]
   additional-builtins = []

   allow-global-unused-variables = true

   allowed-redefined-builtins = []

   callbacks = ["cb_", "_cb"]

   dummy-variables-rgx = "_+$|(_[a-zA-Z0-9_]*[a-zA-Z0-9]+?$)|dummy|^ignored_|^unused_"

   ignored-argument-names = "_.*|^ignored_|^unused_"

   init-import = false

   redefining-builtins-modules = ["six.moves", "past.builtins", "future.builtins", "builtins", "io"]



.. raw:: html

   </details>


Extensions
^^^^^^^^^^


.. _broad_try_clause-options:

``Broad_try_clause`` **Checker**
--------------------------------
--max-try-statements
""""""""""""""""""""
*Maximum number of statements allowed in a try clause*

**Default:**  ``1``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.broad_try_clause]
   max-try-statements = 1



.. raw:: html

   </details>


.. _code_style-options:

``Code_style`` **Checker**
--------------------------
--max-line-length-suggestions
"""""""""""""""""""""""""""""
*Max line length for which to sill emit suggestions. Used to prevent optional suggestions which would get split by a code formatter (e.g., black). Will default to the setting for ``max-line-length``.*

**Default:**  ``0``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.code_style]
   max-line-length-suggestions = 0



.. raw:: html

   </details>


.. _deprecated_builtins-options:

``Deprecated_builtins`` **Checker**
-----------------------------------
--bad-functions
"""""""""""""""
*List of builtins function names that should not be used, separated by a comma*

**Default:**  ``['map', 'filter']``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.deprecated_builtins]
   bad-functions = ["map", "filter"]



.. raw:: html

   </details>


.. _dunder-options:

``Dunder`` **Checker**
----------------------
--good-dunder-names
"""""""""""""""""""
*Good dunder names which should always be accepted.*

**Default:**  ``[]``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.dunder]
   good-dunder-names = []



.. raw:: html

   </details>


.. _magic-value-options:

``Magic-value`` **Checker**
---------------------------
--valid-magic-values
""""""""""""""""""""
*List of valid magic values that `magic-value-compare` will not detect. Supports integers, floats, negative numbers, for empty string enter ``''``, for backslash values just use one backslash e.g \n.*

**Default:**  ``(0, -1, 1, '', '__main__')``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.magic-value]
   valid-magic-values = [0, -1, 1, "", "__main__"]



.. raw:: html

   </details>


.. _parameter_documentation-options:

``Parameter_documentation`` **Checker**
---------------------------------------
--accept-no-param-doc
"""""""""""""""""""""
*Whether to accept totally missing parameter documentation in the docstring of a function that has parameters.*

**Default:**  ``True``


--accept-no-raise-doc
"""""""""""""""""""""
*Whether to accept totally missing raises documentation in the docstring of a function that raises an exception.*

**Default:**  ``True``


--accept-no-return-doc
""""""""""""""""""""""
*Whether to accept totally missing return documentation in the docstring of a function that returns a statement.*

**Default:**  ``True``


--accept-no-yields-doc
""""""""""""""""""""""
*Whether to accept totally missing yields documentation in the docstring of a generator.*

**Default:**  ``True``


--default-docstring-type
""""""""""""""""""""""""
*If the docstring type cannot be guessed the specified docstring type will be used.*

**Default:**  ``default``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.parameter_documentation]
   accept-no-param-doc = true

   accept-no-raise-doc = true

   accept-no-return-doc = true

   accept-no-yields-doc = true

   default-docstring-type = "default"



.. raw:: html

   </details>


.. _typing-options:

``Typing`` **Checker**
----------------------
--runtime-typing
""""""""""""""""
*Set to ``no`` if the app / library does **NOT** need to support runtime introspection of type annotations. If you use type annotations **exclusively** for type checking of an application, you're probably fine. For libraries, evaluate if some users want to access the type hints at runtime first, e.g., through ``typing.get_type_hints``. Applies to Python versions 3.7 - 3.9*

**Default:**  ``True``



.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

.. code-block:: toml

   [tool.pylint.typing]
   runtime-typing = true



.. raw:: html

   </details>
