Full changelog
==============


What's New in Pylint 2.14.5?
----------------------------
Release date: 2022-07-17


* Fixed a crash in the ``undefined-loop-variable`` check when ``enumerate()`` is used
  in a ternary expression.

  Closes #7131

* Fixed handling of ``--`` as separator between positional arguments and flags.

  Closes #7003

* Fixed the disabling of ``fixme`` and its interaction with ``useless-suppression``.

* Allow lists of default values in parameter documentation for ``Numpy`` style.

  Closes #4035


What's New in Pylint 2.14.4?
----------------------------
Release date: 2022-06-29

* The ``differing-param-doc`` check was triggered by positional only arguments.

  Closes #6950

* Fixed an issue where scanning `.` directory recursively with ``--ignore-path=^path/to/dir`` is not
  ignoring the `path/to/dir` directory.

  Closes #6964

* Fixed regression that didn't allow quoted ``init-hooks`` in option files.

  Closes #7006

* Fixed a false positive for ``modified-iterating-dict`` when updating an existing key.

  Closes #6179

* Fixed an issue where many-core Windows machines (>~60 logical processors) would hang when
  using the default jobs count.

  Closes #6965

* Fixed an issue with the recognition of ``setup.cfg`` files.
  Only ``.cfg`` files that are exactly named ``setup.cfg`` require section names that
  start with ``pylint.``.

  Closes #3630

* Don't report ``import-private-name`` for relative imports.

  Closes #7078


What's New in Pylint 2.14.3?
----------------------------
Release date: 2022-06-18

* Fixed two false positives for ``bad-super-call`` for calls that refer to a non-direct parent.

  Closes #4922, Closes #2903

* Fixed a false positive for ``useless-super-delegation`` for subclasses that specify the number of
  of parameters against a parent that uses a variadic argument.

  Closes #2270

* Allow suppressing ``undefined-loop-variable`` and ``undefined-variable`` without raising ``useless-suppression``.

* Fixed false positive for ``undefined-variable`` for ``__class__`` in inner methods.

  Closes #4032


What's New in Pylint 2.14.2?
----------------------------
Release date: 2022-06-15

* Fixed a false positive for ``unused-variable`` when a function returns an
  ``argparse.Namespace`` object.

  Closes #6895

* Avoided raising an identical ``undefined-loop-variable`` message twice on the same line.

* Don't crash if ``lint.run._query_cpu()`` is run within a Kubernetes Pod, that has only
  a fraction of a cpu core assigned. Just go with one process then.

  Closes #6902

* Fixed a false positive in ``consider-using-f-string`` if the left side of a ``%`` is not a string.

  Closes #6689

* Fixed a false positive in ``unnecessary-list-index-lookup`` and ``unnecessary-dict-index-lookup``
  when the subscript is updated in the body of a nested loop.

  Closes #6818

* Fixed an issue with multi-line ``init-hook`` options which did not record the line endings.

  Closes #6888

* Fixed a false positive for ``used-before-assignment`` when a try block returns
  but an except handler defines a name via type annotation.

* ``--errors-only`` no longer enables previously disabled messages. It was acting as
  "emit *all* and only error messages" without being clearly documented that way.

  Closes #6811


What's New in Pylint 2.14.1?
----------------------------
Release date: 2022-06-06

* Avoid reporting ``unnecessary-dict-index-lookup`` or ``unnecessary-list-index-lookup``
  when the index lookup is part of a destructuring assignment.

  Closes #6788

* Fixed parsing of unrelated options in ``tox.ini``.

  Closes #6800

* Fixed a crash when linting ``__new__()`` methods that return a call expression.

  Closes #6805

* Don't crash if we can't find the user's home directory.

  Closes #6802

* Fixed false positives for ``unused-import`` when aliasing ``typing`` e.g. as ``t``
  and guarding imports under ``t.TYPE_CHECKING``.

  Closes #3846

* Fixed a false positive regression in 2.13 for ``used-before-assignment`` where it is safe to rely
  on a name defined only in an ``except`` block because the ``else`` block returned.

  Closes #6790

* Fixed the use of abbreviations for some special options on the command line.

  Closes #6810

* Fix a crash in the optional ``pylint.extensions.private_import`` extension.

  Closes #6624

* ``bad-option-value`` (E0012) is now a warning ``unknown-option-value`` (W0012). Deleted messages that do not exist
  anymore in pylint now raise ``useless-option-value`` (R0022) instead of ``bad-option-value``. This allows to
  distinguish between genuine typos and configuration that could be cleaned up.  Existing message disables for
  ``bad-option-value`` will still work on both new messages.

  Refs #6794


What's New in Pylint 2.14.0?
----------------------------
Release date: 2022-06-01


* The refactoring checker now also raises 'consider-using-generator' messages for
  ``max()``, ``min()`` and ``sum()``.

  Refs #6595

* We have improved our recognition of inline disable and enable comments. It is
  now possible to disable ``bad-option-value`` inline  (as long as you disable it before
  the bad option value is raised, i.e. ``disable=bad-option-value,bad-message`` not ``disable=bad-message,bad-option-value`` ) as well as certain other previously unsupported messages.

  Closes #3312

* Fixed a crash in the ``unused-private-member`` checker involving chained private attributes.

  Closes #6709

* Added new checker ``comparison-of-constants``.

  Closes #6076

* ``pylint.pyreverse.ASTWalker`` has been removed, as it was only used internally by a single child class.

  Refs #6712

* ``pyreverse``: Resolving and displaying implemented interfaces that are defined by the ``__implements__``
  attribute has been deprecated and will be removed in 3.0.

  Refs #6713

* Fix syntax for return type annotations in MermaidJS diagrams produced with ``pyreverse``.

  Closes #6467

* Fix type annotations of class and instance attributes using the alternative union syntax in ``pyreverse`` diagrams.

* Fix ``unexpected-special-method-signature`` false positive for ``__init_subclass__`` methods with one or more arguments.

  Closes #6644

* Started ignoring underscore as a local variable for ``too-many-locals``.

  Closes #6488

* Improved wording of the message of ``deprecated-module``

  Closes #6169

* ``Pylint`` now requires Python 3.7.2 or newer to run.

  Closes #4301

* ``BaseChecker`` classes now require the ``linter`` argument to be passed.

* Fix a failure to respect inline disables for ``fixme`` occurring on the last line
  of a module when pylint is launched with ``--enable=fixme``.

* Update ``invalid-slots-object`` message to show bad object rather than its inferred value.

  Closes #6101

* The main checker name is now ``main`` instead of ``master``. The configuration does not need to be updated as sections' name are optional.

  Closes #5467

* Don't report ``useless-super-delegation`` for the ``__hash__`` method in classes that also override the ``__eq__`` method.

  Closes #3934

* Added new checker ``typevar-name-mismatch``: TypeVar must be assigned to a variable with the same name as its name argument.

  Closes #5224

* Pylint can now be installed with an extra-require called ``spelling`` (``pip install pylint[spelling]``).
  This will add ``pyenchant`` to pylint's dependencies. You will still need to install the
  requirements for ``pyenchant`` (the ``enchant`` library and any dictionaries) yourself. You will also
  need to set the ``spelling-dict`` option.

  Refs #6462

* Removed the ``assign-to-new-keyword`` message as there are no new keywords in the supported Python
  versions any longer.

  Closes #4683

* Fixed a crash in the ``not-an-iterable`` checker involving multiple starred expressions
  inside a call.

  Closes #6372

* Fixed a crash in the ``docparams`` extension involving raising the result of a function.

* Fixed failure to enable ``deprecated-module`` after a ``disable=all``
  by making ``ImportsChecker`` solely responsible for emitting ``deprecated-module`` instead
  of sharing responsibility with ``StdlibChecker``. (This could have led to double messages.)

* The ``no-init`` (W0232) warning has been removed. It's ok to not have an ``__init__`` in a class.

  Closes #2409

* The ``config`` attribute of ``BaseChecker`` has been deprecated. You can use ``checker.linter.config``
  to access the global configuration object instead of a checker-specific object.

  Refs #5392

* The ``level`` attribute of ``BaseChecker`` has been deprecated: everything is now
  displayed in ``--help``, all the time.

  Refs #5392

* The ``options_providers`` attribute of ``ArgumentsManager`` has been deprecated.

  Refs #5392

* The ``option_groups`` attribute of ``PyLinter`` has been deprecated.

  Refs #5392

* All ``Interface`` classes in ``pylint.interfaces`` have been deprecated. You can subclass
  the respective normal classes to get the same behaviour. The ``__implements__`` functionality
  was based on a rejected PEP from 2001:
  https://peps.python.org/pep-0245/

  Closes #2287

* The ``set_option`` method of ``BaseChecker`` has been deprecated. You can use ``checker.linter.set_option``
  to set an option on the global configuration object instead of a checker-specific object.

  Refs #5392

* ``implicit-str-concat`` will now be raised on calls like ``open("myfile.txt" "a+b")`` too.

  Closes #6441

* The ``config`` attribute of ``PyLinter`` is now of the ``argparse.Namespace`` type instead of
  ``optparse.Values``.

  Refs #5392

* ``MapReduceMixin`` has been deprecated. ``BaseChecker`` now implements ``get_map_data`` and
  ``reduce_map_data``. If a checker actually needs to reduce data it should define ``get_map_data``
  as returning something different than ``None`` and let its ``reduce_map_data`` handle a list
  of the types returned by ``get_map_data``.
  An example can be seen by looking at ``pylint/checkers/similar.py``.

* ``UnsupportedAction`` has been deprecated.

  Refs #5392

* ``OptionsManagerMixIn`` has been deprecated.

  Refs #5392

* ``OptionParser`` has been deprecated.

  Refs #5392

* ``Option`` has been deprecated.

  Refs #5392

* ``OptionsProviderMixIn`` has been deprecated.

  Refs #5392

* ``ConfigurationMixIn`` has been deprecated.

  Refs #5392

* ``get_global_config`` has been deprecated. You can now access all global options from
  ``checker.linter.config``.

  Refs #5392

* ``OptionsManagerMixIn`` has been replaced with ``ArgumentsManager``. ``ArgumentsManager`` is considered
  private API and most methods that were public on ``OptionsManagerMixIn`` have now been deprecated and will
  be removed in a future release.

  Refs #5392

* ``OptionsProviderMixIn`` has been replaced with ``ArgumentsProvider``. ``ArgumentsProvider`` is considered
  private API and most methods that were public on ``OptionsProviderMixIn`` have now been deprecated and will
  be removed in a future release.

  Refs #5392

* ``interfaces.implements`` has been deprecated and will be removed in 3.0. Please use standard inheritance
  patterns instead of ``__implements__``.

  Refs #2287

* ``invalid-enum-extension``: Used when a class tries to extend an inherited Enum class.

  Closes #5501

* Added the ``unrecognized-option`` message. Raised if we encounter any unrecognized options.

  Closes #5259

* Added new checker ``typevar-double-variance``: The "covariant" and "contravariant" keyword arguments
  cannot both be set to "True" in a TypeVar.

  Closes #5895

* Re-enable checker ``bad-docstring-quotes`` for Python <= 3.7.

  Closes #6087

* Removed the broken ``generate-man`` option.

  Closes #5283
  Closes #1887

* Fix false negative for ``bad-string-format-type`` if the value to be formatted is passed in
  as a variable holding a constant.

* Add new check ``unnecessary-dunder-call`` for unnecessary dunder method calls.

  Closes #5936
  Closes #6074

* The ``cache-max-size-none`` checker has been renamed to ``method-cache-max-size-none``.

  Closes #5670

* The ``method-cache-max-size-none`` checker will now also check ``functools.cache``.

  Closes #5670

* ``unnecessary-lambda-assignment``: Lambda expression assigned to a variable.
  Define a function using the "def" keyword instead.
  ``unnecessary-direct-lambda-call``: Lambda expression called directly.
  Execute the expression inline instead.

  Closes #5976

* ``potential-index-error``: Emitted when the index of a list or tuple exceeds its length.
  This checker is currently quite conservative to avoid false positives. We welcome
  suggestions for improvements.

  Closes #578

* Added optional extension ``redefined-loop-name`` to emit messages when a loop variable
  is redefined in the loop body.

  Closes #5072

* Changed message type from ``redefined-outer-name`` to ``redefined-loop-name``
  (optional extension) for redefinitions of outer loop variables by inner loops.

  Closes #5608

* The ``ignore-mixin-members`` option has been deprecated. You should now use the new
  ``ignored-checks-for-mixins`` option.

  Closes #5205

* ``bad-option-value`` will be emitted whenever a configuration value or command line invocation
  includes an unknown message.

  Closes #4324

* Avoid reporting ``superfluous-parens`` on expressions using the ``is not`` operator.

  Closes #5930

* Added the ``super-without-brackets`` checker, raised when a super call is missing its brackets.

  Closes #4008

* Added the ``generate-toml-config`` option.

  Refs #5462

* Added new checker ``unnecessary-list-index-lookup`` for indexing into a list while
  iterating over ``enumerate()``.

  Closes #4525

* Fix falsely issuing ``useless-suppression`` on the ``wrong-import-position`` checker.

  Closes #5219

* Fixed false positive ``no-member`` for Enums with self-defined members.

  Closes #5138

* Fix false negative for ``no-member`` when attempting to assign an instance
  attribute to itself without any prior assignment.

  Closes #1555

* The concept of checker priority has been removed.

* Add a new command line option ``--minimal-messages-config`` for ``pytest``, which disables all
  irrelevant messages when running the functional tests.

* ``duplicate-argument-name`` now only raises once for each set of duplicated arguments.

* Fix bug where specifically enabling just ``await-outside-async`` was not possible.

* The ``set_config_directly`` decorator has been removed.

* Added new message called ``duplicate-value`` which identifies duplicate values inside sets.

  Closes #5880

* Pylint now expands the user path (i.e. ``~`` to ``home/yusef/``) and expands environment variables (i.e. ``home/$USER/$project``
  to ``home/yusef/pylint`` for ``USER=yusef`` and ``project=pylint``) for pyreverse's ``output-directory``,
  ``import-graph``, ``ext-import-graph``,  ``int-import-graph`` options, and the spell checker's ``spelling-private-dict-file``
  option.

  Refs #6493

* Created ``NoSelfUseChecker`` extension and moved the ``no-self-use`` check.
  You now need to explicitly enable this check using
  ``load-plugins=pylint.extensions.no_self_use``.

  Closes #5502

* Fix saving of persistent data files in environments where the user's cache
  directory and the linted file are on a different drive.

  Closes #6394

* Don't emit ``unsubscriptable-object`` for string annotations.
  Pylint doesn't check if class is only generic in type stubs only.

  Closes #4369 and #6523

* Fix pyreverse crash ``RuntimeError: dictionary changed size during iteration``

  Refs #6612

* Fix bug where it writes a plain text error message to stdout, invalidating output formats.

  Closes #6597

* ``is_class_subscriptable_pep585_with_postponed_evaluation_enabled`` has been deprecated.
  Use ``is_postponed_evaluation_enabled(node) and is_node_in_type_annotation_context(node)``
  instead.

  Refs #6536

* Update ranges for ``using-constant-test`` and ``missing-parentheses-for-call-in-test``
  error messages.

* Don't emit ``no-member`` inside type annotations with
  ``from __future__ import annotations``.

  Closes #6594
