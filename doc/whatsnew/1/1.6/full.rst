Full changelog
==============

What's new in Pylint 1.6.3?
----------------------------
Release date: 2016-07-18

* Do not crash when inferring uninferable exception types for docparams extension

  Closes #998


What's new in Pylint 1.6.2?
----------------------------
Release date: 2016-07-15

* Do not crash when printing the help of options with default regular expressions

  Closes #990

* More granular versions for deprecated modules.

  Closes #991


What's new in Pylint 1.6.1?
----------------------------
Release date: 2016-07-07

* Use environment markers for supporting conditional dependencies.


What's New in Pylint 1.6.0?
---------------------------
Release date: 2016-07-03

* Added a new extension, ``pylint.extensions.mccabe``, for warning
  about complexity in code.

* Deprecate support for --optimize-ast

  Fixes part of #975

* Deprecate support for the HTML output

  Fixes part of #975

* Deprecate support for --output-files

  Fixes part of #975

* Fixed a documentation error for the check_docs extension.

  Closes #735

* Made the list of property-defining decorators configurable.

* Fix a bug where the top name of a qualified import was detected as unused variable.

  Closes #923

* bad-builtin is now an extension check.

* generated-members support qualified name through regular expressions.

  For instance, one can specify a regular expression as --generated-members=astroid.node_classes.*
  for ignoring every no-member error that is accessed as in ``astroid.node_classes.missing.object``.

* Add the ability to ignore files based on regex matching, with the new ``--ignore-patterns``
  option. Allow for multiple ignore patterns to be specified. Rather than clobber the existing
  ignore option, we introduced a new one called ignore-patterns.

  Closes #156

* Added a new error, 'trailing-newlines', which is emitted when a file
  has trailing new lines.

  Closes #682

* Add a new option, 'redefining-builtins-modules', for controlling the modules
  which can redefine builtins, such as six.moves and future.builtins.

  Closes #464

* 'reimported' is emitted when the same name is imported from different module.

  Closes #162

* Add a new recommendation checker, 'consider-iterating-dictionary', which is emitted
  which is emitted when a dictionary is iterated through .keys().

  Closes #699

* Use the configparser backport for Python 2

  This fixes a problem we were having with comments inside values, which is fixed
  in Python 3's configparser.

  Closes #828

* A new error was added, 'invalid-length-returned', when the ``__len__``
  special method returned something else than a non-negative number.

  Closes #557

* Switch to using isort internally for wrong-import-order.

  Closes #879

* check_docs extension can find constructor parameters in __init__.

  Closes #887

* Don't warn about invalid-sequence-index if the indexed object has unknown base
  classes.

  Closes #867

* Don't crash when checking, for super-init-not-called, a method defined in an if block.

* Do not emit import-error or no-name-in-module for fallback import blocks by default.

  Until now, we warned with these errors when a fallback import block (a TryExcept block
  that contained imports for Python 2 and 3) was found, but this gets cumbersome when
  trying to write compatible code. As such, we don't check these blocks by default,
  but the analysis can be enforced by using the new ``--analyse-fallback-block`` flag.

  Closes #769.
