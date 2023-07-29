:Release: 2.14
:Date: 2022-06-01

Summary -- Release highlights
=============================

With 2.14 ``pylint`` only supports Python version 3.7.2 and above.

We introduced several new checks among which ``duplicate-value`` for sets,
``comparison-of-constants``, and checks related to lambdas. We removed ``no-init`` and
made ``no-self-use`` optional as they were too opinionated. We also added an option
to generate a toml configuration: ``--generate-toml-config``.

We migrated to ``argparse`` from ``optparse`` and refactored the configuration handling
thanks to Daniël van Noord. On the user side it should change the output of the
``--help`` command, and some inconsistencies and bugs should disappear. The behavior
between options set in a config file versus on the command line will be more consistent. For us,
it will permit to maintain this part of the code easily in the future.

As a result of the refactor there are a lot of internal deprecations. If you're a library
maintainer that depends on pylint, please verify that you're ready for pylint 3.0
by activating deprecation warnings.

We continued the integration of ``pylint-error`` and are now at 33%!. We still welcome any community effort
to help review, integrate, and add good/bad examples <https://github.com/pylint-dev/pylint/issues/5953>`_. This should be doable
without any ``pylint`` or ``astroid`` knowledge, so this is the perfect entrypoint if you want
to contribute to ``pylint`` or open source without any experience with our code!

New checkers
============

* Added new checker ``comparison-of-constants``.

  Closes #6076

* Added new checker ``typevar-name-mismatch``: TypeVar must be assigned to a variable with the same name as its name argument.

  Closes #5224

* ``invalid-enum-extension``: Used when a class tries to extend an inherited Enum class.

  Closes #5501

* Added new checker ``typevar-double-variance``: The "covariant" and "contravariant" keyword arguments
  cannot both be set to "True" in a TypeVar.

  Closes #5895

* Add new check ``unnecessary-dunder-call`` for unnecessary dunder method calls.

  Closes #5936

* ``unnecessary-lambda-assignment``: Lambda expression assigned to a variable.
  Define a function using the "def" keyword instead.
  ``unnecessary-direct-lambda-call``: Lambda expression called directly.
  Execute the expression inline instead.

  Closes #5976

* ``potential-index-error``: Emitted when the index of a list or tuple exceeds its length.
  This checker is currently quite conservative to avoid false positives. We welcome
  suggestions for improvements.

  Closes #578

* Added new checker ``unnecessary-list-index-lookup`` for indexing into a list while
  iterating over ``enumerate()``.

  Closes #4525

* Added new message called ``duplicate-value`` which identifies duplicate values inside sets.

  Closes #5880

* Added the ``super-without-brackets`` checker, raised when a super call is missing its brackets.

  Closes #4008

Removed checkers
================

* The ``no-init`` (W0232) warning has been removed. It's ok to not have an ``__init__`` in a class.

  Closes #2409

* Removed the ``assign-to-new-keyword`` message as there are no new keywords in the supported Python
  versions any longer.

  Closes #4683

* Moved ``no-self-use`` check to optional extension.
  You now need to explicitly enable this check using
  ``load-plugins=pylint.extensions.no_self_use``.

  Closes #5502


Extensions
==========

* ``RedefinedLoopNameChecker``

    * Added optional extension ``redefined-loop-name`` to emit messages when a loop variable
      is redefined in the loop body.

   Closes #5072

* ``DocStringStyleChecker``

    * Re-enable checker ``bad-docstring-quotes`` for Python <= 3.7.

   Closes #6087

* ``NoSelfUseChecker``

    * Added ``no-self-use`` check, previously enabled by default.

   Closes #5502


Other Changes
=============

* Started ignoring underscore as a local variable for ``too-many-locals``.

  Closes #6488

* Pylint can now be installed with an extra-require called ``spelling`` (``pip install pylint[spelling]``).
  This will add ``pyenchant`` to pylint's dependencies. You will still need to install the
  requirements for ``pyenchant`` (the ``enchant`` library and any dictionaries) yourself. You will also
  need to set the ``spelling-dict`` option.

  Refs #6462

* Improved wording of the message of ``deprecated-module``

  Closes #6169

* ``Pylint`` now requires Python 3.7.2 or newer to run.

  Closes #4301

* We made a greater effort to reraise failures stemming from the ``astroid``
  library as ``AstroidError``, with the effect that pylint emits ``astroid-error``
  rather than merely ``fatal``. Regardless, please report any such issues you encounter!

* We have improved our recognition of inline disable and enable comments. It is
  now possible to disable ``bad-option-value`` inline (as long as you disable it before
  the bad option value is raised, i.e. ``disable=bad-option-value,bad-message`` not ``disable=bad-message,bad-option-value`` ) as well as certain other
  previously unsupported messages.

  Closes #3312

* The main checker name is now ``main`` instead of ``master``. The configuration does not need to be updated as sections' name are optional.

  Closes #5467

* Update ``invalid-slots-object`` message to show bad object rather than its inferred value.

  Closes #6101

* Fixed a crash in the ``not-an-iterable`` checker involving multiple starred expressions
  inside a call.

  Closes #6372

* Fixed a crash in the ``unused-private-member`` checker involving chained private attributes.

  Closes #6709

* Disable spellchecking of mypy rule names in ignore directives.

  Closes #5929

* ``implicit-str-concat`` will now be raised on calls like ``open("myfile.txt" "a+b")`` too.

  Closes #6441

* Fix a failure to respect inline disables for ``fixme`` occurring on the last line
  of a module when pylint is launched with ``--enable=fixme``.

* Removed the broken ``generate-man`` option.

  Closes #5283
  Closes #1887

* Fixed failure to enable ``deprecated-module`` after a ``disable=all``
  by making ``ImportsChecker`` solely responsible for emitting ``deprecated-module`` instead
  of sharing responsibility with ``StdlibChecker``. (This could have led to double messages.)

* Added the ``generate-toml-config`` option.

  Refs #5462

* ``bad-option-value`` will be emitted whenever a configuration value or command line invocation
  includes an unknown message.

  Closes #4324

* Added the ``unrecognized-option`` message. Raised if we encounter any unrecognized options.

  Closes #5259

* Fix false negative for ``bad-string-format-type`` if the value to be formatted is passed in
  as a variable holding a constant.

* The concept of checker priority has been removed.

* The ``cache-max-size-none`` checker has been renamed to ``method-cache-max-size-none``.

  Closes #5670

* The ``method-cache-max-size-none`` checker will now also check ``functools.cache``.

  Closes #5670

* ``BaseChecker`` classes now require the ``linter`` argument to be passed.

* The ``set_config_directly`` decorator has been removed.

* Don't report ``useless-super-delegation`` for the ``__hash__`` method in classes that also override the ``__eq__`` method.

  Closes #3934

* Fix falsely issuing ``useless-suppression`` on the ``wrong-import-position`` checker.

  Closes #5219

* Fixed false positive ``no-member`` for Enums with self-defined members.

  Closes #5138

* Fix false negative for ``no-member`` when attempting to assign an instance
  attribute to itself without any prior assignment.

  Closes #1555

* Changed message type from ``redefined-outer-name`` to ``redefined-loop-name``
  (optional extension) for redefinitions of outer loop variables by inner loops.

  Closes #5608

* By default the similarity checker will now ignore imports and ignore function signatures when computing
  duplication. If you want to keep the previous behaviour set ``ignore-imports`` and ``ignore-signatures`` to ``False``.

* Pylint now expands the user path (i.e. ``~`` to ``home/yusef/``) and expands environment variables (i.e. ``home/$USER/$project``
  to ``home/yusef/pylint`` for ``USER=yusef`` and ``project=pylint``) for pyreverse's ``output-directory``,
  ``import-graph``, ``ext-import-graph``,  ``int-import-graph`` options, and the spell checker's ``spelling-private-dict-file``
  option.

  Refs #6493

* Don't emit ``unsubscriptable-object`` for string annotations.
  Pylint doesn't check if class is only generic in type stubs only.

  Closes #4369 and #6523

* Fix pyreverse crash ``RuntimeError: dictionary changed size during iteration``

  Refs #6612

* Fix syntax for return type annotations in MermaidJS diagrams produced with ``pyreverse``.

  Closes #6467

* Fix type annotations of class and instance attributes using the alternative union syntax in ``pyreverse`` diagrams.

* Fix bug where it writes a plain text error message to stdout, invalidating output formats.

  Closes #6597

* The refactoring checker now also raises 'consider-using-a-generator' messages for
  ``max()``, ``min()`` and ``sum()``.

  Refs #6595

* Update ranges for ``using-constant-test`` and ``missing-parentheses-for-call-in-test``
  error messages.

* Don't emit ``no-member`` inside type annotations with
  ``from __future__ import annotations``.

  Closes #6594

* Fix ``unexpected-special-method-signature`` false positive for ``__init_subclass__`` methods with one or more arguments.

  Closes #6644


Deprecations
============

* The ``ignore-mixin-members`` option has been deprecated. You should now use the new
  ``ignored-checks-for-mixins`` option.

  Closes #5205

* ``interfaces.implements`` has been deprecated and will be removed in 3.0. Please use standard inheritance
  patterns instead of ``__implements__``.

  Refs #2287

* All ``Interface`` classes in ``pylint.interfaces`` have been deprecated. You can subclass
  the respective normal classes to get the same behaviour. The ``__implements__`` functionality
  was based on a rejected PEP from 2001:
  https://peps.python.org/pep-0245/

  Closes #2287

* ``MapReduceMixin`` has been deprecated. ``BaseChecker`` now implements ``get_map_data`` and
  ``reduce_map_data``. If a checker actually needs to reduce data it should define ``get_map_data``
  as returning something different than ``None`` and let its ``reduce_map_data`` handle a list
  of the types returned by ``get_map_data``.
  An example can be seen by looking at ``pylint/checkers/similar.py``.


* The ``config`` attribute of ``BaseChecker`` has been deprecated. You can use ``checker.linter.config``
  to access the global configuration object instead of a checker-specific object.

  Refs #5392

* The ``level`` attribute of ``BaseChecker`` has been deprecated: everything is now
  displayed in ``--help``, all the time.

  Refs #5392

* The ``set_option`` method of ``BaseChecker`` has been deprecated. You can use ``checker.linter.set_option``
  to set an option on the global configuration object instead of a checker-specific object.

  Refs #5392

* The ``options_providers`` attribute of ``ArgumentsManager`` has been deprecated.

  Refs #5392

* Fix saving of persistent data files in environments where the user's cache
  directory and the linted file are on a different drive.

  Closes #6394

* The ``method-cache-max-size-none`` checker will now also check ``functools.cache``.

* The ``config`` attribute of ``PyLinter`` is now of the ``argparse.Namespace`` type instead of
  ``optparse.Values``.

  Refs #5392

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

* The ``option_groups`` attribute of ``PyLinter`` has been deprecated.

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

* ``pylint.pyreverse.ASTWalker`` has been removed, as it was only used internally by a single child class.

  Refs #6712

* ``pyreverse``: Resolving and displaying implemented interfaces that are defined by the ``__implements__``
  attribute has been deprecated and will be removed in 3.0.

  Refs #6713

* ``is_class_subscriptable_pep585_with_postponed_evaluation_enabled`` has been deprecated.
  Use ``is_postponed_evaluation_enabled(node) and is_node_in_type_annotation_context(node)``
  instead.

  Refs #6536
