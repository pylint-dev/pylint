
.. _messages-overview:

#################
Messages overview
#################


.. This file is auto-generated. Make any changes to the associated
.. docs extension in 'doc/exts/pylint_messages.py'.

Pylint can emit the following messages:


.. _fatal-category:

Fatal
*****

All messages in the fatal category:

.. toctree::
   :maxdepth: 2
   :titlesonly:

   fatal/astroid-error
   fatal/config-parse-error
   fatal/fatal
   fatal/method-check-failed
   fatal/parse-error

All renamed messages in the fatal category:

.. toctree::
   :maxdepth: 1
   :titlesonly:

   fatal/old-import-error

.. _error-category:

Error
*****

All messages in the error category:

.. toctree::
   :maxdepth: 2
   :titlesonly:

   error/abstract-class-instantiated
   error/access-member-before-definition
   error/assigning-non-slot
   error/assignment-from-no-return
   error/assignment-from-none
   error/await-outside-async
   error/bad-configuration-section
   error/bad-except-order
   error/bad-exception-cause
   error/bad-format-character
   error/bad-plugin-value
   error/bad-reversed-sequence
   error/bad-str-strip-call
   error/bad-string-format-type
   error/bad-super-call
   error/bidirectional-unicode
   error/broken-collections-callable
   error/broken-noreturn
   error/catching-non-exception
   error/class-variable-slots-conflict
   error/continue-in-finally
   error/declare-non-slot
   error/dict-iter-missing-items
   error/duplicate-argument-name
   error/duplicate-bases
   error/format-needs-mapping
   error/function-redefined
   error/import-error
   error/inconsistent-mro
   error/inherit-non-class
   error/init-is-generator
   error/invalid-all-format
   error/invalid-all-object
   error/invalid-bool-returned
   error/invalid-bytes-returned
   error/invalid-character-backspace
   error/invalid-character-carriage-return
   error/invalid-character-esc
   error/invalid-character-nul
   error/invalid-character-sub
   error/invalid-character-zero-width-space
   error/invalid-class-object
   error/invalid-enum-extension
   error/invalid-envvar-value
   error/invalid-field-call
   error/invalid-format-returned
   error/invalid-getnewargs-ex-returned
   error/invalid-getnewargs-returned
   error/invalid-hash-returned
   error/invalid-index-returned
   error/invalid-length-hint-returned
   error/invalid-length-returned
   error/invalid-metaclass
   error/invalid-repr-returned
   error/invalid-sequence-index
   error/invalid-slice-index
   error/invalid-slice-step
   error/invalid-slots
   error/invalid-slots-object
   error/invalid-star-assignment-target
   error/invalid-str-returned
   error/invalid-unary-operand-type
   error/invalid-unicode-codec
   error/logging-format-truncated
   error/logging-too-few-args
   error/logging-too-many-args
   error/logging-unsupported-format
   error/method-hidden
   error/misplaced-bare-raise
   error/misplaced-format-function
   error/missing-format-string-key
   error/missing-kwoa
   error/mixed-format-string
   error/modified-iterating-dict
   error/modified-iterating-set
   error/no-member
   error/no-method-argument
   error/no-name-in-module
   error/no-self-argument
   error/no-value-for-parameter
   error/non-iterator-returned
   error/nonexistent-operator
   error/nonlocal-and-global
   error/nonlocal-without-binding
   error/not-a-mapping
   error/not-an-iterable
   error/not-async-context-manager
   error/not-callable
   error/not-context-manager
   error/not-in-loop
   error/notimplemented-raised
   error/positional-only-arguments-expected
   error/possibly-used-before-assignment
   error/potential-index-error
   error/raising-bad-type
   error/raising-non-exception
   error/redundant-keyword-arg
   error/relative-beyond-top-level
   error/repeated-keyword
   error/return-arg-in-generator
   error/return-in-init
   error/return-outside-function
   error/singledispatch-method
   error/singledispatchmethod-function
   error/star-needs-assignment-target
   error/syntax-error
   error/too-few-format-args
   error/too-many-format-args
   error/too-many-function-args
   error/too-many-star-expressions
   error/truncated-format-string
   error/undefined-all-variable
   error/undefined-variable
   error/unexpected-keyword-arg
   error/unexpected-special-method-signature
   error/unhashable-member
   error/unpacking-non-sequence
   error/unrecognized-inline-option
   error/unrecognized-option
   error/unsubscriptable-object
   error/unsupported-assignment-operation
   error/unsupported-binary-operation
   error/unsupported-delete-operation
   error/unsupported-membership-test
   error/used-before-assignment
   error/used-prior-global-declaration
   error/yield-inside-async-function
   error/yield-outside-function

All renamed messages in the error category:

.. toctree::
   :maxdepth: 1
   :titlesonly:

   error/bad-context-manager
   error/bad-exception-context
   error/bad-option-value
   error/maybe-no-member
   error/old-non-iterator-returned-2
   error/old-unbalanced-tuple-unpacking
   error/unhashable-dict-key

.. _warning-category:

Warning
*******

All messages in the warning category:

.. toctree::
   :maxdepth: 2
   :titlesonly:

   warning/abstract-method
   warning/anomalous-backslash-in-string
   warning/anomalous-unicode-escape-in-string
   warning/arguments-differ
   warning/arguments-out-of-order
   warning/arguments-renamed
   warning/assert-on-string-literal
   warning/assert-on-tuple
   warning/attribute-defined-outside-init
   warning/bad-builtin
   warning/bad-chained-comparison
   warning/bad-dunder-name
   warning/bad-format-string
   warning/bad-format-string-key
   warning/bad-indentation
   warning/bad-open-mode
   warning/bad-staticmethod-argument
   warning/bad-thread-instantiation
   warning/bare-except
   warning/binary-op-exception
   warning/boolean-datetime
   warning/broad-exception-caught
   warning/broad-exception-raised
   warning/cell-var-from-loop
   warning/comparison-with-callable
   warning/confusing-with-statement
   warning/consider-ternary-expression
   warning/contextmanager-generator-missing-cleanup
   warning/dangerous-default-value
   warning/deprecated-argument
   warning/deprecated-attribute
   warning/deprecated-class
   warning/deprecated-decorator
   warning/deprecated-method
   warning/deprecated-module
   warning/deprecated-typing-alias
   warning/differing-param-doc
   warning/differing-type-doc
   warning/duplicate-except
   warning/duplicate-key
   warning/duplicate-string-formatting-argument
   warning/duplicate-value
   warning/eq-without-hash
   warning/eval-used
   warning/exec-used
   warning/expression-not-assigned
   warning/f-string-without-interpolation
   warning/fixme
   warning/forgotten-debug-statement
   warning/format-combined-specification
   warning/format-string-without-interpolation
   warning/global-at-module-level
   warning/global-statement
   warning/global-variable-not-assigned
   warning/global-variable-undefined
   warning/implicit-flag-alias
   warning/implicit-str-concat
   warning/import-self
   warning/inconsistent-quotes
   warning/invalid-envvar-default
   warning/invalid-format-index
   warning/invalid-overridden-method
   warning/isinstance-second-argument-not-valid-type
   warning/keyword-arg-before-vararg
   warning/kwarg-superseded-by-positional-arg
   warning/logging-format-interpolation
   warning/logging-fstring-interpolation
   warning/logging-not-lazy
   warning/lost-exception
   warning/method-cache-max-size-none
   warning/misplaced-future
   warning/missing-any-param-doc
   warning/missing-format-argument-key
   warning/missing-format-attribute
   warning/missing-param-doc
   warning/missing-parentheses-for-call-in-test
   warning/missing-raises-doc
   warning/missing-return-doc
   warning/missing-return-type-doc
   warning/missing-timeout
   warning/missing-type-doc
   warning/missing-yield-doc
   warning/missing-yield-type-doc
   warning/modified-iterating-list
   warning/multiple-constructor-doc
   warning/named-expr-without-context
   warning/nan-comparison
   warning/nested-min-max
   warning/non-ascii-file-name
   warning/non-parent-init-called
   warning/non-str-assignment-to-dunder-name
   warning/overlapping-except
   warning/overridden-final-method
   warning/pointless-exception-statement
   warning/pointless-statement
   warning/pointless-string-statement
   warning/possibly-unused-variable
   warning/preferred-module
   warning/protected-access
   warning/raise-missing-from
   warning/raising-format-tuple
   warning/redeclared-assigned-name
   warning/redefined-builtin
   warning/redefined-loop-name
   warning/redefined-outer-name
   warning/redefined-slots-in-subclass
   warning/redundant-returns-doc
   warning/redundant-u-string-prefix
   warning/redundant-unittest-assert
   warning/redundant-yields-doc
   warning/reimported
   warning/return-in-finally
   warning/self-assigning-variable
   warning/self-cls-assignment
   warning/shadowed-import
   warning/shallow-copy-environ
   warning/signature-differs
   warning/subclassed-final-class
   warning/subprocess-popen-preexec-fn
   warning/subprocess-run-check
   warning/super-init-not-called
   warning/super-without-brackets
   warning/too-many-try-statements
   warning/try-except-raise
   warning/unbalanced-dict-unpacking
   warning/unbalanced-tuple-unpacking
   warning/undefined-loop-variable
   warning/unknown-option-value
   warning/unnecessary-ellipsis
   warning/unnecessary-lambda
   warning/unnecessary-pass
   warning/unnecessary-semicolon
   warning/unreachable
   warning/unspecified-encoding
   warning/unused-argument
   warning/unused-format-string-argument
   warning/unused-format-string-key
   warning/unused-import
   warning/unused-private-member
   warning/unused-variable
   warning/unused-wildcard-import
   warning/useless-else-on-loop
   warning/useless-param-doc
   warning/useless-parent-delegation
   warning/useless-type-doc
   warning/useless-with-lock
   warning/using-assignment-expression-in-unsupported-version
   warning/using-constant-test
   warning/using-exception-groups-in-unsupported-version
   warning/using-f-string-in-unsupported-version
   warning/using-final-decorator-in-unsupported-version
   warning/using-generic-type-syntax-in-unsupported-version
   warning/using-positional-only-args-in-unsupported-version
   warning/while-used
   warning/wildcard-import
   warning/wrong-exception-operation

All renamed messages in the warning category:

.. toctree::
   :maxdepth: 1
   :titlesonly:

   warning/broad-except
   warning/cache-max-size-none
   warning/implicit-str-concat-in-sequence
   warning/lru-cache-decorating-method
   warning/old-assignment-from-none
   warning/old-deprecated-argument
   warning/old-deprecated-class
   warning/old-deprecated-decorator
   warning/old-deprecated-method
   warning/old-deprecated-module
   warning/old-empty-docstring
   warning/old-missing-param-doc
   warning/old-missing-returns-doc
   warning/old-missing-type-doc
   warning/old-missing-yields-doc
   warning/old-non-iterator-returned-1
   warning/old-unidiomatic-typecheck
   warning/old-unpacking-non-sequence
   warning/useless-super-delegation

.. _convention-category:

Convention
**********

All messages in the convention category:

.. toctree::
   :maxdepth: 2
   :titlesonly:

   convention/bad-classmethod-argument
   convention/bad-docstring-quotes
   convention/bad-file-encoding
   convention/bad-mcs-classmethod-argument
   convention/bad-mcs-method-argument
   convention/consider-iterating-dictionary
   convention/consider-using-any-or-all
   convention/consider-using-dict-items
   convention/consider-using-enumerate
   convention/consider-using-f-string
   convention/dict-init-mutate
   convention/disallowed-name
   convention/docstring-first-line-empty
   convention/empty-docstring
   convention/import-outside-toplevel
   convention/import-private-name
   convention/invalid-characters-in-docstring
   convention/invalid-name
   convention/line-too-long
   convention/misplaced-comparison-constant
   convention/missing-class-docstring
   convention/missing-final-newline
   convention/missing-function-docstring
   convention/missing-module-docstring
   convention/mixed-line-endings
   convention/multiple-imports
   convention/multiple-statements
   convention/non-ascii-module-import
   convention/non-ascii-name
   convention/single-string-used-for-slots
   convention/singleton-comparison
   convention/superfluous-parens
   convention/too-many-lines
   convention/trailing-newlines
   convention/trailing-whitespace
   convention/typevar-double-variance
   convention/typevar-name-incorrect-variance
   convention/typevar-name-mismatch
   convention/unexpected-line-ending-format
   convention/ungrouped-imports
   convention/unidiomatic-typecheck
   convention/unnecessary-direct-lambda-call
   convention/unnecessary-dunder-call
   convention/unnecessary-lambda-assignment
   convention/unnecessary-negation
   convention/use-implicit-booleaness-not-comparison
   convention/use-implicit-booleaness-not-comparison-to-string
   convention/use-implicit-booleaness-not-comparison-to-zero
   convention/use-implicit-booleaness-not-len
   convention/use-maxsplit-arg
   convention/use-sequence-for-iteration
   convention/useless-import-alias
   convention/wrong-import-order
   convention/wrong-import-position
   convention/wrong-spelling-in-comment
   convention/wrong-spelling-in-docstring

All renamed messages in the convention category:

.. toctree::
   :maxdepth: 1
   :titlesonly:

   convention/blacklisted-name
   convention/compare-to-empty-string
   convention/compare-to-zero
   convention/len-as-condition
   convention/missing-docstring
   convention/old-misplaced-comparison-constant
   convention/old-non-ascii-name
   convention/unneeded-not

.. _refactor-category:

Refactor
********

All messages in the refactor category:

.. toctree::
   :maxdepth: 2
   :titlesonly:

   refactor/chained-comparison
   refactor/comparison-of-constants
   refactor/comparison-with-itself
   refactor/condition-evals-to-constant
   refactor/confusing-consecutive-elif
   refactor/consider-alternative-union-syntax
   refactor/consider-merging-isinstance
   refactor/consider-refactoring-into-while-condition
   refactor/consider-swap-variables
   refactor/consider-using-alias
   refactor/consider-using-assignment-expr
   refactor/consider-using-augmented-assign
   refactor/consider-using-dict-comprehension
   refactor/consider-using-from-import
   refactor/consider-using-generator
   refactor/consider-using-get
   refactor/consider-using-in
   refactor/consider-using-join
   refactor/consider-using-max-builtin
   refactor/consider-using-min-builtin
   refactor/consider-using-namedtuple-or-dataclass
   refactor/consider-using-set-comprehension
   refactor/consider-using-sys-exit
   refactor/consider-using-ternary
   refactor/consider-using-tuple
   refactor/consider-using-with
   refactor/cyclic-import
   refactor/duplicate-code
   refactor/else-if-used
   refactor/empty-comment
   refactor/inconsistent-return-statements
   refactor/literal-comparison
   refactor/magic-value-comparison
   refactor/no-classmethod-decorator
   refactor/no-else-break
   refactor/no-else-continue
   refactor/no-else-raise
   refactor/no-else-return
   refactor/no-self-use
   refactor/no-staticmethod-decorator
   refactor/prefer-typing-namedtuple
   refactor/property-with-parameters
   refactor/redefined-argument-from-local
   refactor/redefined-variable-type
   refactor/redundant-typehint-argument
   refactor/simplifiable-condition
   refactor/simplifiable-if-expression
   refactor/simplifiable-if-statement
   refactor/simplify-boolean-expression
   refactor/stop-iteration-return
   refactor/super-with-arguments
   refactor/too-complex
   refactor/too-few-public-methods
   refactor/too-many-ancestors
   refactor/too-many-arguments
   refactor/too-many-boolean-expressions
   refactor/too-many-branches
   refactor/too-many-instance-attributes
   refactor/too-many-locals
   refactor/too-many-nested-blocks
   refactor/too-many-positional-arguments
   refactor/too-many-public-methods
   refactor/too-many-return-statements
   refactor/too-many-statements
   refactor/trailing-comma-tuple
   refactor/unnecessary-comprehension
   refactor/unnecessary-default-type-args
   refactor/unnecessary-dict-index-lookup
   refactor/unnecessary-list-index-lookup
   refactor/use-a-generator
   refactor/use-dict-literal
   refactor/use-list-literal
   refactor/use-set-for-membership
   refactor/use-yield-from
   refactor/useless-object-inheritance
   refactor/useless-option-value
   refactor/useless-return

All renamed messages in the refactor category:

.. toctree::
   :maxdepth: 1
   :titlesonly:

   refactor/old-no-self-use
   refactor/old-simplifiable-if-statement
   refactor/old-too-many-nested-blocks

.. _information-category:

Information
***********

All messages in the information category:

.. toctree::
   :maxdepth: 2
   :titlesonly:

   information/bad-inline-option
   information/c-extension-no-member
   information/deprecated-pragma
   information/file-ignored
   information/locally-disabled
   information/raw-checker-failed
   information/suppressed-message
   information/use-symbolic-message-instead
   information/useless-suppression

All renamed messages in the information category:

.. toctree::
   :maxdepth: 1
   :titlesonly:

   information/deprecated-disable-all
