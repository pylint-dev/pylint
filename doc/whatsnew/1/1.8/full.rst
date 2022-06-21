Full changelog
==============

What's New in Pylint 1.8.1?
---------------------------
Release date: 2017-12-15

* Wrong version number in __pkginfo__.


What's New in Pylint 1.8?
-------------------------

Release date: 2017-12-15

* Respect disable=... in config file when running with --py3k.

* New warning ``shallow-copy-environ`` added

  Shallow copy of os.environ doesn't work as people may expect. os.environ
  is not a dict object but rather a proxy object, so any changes made
  on copy may have unexpected effects on os.environ

  Instead of copy.copy(os.environ) method os.environ.copy() should be
  used.

  See https://bugs.python.org/issue15373 for details.

  Closes #1301

* Do not display no-absolute-import warning multiple times per file.

* ``trailing-comma-tuple`` refactor check now extends to assignment with
   more than one element (such as lists)

  Closes #1713

* Fixing u'' string in superfluous-parens message

  Closes #1420

* ``abstract-class-instantiated`` is now emitted for all inference paths.

  Closes #1673

* Add set of predefined naming style to ease configuration of checking
  naming conventions.

  Closes #1013

* Added a new check, ``keyword-arg-before-vararg``

  This is emitted for function definitions
  in which keyword arguments are placed before variable
  positional arguments (\*args).

  This may lead to args list getting modified if keyword argument's value
  is not provided in the function call assuming it will take default value
  provided in the definition.

* The ``invalid-name`` check contains the name of the template that caused the failure

  Closes #1176

* Using the -j flag won't start more child linters than needed.

  Closes #1614

* Fix a false positive with bad-python3-import on relative imports

  Closes #1608

* Added a new Python 3 check, ``non-ascii-bytes-literals``

  Closes #1545

* Added a couple of new Python 3 checks for accessing dict methods in non-iterable context

* Protocol checks (not-a-mapping, not-an-iterable and co.) aren't emitted on classes with dynamic getattr

* Added a new warning, 'bad-thread-instantiation'

  This message is emitted when the threading.Thread class does not
  receive the target argument, but receives just one argument, which
  is by default the group parameter.

  Closes #1327

* In non-quiet mode, absolute path of used config file is logged to
  standard error.

  Closes #1519

* Raise meaningful exception for invalid reporter class being selected

  When unknown reporter class will be selected as Pylint reporter,
  meaningful error message would be raised instead of bare ``ImportError``
  or ``AttributeError`` related to module or reporter class being not found.

  Closes #1388

* Added a new Python 3 check for accessing removed functions from itertools
  like ``izip`` or ``ifilterfalse``

* Added a new Python 3 check for accessing removed fields from the types
  module like ``UnicodeType`` or ``XRangeType``

* Added a new Python 3 check for declaring a method ``next`` that would have
  been treated as an iterator in Python 2 but a normal function in Python 3.

* Added a new key-value pair in json output. The key is ``message-id``
  and the value is the message id.

  Closes #1512

* Added a new Python 3.0 check for raising a StopIteration inside a generator.
  The check about raising a StopIteration inside a generator is also valid if the exception
  raised inherit from StopIteration.

  Closes #1385

* Added a new warning, ``raising-format-tuple``, to detect multi-argument
  exception construction instead of message string formatting.

* Added a new check for method of logging module that concatenate string via + operator

  Closes #1479

* Added parameter for limiting number of suggestions in spellchecking checkers

* Fix a corner-case in ``consider-using-ternary`` checker.

  When object ``A`` used in  ``X and A or B`` was falsy in boolean context,
  Pylint incorrectly emitted non-equivalent ternary-based suggestion.
  After a change message is correctly not emitted for this case.

  Closes #1559

* Added ``suggestion-mode`` configuration flag. When flag is enabled, informational
  message is emitted instead of cryptic error message for attributes accessed on
  c-extensions.

  Closes #1466

* Fix a false positive ``useless-super-delegation`` message when
  parameters default values are different from those used in the base class.

  Closes #1085

* Disabling 'wrong-import-order', 'wrong-import-position', or
  'ungrouped-imports' for a single line now prevents that line from
  triggering violations on subsequent lines.

  Closes #1336

* Added a new Python check for inconsistent return statements inside method or function.

  Closes #1267

* Fix ``superfluous-parens`` false positive related to handling logical statements
  involving ``in`` operator.

  Closes #574

* ``function-redefined`` message is no longer emitted for functions and
  methods which names matches dummy variable name regular expression.

  Closes #1369

* Fix ``missing-param-doc`` and ``missing-type-doc`` false positives when
  mixing ``Args`` and ``Keyword Args`` in Google docstring.

  Closes #1409

 * Fix ``missing-docstring`` false negatives when modules, classes, or methods
   consist of compound statements that exceed the ``docstring-min-length``

* Fix ``useless-else-on-loop`` false positives when break statements are
  deeply nested inside loop.

  Closes #1661

* Fix no ``wrong-import-order`` message emitted on ordering of first and third party
  libraries. With this fix, pylint distinguishes third and first party
  modules when checking import order.

  Closes #1702

* Fix ``pylint disable=fixme`` directives ignored for comments following the
  last statement in a file.

  Closes #1681

* Fix ``line-too-long`` message deactivated by wrong disable directive.
  The directive ``disable=fixme`` doesn't deactivate anymore the emission
  of ``line-too-long`` message for long commented lines.

  Closes #1741

* If the rcfile specified on the command line doesn't exist, then an
  IOError exception is raised.

  Closes #1747

* Fix the wrong scope of the ``disable=`` directive after a commented line.
  For example when a ``disable=line-too-long`` directive is at the end of
  a long commented line, it no longer disables the emission of ``line-too-long``
  message for lines that follow.

  Closes #1742
