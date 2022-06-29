Full changelog
==============

What's New in Pylint 1.7.1?
---------------------------
Release date: 2017-04-17

* Fix a false positive which occurred when an exception was reraised

  Closes #1419

* Fix a false positive of ``disallow-trailing-tuple``

  The check was improved by verifying for non-terminating newlines, which
  should exempt function calls and function definitions from the check

  Closes #1424


What's New in Pylint 1.7?
-------------------------

Release date: 2017-04-13

* Don't emit missing-final-newline or trailing-whitespace for formfeeds (page breaks).

  Closes #1218 and #1219

* Don't emit by default no-member if we have opaque inference objects in the inference results

  This is controlled through the new flag ignore-on-opaque-inference, which is by
  default True. The inference can return  multiple potential results while
  evaluating a Python object, but some branches might not be evaluated, which
  results in partial inference. In that case, it might be useful to still emit
  no-member and other checks for the rest of the inferred objects.

* Added new message ``assign-to-new-keyword`` to warn about assigning to names which
  will become a keyword in future Python releases.

  Closes #1351

* Split the 'missing or differing' in parameter documentation in different error.
  'differing-param-doc' covers the differing part of the old 'missing-param-doc',
  and 'differing-type-doc' covers the differing part of the old 'missing-type-doc'

  Closes #1342

* Added a new error, 'used-prior-global-declaration', which is emitted when a name
  is used prior a global declaration in a function. This causes a SyntaxError in
  Python 3.6

  Closes #1257

* The protocol checks are emitting their messages when a special method is set to None.

  Closes #1263

* Properly detect if imported name is assigned to same name in different
  scope.

  Closes #636, #848, #851, and #900

* Require one space for annotations with type hints, as per PEP 8.

* 'trailing-comma-tuple' check was added

  This message is emitted when pylint finds an one-element tuple,
  created by a stray comma. This can suggest a potential problem in the
  code and it is recommended to use parentheses in order to emphasise the
  creation of a tuple, rather than relying on the comma itself.

* Don't emit not-callable for instances with unknown bases.

  Closes #1213

* Treat keyword only arguments the same as positional arguments with regard to unused-argument check

* Don't try to access variables defined in a separate scope when checking for ``protected-access``

* Added new check to detect incorrect usage of len(SEQUENCE) inside
  test conditions.

* Added new extension to detect comparisons against empty string constants

* Added new extension to detect comparisons of integers against zero

* Added new error conditions for 'bad-super-call'

  Now detects ``super(type(self), self)`` and ``super(self.__class__, self)``
  which can lead to recursion loop in derived classes.

* PyLinter.should_analyze_file has a new optional parameter, called ``is_argument``

  Closes #1079

* Add attribute hints for missing members

  Closes #1035

* Add a new warning, 'redefined-argument-from-local'

  Closes #649

* Support inline comments for comma separated values in the config file

  Closes #1024

* epylint.py_run's *script* parameter was removed.

* epylint.py_run now uses ``shell=False`` for running the underlying process.

  Closes #441

* Added a new warning, 'useless-super-delegation'

  Close 839.

* Added a new error, 'invalid-metaclass', raised when
  we can detect that a class is using an improper metaclass.

  Closes #579

* Added a new refactoring message, 'literal-comparison'.

  Closes #786

* arguments-differ takes in consideration kwonlyargs and variadics

  Closes #983

* Removed --optimized-ast

  Fixes part of #975

* Removed --files-output option

  Fixes part of #975

* Removed pylint-gui from the package.

* Removed the HTML reporter

  Fixes part of #975

* ignored-argument-names is now used for ignoring arguments for unused-variable check.

  This option was used for ignoring arguments when computing the correct number of arguments
  a function should have, but for handling the arguments with regard
  to unused-variable check, dummy-variables-rgx was used instead. Now, ignored-argument-names
  is used for its original purpose and also for ignoring the matched arguments for
  the unused-variable check. This offers a better control of what should be ignored
  and how.
  Also, the same option was moved from the design checker to the variables checker,
  which means that the option now appears under the ``[VARIABLES]`` section inside
  the configuration file.

  Closes #862.

* Fix a false positive for keyword variadics with regard to keyword only arguments.

  If a keyword only argument was necessary for a function, but that function was called
  with keyword variadics (\**kwargs), then we were emitting a missing-kwoa false positive,
  which is now fixed.

  Closes #934.

* Fix some false positives with unknown sized variadics.

  Closes #878

* Added a new extension, check_docstring, for checking PEP 257 conventions.

  Closes #868.

* config files with BOM markers can now be read.

  Closes #864.

* epylint.py_run does not crash on big files, using .communicate() instead of .wait()

  Closes #599

* Disable reports by default and show the evaluation score by default

  The reports were disabled by default in order to simplify the interaction
  between the tool and the users. The score is still shown by default, as
  a way of closely measuring when it increases or decreases due to changes
  brought to the code.

  Refs #746

* Disable the information category messages by default. This is a step towards
  making pylint more sane.

  Refs #746.

* Catch more cases as not proper iterables for __slots__ with
  regard to invalid-slots pattern.

  Closes #775

* empty indent strings are rejected.

* Added a new error, 'relative-beyond-top-level', which is emitted
  when a relative import was attempted beyond the top level package.

  Closes #588

* Added a new warning, 'unsupported-assignment-operation', which is
  emitted when item assignment is tried on an object which doesn't
  have this ability.

  Closes #591

* Added a new warning, 'unsupported-delete-operation', which is
  emitted when item deletion is tried on an object which doesn't
  have this ability.

  Closes #592

* Fix a false positive of 'redundant-returns-doc', occurred when the documented
  function was using *yield* instead of *return*.

  Closes #984.

* Fix false positives of 'missing-[raises|params|type]-doc' due to not
  recognizing keyword synonyms supported by Sphinx.

* Added a new refactoring message, 'consider-merging-isinstance', which is
  emitted whenever we can detect that consecutive isinstance calls can be
  merged together.

  Closes #968

* Fix a false positive of 'missing-param-doc' and 'missing-type-doc',
  occurred when a class docstring uses the 'For the parameters, see'
  magic string but the class __init__ docstring does not, or vice versa.

* ``redefined-outer-name`` is now also emitted when a nested loop's target
  variable is the same as a target variable in an outer loop.

  Closes #911.

* Added proper exception type inference for 'missing-raises-doc'.

* Added InvalidMessageError exception class to replace asserts in
  pylint.utils.

* More thorough validation in MessagesStore.register_messages() to avoid
  one message accidentally overwriting another.

* InvalidMessageError, UnknownMessage, and EmptyReport exceptions are
  moved to the new pylint.exceptions submodule.

* UnknownMessage and EmptyReport are renamed to UnknownMessageError and
  EmptyReportError.

* Warnings 'missing-returns-type-doc' and 'missing-yields-type-doc'
  have each been split into two warnings - 'missing-[return|yield]-doc'
  and 'missing-[return|yield]-type-doc'.

* Added epytext support to docparams extension.

  Closes #1029

* Support having plugins with the same name and with options defined

  Closes #1018

* Sort configuration options in a section

  Closes #1087

* Added a new Python 3 warning around implementing '__div__', '__idiv__', or
  '__rdiv__' as those methods are phased out in Python 3.

* Added a new warning, 'overlapping-except', which is
  emitted when two exceptions in the same except-clause are aliases
  for each other or one exceptions is an ancestor of another.

* Avoid crashing on ill-formatted strings when checking for string formatting errors.

* Added a new Python 3 warning for calling 'str.encode' or 'str.decode' with a non-text
  encoding.

* Added new coding convention message, 'single-string-used-for-slots'.

  Closes #1166

* Added a new Python 3 check for accessing 'sys.maxint' which was removed in Python 3 in favor
  of 'sys.maxsize'

* Added a new Python 3 check for bad imports.

* Added a new Python 3 check for accessing deprecated string functions.

* Do not warn about unused arguments or function being redefined in singledispatch
  registered implementations.

  Closes #1032 and #1034

* Added refactoring message 'no-else-return'.

* Improve unused-variable checker to warn about unused variables in module scope.

  Closes #919

* Ignore modules import as _ when checking for unused imports.

  Closes #1190

* Improve handing of Python 3 classes with metaclasses declared in nested scopes.

  Closes #1177

* Added refactoring message 'consider-using-ternary'.

  Closes #1204

* Bug-fix for false-positive logging-format-interpolation` when format specifications
  are used in formatted string.

  Closes #572

* Added a new switch ``single-line-class-stmt`` to allow single-line declaration
  of empty class bodies.

  Closes #738

* Protected access in form ``type(self)._attribute`` are now allowed.

  Closes #1031

* Let the user modify msg-template when Pylint is called from a Python script

  Closes #1269

* Imports checker supports new switch ``allow-wildcard-with-all`` which disables
  warning on wildcard import when imported module defines ``__all__`` variable.

  Closes #831

* ``too-many-format-args`` and ``too-few-format-args`` are emitted correctly when
  starred expression are used in RHS tuple.

  Closes #957

* ``cyclic-import`` checker supports local disable clauses. When one
  of cycle imports was done in scope where disable clause was active,
  cycle is not reported as violation.

  Closes #59
