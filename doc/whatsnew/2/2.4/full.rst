Full changelog
==============

What's New in Pylint 2.4.4?
---------------------------
Release date: 2019-11-13

* Exempt all the names found in type annotations from ``unused-import``

  The previous code was assuming that only ``typing`` names need to be
  exempted, but we need to do that for the rest of the type comment
  names as well.

  Closes #3112

* Relax type import detection for names that do not come from the ``typing`` module

  Closes #3191


What's New in Pylint 2.4.3?
---------------------------
Release date: 2019-10-18

* Fix an issue with ``unnecessary-comprehension`` in comprehensions with additional repacking of elements.

  Closes #3148

* ``import-outside-toplevel`` is emitted for ``ImportFrom`` nodes as well.

  Closes #3175

* Do not emit ``no-method-argument`` for functions using positional only args.

  Closes #3161

* ``consider-using-sys-exit`` is no longer emitted when ``exit`` is imported in the local scope.

  Closes #3147

* ``invalid-overridden-method`` takes ``abc.abstractproperty`` in account

  Closes #3150

* Fixed ``missing-yield-type-doc`` getting incorrectly raised when
  a generator does not document a yield type but has a type annotation.

  Closes #3185

* ``typing.overload`` functions are exempted from ``too-many-function-args``

  Closes #3170


What's New in Pylint 2.4.2?
---------------------------
Release date: 2019-09-30


* ``ignored-modules`` can skip submodules.

  Closes #3135

* ``self-assigning-variable`` skips class level assignments.

  Closes #2930

* ``consider-using-sys-exit`` is exempted when ``exit()`` is imported from ``sys``

  Closes #3145

* Exempt annotated assignments without variable from ``class-variable-slots-conflict``

  Closes #3141

* Fix ``utils.is_error`` to account for functions returning early.

  This fixes a false negative with ``unused-variable`` which was no longer triggered
  when a function raised an exception as the last instruction, but the body of the function
  still had unused variables.

  Closes #3028


What's New in Pylint 2.4.1?
---------------------------
Release date: 2019-09-25


* Exempt type checking definitions defined in both clauses of a type checking guard

  Closes #3127


* Exempt type checking definitions inside the type check guard

  In a7f236528bb3758886b97285a56f3f9ce5b13a99 we added basic support
  for emitting ``used-before-assignment`` if a variable was only defined
  inside a type checking guard (using ``TYPE_CHECKING`` variable from `typing`)
  Unfortunately that missed the case of using those type checking imports
  inside the guard itself, which triggered spurious used-before-assignment errors.

  Closes #3119

* Require astroid >= 2.3 to avoid any compatibility issues.


What's New in Pylint 2.4.0?
---------------------------
Release date: 2019-09-24

* New check: ``import-outside-toplevel``

  This check warns when modules are imported from places other than a
  module toplevel, e.g. inside a function or a class.

* Handle inference ambiguity for ``invalid-format-index``

  Closes #2752

* Removed Python 2 specific checks such as ``relative-import``,
  ``invalid-encoded-data``, ``missing-super-argument``.

* Support forward references for ``function-redefined`` check.

  Closes #2540

* Handle redefinitions in case of type checking imports.

  Closes #2834

* Added a new check, ``consider-using-sys-exit``

  This check is emitted when we detect that a quit() or exit() is invoked
  instead of sys.exit(), which is the preferred way of exiting in program.

  Closes #2925

* ``useless-suppression`` check now ignores ``cyclic-import`` suppressions,
  which could lead to false positives due to incomplete context at the time
  of the check.

  Closes #3064

* Added new checks, ``no-else-break`` and ``no-else-continue``

  These checks highlight unnecessary ``else`` and ``elif`` blocks after
  ``break`` and ``continue`` statements.

  Closes #2327

* Don't emit ``protected-access`` when a single underscore prefixed attribute
  is used inside a special method

  Closes #1802

* Fix the "statement" values in the PyLinter's stats reports by module.

* Added a new check, ``invalid-overridden-method``

  This check is emitted when we detect that a method is overridden
  as a property or a property is overridden as a method. This can indicate
  a bug in the application code that will trigger a runtime error.

  Closes #2670

* Added a new check, ``arguments-out-of-order``

  This check warns if you have arguments with names that match those in
  a function's signature but you are passing them in to the function
  in a different order.

  Closes #2975

* Added a new check, ``redeclared-assigned-name``

  This check is emitted when ``pylint`` detects that a name
  was assigned one or multiple times in the same assignment,
  which indicate a potential bug.

  Closes #2898

* Ignore lambda calls with variadic arguments without a context.

  Inferring variadic positional arguments and keyword arguments
  will result into empty Tuples and Dicts, which can lead in
  some cases to false positives with regard to no-value-for-parameter.
  In order to avoid this, until we'll have support for call context
  propagation, we're ignoring such cases if detected.
  We already did that for function calls, but the previous fix
  was not taking in consideration ``lambdas``

  Closes #2918

* Added a new check, ``self-assigning-variable``. This check is emitted
  when we detect that a variable is assigned to itself, which might
  indicate a potential bug in the code application.

  Closes #2930

* Added a new check, ``property-with-parameters``.

  This check is emitted when we detect that a defined property also
  has parameters, which are useless.

  Closes #3006

* Excluded protocol classes from a couple of checks.

  Closes #3002.

* Add a check ``unnecessary-comprehension`` that detects unnecessary comprehensions.

  This check is emitted when ``pylint`` finds list-, set- or dict-comprehensions,
  that are unnecessary and can be rewritten with the list-, set- or dict-constructors.

  Closes #2905

* Excluded PEP 526 instance and class variables from ``no-member``.

  Closes #2945

* Excluded ``attrs`` from ``too-few-public-methods`` check.

  Closes #2988.

* ``unused-import`` emitted for the right import names in function scopes.

  Closes #2928

* Dropped support for Python 3.4.

* ``assignment-from-no-return`` not triggered for async methods.

  Closes #2902

* Don't emit ``attribute-defined-outside-init`` for variables defined in setters.

  Closes #409

* Syntax errors report the column number.

  Closes #2914

* Support fully qualified typing imports for type annotations.

  Closes #2915

* Exclude ``__dict__`` from ``attribute-defined-outside-init``

* Fix pointer on spelling check when the error are more than one time in the same line.

  Closes #2895

* Fix crash happening when parent of called object cannot be determined

* Allow of in ``GoogleDocstring.re_multiple_type``

* Added ``subprocess-run-check`` to handle subrocess.run without explicitly set ``check`` keyword.

  Closes #2848

* When we can't infer bare except handlers, skip ``try-except-raise``

  Closes #2853

* Handle more ``unnecessary-lambda`` cases when dealing with additional kwargs in wrapped calls

  Closes #2845

* Better postponed evaluation of annotations handling

  Closes #2847

* Support postponed evaluation of annotations for variable annotations.

  Closes #2838

* ``epylint.py_run`` defaults to ``python`` in case the current executable is not a Python one.

  Closes #2837

* Ignore raw docstrings when running Similarities checker with ``ignore-docstrings=yes`` option

* Fix crash when calling ``inherit_from_std_ex`` on a class which is its own ancestor

  Closes #2680

* Added a new check that warns the user if a function call is used inside a test but parentheses are missing.

  Closes #2658

* ``len-as-condition`` now only fires when a ``len(x)`` call is made without an explicit comparison

  The message and description accompanying this checker has been changed
  reflect this new behavior, by explicitly asking to either rely on the
  fact that empty sequence are false or to compare the length with a scalar.

  Closes #2684

* Add ``preferred-module`` checker that notify if an import has a replacement module that should be used.

  This check is emitted when ``pylint`` finds an imported module that has a
  preferred replacement listed in ``preferred-modules``.

* ``assigning-non-slot`` not emitted for classes with unknown base classes.

  Closes #2807

* ``old-division`` is not emitted for non-Const nodes.

  Closes #2808

* Added method arguments to the dot writer for pyreverse.

  Closes #2139

* Support for linting file from stdin.

  IDEs may benefit from the support for linting from an in-memory file.

  Closes #1187

* Added a new check ``class-variable-slots-conflict``

  This check is emitted when ``pylint`` finds a class variable that conflicts with a slot
  name, which would raise a ``ValueError`` at runtime.

* Added new check: dict-iter-missing-items (E1141)

  Closes #2761

* Fix issue with pylint name in output of python -m pylint --version

  Closes #2764

* Relicense logo material under the CC BY-SA 4.0 license.

* Skip ``if`` expressions from f-strings for the ``check_elif`` checker

  Closes #2816

* C0412 (ungrouped-import) is now compatible with isort.

  Closes #2806

* Added new extension to detect too much code in a try clause

  Closes #2877

* ``signature-mutators`` option was added.
  With this option, users can choose to ignore ``too-many-function-args``, ``unexpected-keyword-arg``,
  and ``no-value-for-parameter`` for functions decorated with decorators that change
  the signature of a decorated function.

  Closes #259

* Fixed a pragma comment on its own physical line being ignored when part
  of a logical line with the previous physical line.

  Closes #199

* Fixed false ``undefined-loop-variable`` for a function defined in the loop,
  that uses the variable defined in that loop.

  Closes #202

* Fixed ``unused-argument`` and ``function-redefined`` getting raised for
  functions decorated with ``typing.overload``.

  Closes #1581

* Fixed a false positive with ``consider-using-dict-comprehension`` for constructions that can't be converted to a comprehension

  Closes #2963

* Added ``__post_init__`` to ``defining-attr-methods`` in order to avoid ``attribute-defined-outside-init`` in dataclasses.

  Closes #2581

* Changed description of W0199 to use the term 2-item-tuple instead of 2-uple.

* Allow a ``.`` as a prefix for Sphinx name resolution.

* Checkers must now keep a 1 to 1 relationship between "msgid" (ie: C1234) and "symbol" (i.e. : human-readable-symbol)

* In checkers, an old_names can now be used for multiple new messages and pylint is now a little faster

  It means if you do a partial old_names for a message definition an exception will tell you that you
  must rename the associated identification.

* Allow the choice of f-strings as a valid way of formatting logging strings.

  Closes #2395

* Added ``--list-msgs-enabled`` command to list all enabled and disabled messages given the current RC file and command line arguments.
