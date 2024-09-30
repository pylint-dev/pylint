Pylint features
===============

.. This file is auto-generated. Make any changes to the associated
.. docs extension in 'doc/exts/pylint_features.py'.

Pylint checkers' options and switches
-------------------------------------

Pylint checkers can provide three set of features:

* options that control their execution,
* messages that they can raise,
* reports that they can generate.

Below is a list of all checkers and their features.

Async checker
~~~~~~~~~~~~~

Verbatim name of the checker is ``async``.

Async checker Messages
^^^^^^^^^^^^^^^^^^^^^^
:not-async-context-manager (E1701): *Async context manager '%s' doesn't implement __aenter__ and __aexit__.*
  Used when an async context manager is used with an object that does not
  implement the async context management protocol. This message can't be
  emitted when using Python < 3.5.
:yield-inside-async-function (E1700): *Yield inside async function*
  Used when an `yield` or `yield from` statement is found inside an async
  function. This message can't be emitted when using Python < 3.5.


Bad-Chained-Comparison checker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``bad-chained-comparison``.

Bad-Chained-Comparison checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:bad-chained-comparison (W3601): *Suspicious %s-part chained comparison using semantically incompatible operators (%s)*
  Used when there is a chained comparison where one expression is part of two
  comparisons that belong to different semantic groups ("<" does not mean the
  same thing as "is", chaining them in "0 < x is None" is probably a mistake).


Basic checker
~~~~~~~~~~~~~

Verbatim name of the checker is ``basic``.

See also :ref:`basic checker's options' documentation <basic-options>`

Basic checker Messages
^^^^^^^^^^^^^^^^^^^^^^
:not-in-loop (E0103): *%r not properly in loop*
  Used when break or continue keywords are used outside a loop.
:function-redefined (E0102): *%s already defined line %s*
  Used when a function / class / method is redefined.
:continue-in-finally (E0116): *'continue' not supported inside 'finally' clause*
  Emitted when the `continue` keyword is found inside a finally clause, which
  is a SyntaxError.
:abstract-class-instantiated (E0110): *Abstract class %r with abstract methods instantiated*
  Used when an abstract class with `abc.ABCMeta` as metaclass has abstract
  methods and is instantiated.
:star-needs-assignment-target (E0114): *Can use starred expression only in assignment target*
  Emitted when a star expression is not used in an assignment target.
:duplicate-argument-name (E0108): *Duplicate argument name %r in function definition*
  Duplicate argument names in function definitions are syntax errors.
:return-in-init (E0101): *Explicit return in __init__*
  Used when the special class method __init__ has an explicit return value.
:too-many-star-expressions (E0112): *More than one starred expression in assignment*
  Emitted when there are more than one starred expressions (`*x`) in an
  assignment. This is a SyntaxError.
:nonlocal-and-global (E0115): *Name %r is nonlocal and global*
  Emitted when a name is both nonlocal and global.
:used-prior-global-declaration (E0118): *Name %r is used prior to global declaration*
  Emitted when a name is used prior a global declaration, which results in an
  error since Python 3.6. This message can't be emitted when using Python <
  3.6.
:return-outside-function (E0104): *Return outside function*
  Used when a "return" statement is found outside a function or method.
:return-arg-in-generator (E0106): *Return with argument inside generator*
  Used when a "return" statement with an argument is found in a generator
  function or method (e.g. with some "yield" statements). This message can't be
  emitted when using Python >= 3.3.
:invalid-star-assignment-target (E0113): *Starred assignment target must be in a list or tuple*
  Emitted when a star expression is used as a starred assignment target.
:bad-reversed-sequence (E0111): *The first reversed() argument is not a sequence*
  Used when the first argument to reversed() builtin isn't a sequence (does not
  implement __reversed__, nor __getitem__ and __len__
:nonexistent-operator (E0107): *Use of the non-existent %s operator*
  Used when you attempt to use the C-style pre-increment or pre-decrement
  operator -- and ++, which doesn't exist in Python.
:yield-outside-function (E0105): *Yield outside function*
  Used when a "yield" statement is found outside a function or method.
:init-is-generator (E0100): *__init__ method is a generator*
  Used when the special class method __init__ is turned into a generator by a
  yield in its body.
:misplaced-format-function (E0119): *format function is not called on str*
  Emitted when format function is not called on str object. e.g doing
  print("value: {}").format(123) instead of print("value: {}".format(123)).
  This might not be what the user intended to do.
:nonlocal-without-binding (E0117): *nonlocal name %s found without binding*
  Emitted when a nonlocal variable does not have an attached name somewhere in
  the parent scopes
:lost-exception (W0150): *%s statement in finally block may swallow exception*
  Used when a break or a return statement is found inside the finally clause of
  a try...finally block: the exceptions raised in the try clause will be
  silently swallowed instead of being re-raised.
:return-in-finally (W0134): *'return' shadowed by the 'finally' clause.*
  Emitted when a 'return' statement is found in a 'finally' block. This will
  overwrite the return value of a function and should be avoided.
:assert-on-tuple (W0199): *Assert called on a populated tuple. Did you mean 'assert x,y'?*
  A call of assert on a tuple will always evaluate to true if the tuple is not
  empty, and will always evaluate to false if it is.
:assert-on-string-literal (W0129): *Assert statement has a string literal as its first argument. The assert will %s fail.*
  Used when an assert statement has a string literal as its first argument,
  which will cause the assert to always pass.
:self-assigning-variable (W0127): *Assigning the same variable %r to itself*
  Emitted when we detect that a variable is assigned to itself
:comparison-with-callable (W0143): *Comparing against a callable, did you omit the parenthesis?*
  This message is emitted when pylint detects that a comparison with a callable
  was made, which might suggest that some parenthesis were omitted, resulting
  in potential unwanted behaviour.
:nan-comparison (W0177): *Comparison %s should be %s*
  Used when an expression is compared to NaN values like numpy.NaN and
  float('nan').
:dangerous-default-value (W0102): *Dangerous default value %s as argument*
  Used when a mutable value as list or dictionary is detected in a default
  value for an argument.
:duplicate-key (W0109): *Duplicate key %r in dictionary*
  Used when a dictionary expression binds the same key multiple times.
:duplicate-value (W0130): *Duplicate value %r in set*
  This message is emitted when a set contains the same value two or more times.
:useless-else-on-loop (W0120): *Else clause on loop without a break statement, remove the else and de-indent all the code inside it*
  Loops should only have an else clause if they can exit early with a break
  statement, otherwise the statements under else should be on the same scope as
  the loop itself.
:pointless-exception-statement (W0133): *Exception statement has no effect*
  Used when an exception is created without being assigned, raised or returned
  for subsequent use elsewhere.
:expression-not-assigned (W0106): *Expression "%s" is assigned to nothing*
  Used when an expression that is not a function call is assigned to nothing.
  Probably something else was intended.
:confusing-with-statement (W0124): *Following "as" with another context manager looks like a tuple.*
  Emitted when a `with` statement component returns multiple values and uses
  name binding with `as` only for a part of those values, as in with ctx() as
  a, b. This can be misleading, since it's not clear if the context manager
  returns a tuple or if the node without a name binding is another context
  manager.
:unnecessary-lambda (W0108): *Lambda may not be necessary*
  Used when the body of a lambda expression is a function call on the same
  argument list as the lambda itself; such lambda expressions are in all but a
  few cases replaceable with the function being called in the body of the
  lambda.
:named-expr-without-context (W0131): *Named expression used without context*
  Emitted if named expression is used to do a regular assignment outside a
  context like if, for, while, or a comprehension.
:redeclared-assigned-name (W0128): *Redeclared variable %r in assignment*
  Emitted when we detect that a variable was redeclared in the same assignment.
:pointless-statement (W0104): *Statement seems to have no effect*
  Used when a statement doesn't have (or at least seems to) any effect.
:pointless-string-statement (W0105): *String statement has no effect*
  Used when a string is used as a statement (which of course has no effect).
  This is a particular case of W0104 with its own message so you can easily
  disable it if you're using those strings as documentation, instead of
  comments.
:contextmanager-generator-missing-cleanup (W0135): *The context used in function %r will not be exited.*
  Used when a contextmanager is used inside a generator function and the
  cleanup is not handled.
:unnecessary-pass (W0107): *Unnecessary pass statement*
  Used when a "pass" statement can be removed without affecting the behaviour
  of the code.
:unreachable (W0101): *Unreachable code*
  Used when there is some code behind a "return" or "raise" statement, which
  will never be accessed.
:eval-used (W0123): *Use of eval*
  Used when you use the "eval" function, to discourage its usage. Consider
  using `ast.literal_eval` for safely evaluating strings containing Python
  expressions from untrusted sources.
:exec-used (W0122): *Use of exec*
  Raised when the 'exec' statement is used. It's dangerous to use this function
  for a user input, and it's also slower than actual code in general. This
  doesn't mean you should never use it, but you should consider alternatives
  first and restrict the functions available.
:using-constant-test (W0125): *Using a conditional statement with a constant value*
  Emitted when a conditional statement (If or ternary if) uses a constant value
  for its test. This might not be what the user intended to do.
:missing-parentheses-for-call-in-test (W0126): *Using a conditional statement with potentially wrong function or method call due to missing parentheses*
  Emitted when a conditional statement (If or ternary if) seems to wrongly call
  a function due to missing parentheses
:comparison-of-constants (R0133): *Comparison between constants: '%s %s %s' has a constant value*
  When two literals are compared with each other the result is a constant.
  Using the constant directly is both easier to read and more performant.
  Initializing 'True' and 'False' this way is not required since Python 2.3.
:literal-comparison (R0123): *In '%s', use '%s' when comparing constant literals not '%s' ('%s')*
  Used when comparing an object to a literal, which is usually what you do not
  want to do, since you can compare to a different literal than what was
  expected altogether.
:comparison-with-itself (R0124): *Redundant comparison - %s*
  Used when something is compared against itself.
:invalid-name (C0103): *%s name "%s" doesn't conform to %s*
  Used when the name doesn't conform to naming rules associated to its type
  (constant, variable, class...).
:singleton-comparison (C0121): *Comparison %s should be %s*
  Used when an expression is compared to singleton values like True, False or
  None.
:disallowed-name (C0104): *Disallowed name "%s"*
  Used when the name matches bad-names or bad-names-rgxs- (unauthorized names).
:empty-docstring (C0112): *Empty %s docstring*
  Used when a module, function, class or method has an empty docstring (it
  would be too easy ;).
:missing-class-docstring (C0115): *Missing class docstring*
  Used when a class has no docstring. Even an empty class must have a
  docstring.
:missing-function-docstring (C0116): *Missing function or method docstring*
  Used when a function or method has no docstring. Some special methods like
  __init__ do not require a docstring.
:missing-module-docstring (C0114): *Missing module docstring*
  Used when a module has no docstring. Empty modules do not require a
  docstring.
:typevar-name-incorrect-variance (C0105): *Type variable name does not reflect variance%s*
  Emitted when a TypeVar name doesn't reflect its type variance. According to
  PEP8, it is recommended to add suffixes '_co' and '_contra' to the variables
  used to declare covariant or contravariant behaviour respectively. Invariant
  (default) variables do not require a suffix. The message is also emitted when
  invariant variables do have a suffix.
:typevar-double-variance (C0131): *TypeVar cannot be both covariant and contravariant*
  Emitted when both the "covariant" and "contravariant" keyword arguments are
  set to "True" in a TypeVar.
:typevar-name-mismatch (C0132): *TypeVar name "%s" does not match assigned variable name "%s"*
  Emitted when a TypeVar is assigned to a variable that does not match its name
  argument.
:unidiomatic-typecheck (C0123): *Use isinstance() rather than type() for a typecheck.*
  The idiomatic way to perform an explicit typecheck in Python is to use
  isinstance(x, Y) rather than type(x) == Y, type(x) is Y. Though there are
  unusual situations where these give different results.

Basic checker Reports
^^^^^^^^^^^^^^^^^^^^^
:RP0101: Statistics by type


Classes checker
~~~~~~~~~~~~~~~

Verbatim name of the checker is ``classes``.

See also :ref:`classes checker's options' documentation <classes-options>`

Classes checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^
:access-member-before-definition (E0203): *Access to member %r before its definition line %s*
  Used when an instance member is accessed before it's actually assigned.
:method-hidden (E0202): *An attribute defined in %s line %s hides this method*
  Used when a class defines a method which is hidden by an instance attribute
  from an ancestor class or set by some client code.
:assigning-non-slot (E0237): *Assigning to attribute %r not defined in class slots*
  Used when assigning to an attribute not defined in the class slots.
:duplicate-bases (E0241): *Duplicate bases for class %r*
  Duplicate use of base classes in derived classes raise TypeErrors.
:invalid-enum-extension (E0244): *Extending inherited Enum class "%s"*
  Used when a class tries to extend an inherited Enum class. Doing so will
  raise a TypeError at runtime.
:inconsistent-mro (E0240): *Inconsistent method resolution order for class %r*
  Used when a class has an inconsistent method resolution order.
:inherit-non-class (E0239): *Inheriting %r, which is not a class.*
  Used when a class inherits from something which is not a class.
:invalid-slots (E0238): *Invalid __slots__ object*
  Used when an invalid __slots__ is found in class. Only a string, an iterable
  or a sequence is permitted.
:invalid-class-object (E0243): *Invalid assignment to '__class__'. Should be a class definition but got a '%s'*
  Used when an invalid object is assigned to a __class__ property. Only a class
  is permitted.
:invalid-slots-object (E0236): *Invalid object %r in __slots__, must contain only non empty strings*
  Used when an invalid (non-string) object occurs in __slots__.
:no-method-argument (E0211): *Method %r has no argument*
  Used when a method which should have the bound instance as first argument has
  no argument defined.
:no-self-argument (E0213): *Method %r should have "self" as first argument*
  Used when a method has an attribute different the "self" as first argument.
  This is considered as an error since this is a so common convention that you
  shouldn't break it!
:declare-non-slot (E0245): *No such name %r in __slots__*
  Raised when a type annotation on a class is absent from the list of names in
  __slots__, and __slots__ does not contain a __dict__ entry.
:unexpected-special-method-signature (E0302): *The special method %r expects %s param(s), %d %s given*
  Emitted when a special method was defined with an invalid number of
  parameters. If it has too few or too many, it might not work at all.
:class-variable-slots-conflict (E0242): *Value %r in slots conflicts with class variable*
  Used when a value in __slots__ conflicts with a class variable, property or
  method.
:invalid-bool-returned (E0304): *__bool__ does not return bool*
  Used when a __bool__ method returns something which is not a bool
:invalid-bytes-returned (E0308): *__bytes__ does not return bytes*
  Used when a __bytes__ method returns something which is not bytes
:invalid-format-returned (E0311): *__format__ does not return str*
  Used when a __format__ method returns something which is not a string
:invalid-getnewargs-returned (E0312): *__getnewargs__ does not return a tuple*
  Used when a __getnewargs__ method returns something which is not a tuple
:invalid-getnewargs-ex-returned (E0313): *__getnewargs_ex__ does not return a tuple containing (tuple, dict)*
  Used when a __getnewargs_ex__ method returns something which is not of the
  form tuple(tuple, dict)
:invalid-hash-returned (E0309): *__hash__ does not return int*
  Used when a __hash__ method returns something which is not an integer
:invalid-index-returned (E0305): *__index__ does not return int*
  Used when an __index__ method returns something which is not an integer
:non-iterator-returned (E0301): *__iter__ returns non-iterator*
  Used when an __iter__ method returns something which is not an iterable (i.e.
  has no `__next__` method)
:invalid-length-returned (E0303): *__len__ does not return non-negative integer*
  Used when a __len__ method returns something which is not a non-negative
  integer
:invalid-length-hint-returned (E0310): *__length_hint__ does not return non-negative integer*
  Used when a __length_hint__ method returns something which is not a non-
  negative integer
:invalid-repr-returned (E0306): *__repr__ does not return str*
  Used when a __repr__ method returns something which is not a string
:invalid-str-returned (E0307): *__str__ does not return str*
  Used when a __str__ method returns something which is not a string
:arguments-differ (W0221): *%s %s %r method*
  Used when a method has a different number of arguments than in the
  implemented interface or in an overridden method. Extra arguments with
  default values are ignored.
:arguments-renamed (W0237): *%s %s %r method*
  Used when a method parameter has a different name than in the implemented
  interface or in an overridden method.
:protected-access (W0212): *Access to a protected member %s of a client class*
  Used when a protected member (i.e. class member with a name beginning with an
  underscore) is accessed outside the class or a descendant of the class where
  it's defined.
:attribute-defined-outside-init (W0201): *Attribute %r defined outside __init__*
  Used when an instance attribute is defined outside the __init__ method.
:subclassed-final-class (W0240): *Class %r is a subclass of a class decorated with typing.final: %r*
  Used when a class decorated with typing.final has been subclassed.
:implicit-flag-alias (W0213): *Flag member %(overlap)s shares bit positions with %(sources)s*
  Used when multiple integer values declared within an enum.IntFlag class share
  a common bit position.
:abstract-method (W0223): *Method %r is abstract in class %r but is not overridden in child class %r*
  Used when an abstract method (i.e. raise NotImplementedError) is not
  overridden in concrete class.
:overridden-final-method (W0239): *Method %r overrides a method decorated with typing.final which is defined in class %r*
  Used when a method decorated with typing.final has been overridden.
:invalid-overridden-method (W0236): *Method %r was expected to be %r, found it instead as %r*
  Used when we detect that a method was overridden in a way that does not match
  its base class which could result in potential bugs at runtime.
:redefined-slots-in-subclass (W0244): *Redefined slots %r in subclass*
  Used when a slot is re-defined in a subclass.
:signature-differs (W0222): *Signature differs from %s %r method*
  Used when a method signature is different than in the implemented interface
  or in an overridden method.
:bad-staticmethod-argument (W0211): *Static method with %r as first argument*
  Used when a static method has "self" or a value specified in valid-
  classmethod-first-arg option or valid-metaclass-classmethod-first-arg option
  as first argument.
:super-without-brackets (W0245): *Super call without brackets*
  Used when a call to super does not have brackets and thus is not an actual
  call and does not work as expected.
:unused-private-member (W0238): *Unused private member `%s.%s`*
  Emitted when a private member of a class is defined but not used.
:useless-parent-delegation (W0246): *Useless parent or super() delegation in method %r*
  Used whenever we can detect that an overridden method is useless, relying on
  parent or super() delegation to do the same thing as another method from the
  MRO.
:non-parent-init-called (W0233): *__init__ method from a non direct base class %r is called*
  Used when an __init__ method is called on a class which is not in the direct
  ancestors for the analysed class.
:super-init-not-called (W0231): *__init__ method from base class %r is not called*
  Used when an ancestor class method has an __init__ method which is not called
  by a derived class.
:property-with-parameters (R0206): *Cannot have defined parameters for properties*
  Used when we detect that a property also has parameters, which are useless,
  given that properties cannot be called with additional arguments.
:useless-object-inheritance (R0205): *Class %r inherits from object, can be safely removed from bases in python3*
  Used when a class inherit from object, which under python3 is implicit, hence
  can be safely removed from bases.
:no-classmethod-decorator (R0202): *Consider using a decorator instead of calling classmethod*
  Used when a class method is defined without using the decorator syntax.
:no-staticmethod-decorator (R0203): *Consider using a decorator instead of calling staticmethod*
  Used when a static method is defined without using the decorator syntax.
:single-string-used-for-slots (C0205): *Class __slots__ should be a non-string iterable*
  Used when a class __slots__ is a simple string, rather than an iterable.
:bad-classmethod-argument (C0202): *Class method %s should have %s as first argument*
  Used when a class method has a first argument named differently than the
  value specified in valid-classmethod-first-arg option (default to "cls"),
  recommended to easily differentiate them from regular instance methods.
:bad-mcs-classmethod-argument (C0204): *Metaclass class method %s should have %s as first argument*
  Used when a metaclass class method has a first argument named differently
  than the value specified in valid-metaclass-classmethod-first-arg option
  (default to "mcs"), recommended to easily differentiate them from regular
  instance methods.
:bad-mcs-method-argument (C0203): *Metaclass method %s should have %s as first argument*
  Used when a metaclass method has a first argument named differently than the
  value specified in valid-classmethod-first-arg option (default to "cls"),
  recommended to easily differentiate them from regular instance methods.
:method-check-failed (F0202): *Unable to check methods signature (%s / %s)*
  Used when Pylint has been unable to check methods signature compatibility for
  an unexpected reason. Please report this kind if you don't make sense of it.


Dataclass checker
~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``dataclass``.

Dataclass checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^
:invalid-field-call (E3701): *Invalid usage of field(), %s*
  The dataclasses.field() specifier should only be used as the value of an
  assignment within a dataclass, or within the make_dataclass() function.


Design checker
~~~~~~~~~~~~~~

Verbatim name of the checker is ``design``.

See also :ref:`design checker's options' documentation <design-options>`

Design checker Messages
^^^^^^^^^^^^^^^^^^^^^^^
:too-few-public-methods (R0903): *Too few public methods (%s/%s)*
  Used when class has too few public methods, so be sure it's really worth it.
:too-many-ancestors (R0901): *Too many ancestors (%s/%s)*
  Used when class has too many parent classes, try to reduce this to get a
  simpler (and so easier to use) class.
:too-many-arguments (R0913): *Too many arguments (%s/%s)*
  Used when a function or method takes too many arguments.
:too-many-boolean-expressions (R0916): *Too many boolean expressions in if statement (%s/%s)*
  Used when an if statement contains too many boolean expressions.
:too-many-branches (R0912): *Too many branches (%s/%s)*
  Used when a function or method has too many branches, making it hard to
  follow.
:too-many-instance-attributes (R0902): *Too many instance attributes (%s/%s)*
  Used when class has too many instance attributes, try to reduce this to get a
  simpler (and so easier to use) class.
:too-many-locals (R0914): *Too many local variables (%s/%s)*
  Used when a function or method has too many local variables.
:too-many-positional-arguments (R0917): *Too many positional arguments (%s/%s)*
  Used when a function has too many positional arguments.
:too-many-public-methods (R0904): *Too many public methods (%s/%s)*
  Used when class has too many public methods, try to reduce this to get a
  simpler (and so easier to use) class.
:too-many-return-statements (R0911): *Too many return statements (%s/%s)*
  Used when a function or method has too many return statement, making it hard
  to follow.
:too-many-statements (R0915): *Too many statements (%s/%s)*
  Used when a function or method has too many statements. You should then split
  it in smaller functions / methods.


Exceptions checker
~~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``exceptions``.

See also :ref:`exceptions checker's options' documentation <exceptions-options>`

Exceptions checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^
:bad-except-order (E0701): *Bad except clauses order (%s)*
  Used when except clauses are not in the correct order (from the more specific
  to the more generic). If you don't fix the order, some exceptions may not be
  caught by the most specific handler.
:catching-non-exception (E0712): *Catching an exception which doesn't inherit from Exception: %s*
  Used when a class which doesn't inherit from Exception is used as an
  exception in an except clause.
:bad-exception-cause (E0705): *Exception cause set to something which is not an exception, nor None*
  Used when using the syntax "raise ... from ...", where the exception cause is
  not an exception, nor None.
:notimplemented-raised (E0711): *NotImplemented raised - should raise NotImplementedError*
  Used when NotImplemented is raised instead of NotImplementedError
:raising-bad-type (E0702): *Raising %s while only classes or instances are allowed*
  Used when something which is neither a class nor an instance is raised (i.e.
  a `TypeError` will be raised).
:raising-non-exception (E0710): *Raising a class which doesn't inherit from BaseException*
  Used when a class which doesn't inherit from BaseException is raised.
:misplaced-bare-raise (E0704): *The raise statement is not inside an except clause*
  Used when a bare raise is not used inside an except clause. This generates an
  error, since there are no active exceptions to be reraised. An exception to
  this rule is represented by a bare raise inside a finally clause, which might
  work, as long as an exception is raised inside the try block, but it is
  nevertheless a code smell that must not be relied upon.
:duplicate-except (W0705): *Catching previously caught exception type %s*
  Used when an except catches a type that was already caught by a previous
  handler.
:broad-exception-caught (W0718): *Catching too general exception %s*
  If you use a naked ``except Exception:`` clause, you might end up catching
  exceptions other than the ones you expect to catch. This can hide bugs or
  make it harder to debug programs when unrelated errors are hidden.
:raise-missing-from (W0707): *Consider explicitly re-raising using %s'%s from %s'*
  Python's exception chaining shows the traceback of the current exception, but
  also of the original exception. When you raise a new exception after another
  exception was caught it's likely that the second exception is a friendly re-
  wrapping of the first exception. In such cases `raise from` provides a better
  link between the two tracebacks in the final error.
:raising-format-tuple (W0715): *Exception arguments suggest string formatting might be intended*
  Used when passing multiple arguments to an exception constructor, the first
  of them a string literal containing what appears to be placeholders intended
  for formatting
:binary-op-exception (W0711): *Exception to catch is the result of a binary "%s" operation*
  Used when the exception to catch is of the form "except A or B:". If
  intending to catch multiple, rewrite as "except (A, B):"
:wrong-exception-operation (W0716): *Invalid exception operation. %s*
  Used when an operation is done against an exception, but the operation is not
  valid for the exception in question. Usually emitted when having binary
  operations between exceptions in except handlers.
:bare-except (W0702): *No exception type(s) specified*
  A bare ``except:`` clause will catch ``SystemExit`` and ``KeyboardInterrupt``
  exceptions, making it harder to interrupt a program with ``Control-C``, and
  can disguise other problems. If you want to catch all exceptions that signal
  program errors, use ``except Exception:`` (bare except is equivalent to
  ``except BaseException:``).
:broad-exception-raised (W0719): *Raising too general exception: %s*
  Raising exceptions that are too generic force you to catch exceptions
  generically too. It will force you to use a naked ``except Exception:``
  clause. You might then end up catching exceptions other than the ones you
  expect to catch. This can hide bugs or make it harder to debug programs when
  unrelated errors are hidden.
:try-except-raise (W0706): *The except handler raises immediately*
  Used when an except handler uses raise as its first or only operator. This is
  useless because it raises back the exception immediately. Remove the raise
  operator or the entire try-except-raise block!


Format checker
~~~~~~~~~~~~~~

Verbatim name of the checker is ``format``.

See also :ref:`format checker's options' documentation <format-options>`

Format checker Messages
^^^^^^^^^^^^^^^^^^^^^^^
:bad-indentation (W0311): *Bad indentation. Found %s %s, expected %s*
  Used when an unexpected number of indentation's tabulations or spaces has
  been found.
:unnecessary-semicolon (W0301): *Unnecessary semicolon*
  Used when a statement is ended by a semi-colon (";"), which isn't necessary
  (that's python, not C ;).
:missing-final-newline (C0304): *Final newline missing*
  Used when the last line in a file is missing a newline.
:line-too-long (C0301): *Line too long (%s/%s)*
  Used when a line is longer than a given number of characters.
:mixed-line-endings (C0327): *Mixed line endings LF and CRLF*
  Used when there are mixed (LF and CRLF) newline signs in a file.
:multiple-statements (C0321): *More than one statement on a single line*
  Used when more than on statement are found on the same line.
:too-many-lines (C0302): *Too many lines in module (%s/%s)*
  Used when a module has too many lines, reducing its readability.
:trailing-newlines (C0305): *Trailing newlines*
  Used when there are trailing blank lines in a file.
:trailing-whitespace (C0303): *Trailing whitespace*
  Used when there is whitespace between the end of a line and the newline.
:unexpected-line-ending-format (C0328): *Unexpected line ending format. There is '%s' while it should be '%s'.*
  Used when there is different newline than expected.
:superfluous-parens (C0325): *Unnecessary parens after %r keyword*
  Used when a single item in parentheses follows an if, for, or other keyword.


Imports checker
~~~~~~~~~~~~~~~

Verbatim name of the checker is ``imports``.

See also :ref:`imports checker's options' documentation <imports-options>`

Imports checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^
:relative-beyond-top-level (E0402): *Attempted relative import beyond top-level package*
  Used when a relative import tries to access too many levels in the current
  package.
:import-error (E0401): *Unable to import %s*
  Used when pylint has been unable to import a module.
:deprecated-module (W4901): *Deprecated module %r*
  A module marked as deprecated is imported.
:import-self (W0406): *Module import itself*
  Used when a module is importing itself.
:preferred-module (W0407): *Prefer importing %r instead of %r*
  Used when a module imported has a preferred replacement module.
:reimported (W0404): *Reimport %r (imported line %s)*
  Used when a module is imported more than once.
:shadowed-import (W0416): *Shadowed %r (imported line %s)*
  Used when a module is aliased with a name that shadows another import.
:wildcard-import (W0401): *Wildcard import %s*
  Used when `from module import *` is detected.
:misplaced-future (W0410): *__future__ import is not the first non docstring statement*
  Python 2.5 and greater require __future__ import to be the first non
  docstring statement in the module.
:cyclic-import (R0401): *Cyclic import (%s)*
  Used when a cyclic import between two or more modules is detected.
:consider-using-from-import (R0402): *Use 'from %s import %s' instead*
  Emitted when a submodule of a package is imported and aliased with the same
  name, e.g., instead of ``import concurrent.futures as futures`` use ``from
  concurrent import futures``.
:wrong-import-order (C0411): *%s should be placed before %s*
  Used when PEP8 import order is not respected (standard imports first, then
  third-party libraries, then local imports).
:wrong-import-position (C0413): *Import "%s" should be placed at the top of the module*
  Used when code and imports are mixed.
:useless-import-alias (C0414): *Import alias does not rename original package*
  Used when an import alias is same as original package, e.g., using import
  numpy as numpy instead of import numpy as np.
:import-outside-toplevel (C0415): *Import outside toplevel (%s)*
  Used when an import statement is used anywhere other than the module
  toplevel. Move this import to the top of the file.
:ungrouped-imports (C0412): *Imports from package %s are not grouped*
  Used when imports are not grouped by packages.
:multiple-imports (C0410): *Multiple imports on one line (%s)*
  Used when import statement importing multiple modules is detected.

Imports checker Reports
^^^^^^^^^^^^^^^^^^^^^^^
:RP0401: External dependencies
:RP0402: Modules dependencies graph


Lambda-Expressions checker
~~~~~~~~~~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``lambda-expressions``.

Lambda-Expressions checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:unnecessary-lambda-assignment (C3001): *Lambda expression assigned to a variable. Define a function using the "def" keyword instead.*
  Used when a lambda expression is assigned to variable rather than defining a
  standard function with the "def" keyword.
:unnecessary-direct-lambda-call (C3002): *Lambda expression called directly. Execute the expression inline instead.*
  Used when a lambda expression is directly called rather than executing its
  contents inline.


Logging checker
~~~~~~~~~~~~~~~

Verbatim name of the checker is ``logging``.

See also :ref:`logging checker's options' documentation <logging-options>`

Logging checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^
:logging-format-truncated (E1201): *Logging format string ends in middle of conversion specifier*
  Used when a logging statement format string terminates before the end of a
  conversion specifier.
:logging-too-few-args (E1206): *Not enough arguments for logging format string*
  Used when a logging format string is given too few arguments.
:logging-too-many-args (E1205): *Too many arguments for logging format string*
  Used when a logging format string is given too many arguments.
:logging-unsupported-format (E1200): *Unsupported logging format character %r (%#02x) at index %d*
  Used when an unsupported format character is used in a logging statement
  format string.
:logging-format-interpolation (W1202): *Use %s formatting in logging functions*
  Used when a logging statement has a call form of "logging.<logging
  method>(format_string.format(format_args...))". Use another type of string
  formatting instead. You can use % formatting but leave interpolation to the
  logging function by passing the parameters as arguments. If logging-fstring-
  interpolation is disabled then you can use fstring formatting. If logging-
  not-lazy is disabled then you can use % formatting as normal.
:logging-fstring-interpolation (W1203): *Use %s formatting in logging functions*
  Used when a logging statement has a call form of "logging.<logging
  method>(f"...")".Use another type of string formatting instead. You can use %
  formatting but leave interpolation to the logging function by passing the
  parameters as arguments. If logging-format-interpolation is disabled then you
  can use str.format. If logging-not-lazy is disabled then you can use %
  formatting as normal.
:logging-not-lazy (W1201): *Use %s formatting in logging functions*
  Used when a logging statement has a call form of "logging.<logging
  method>(format_string % (format_args...))". Use another type of string
  formatting instead. You can use % formatting but leave interpolation to the
  logging function by passing the parameters as arguments. If logging-fstring-
  interpolation is disabled then you can use fstring formatting. If logging-
  format-interpolation is disabled then you can use str.format.


Method Args checker
~~~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``method_args``.

See also :ref:`method_args checker's options' documentation <method_args-options>`

Method Args checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:positional-only-arguments-expected (E3102): *`%s()` got some positional-only arguments passed as keyword arguments: %s*
  Emitted when positional-only arguments have been passed as keyword arguments.
  Remove the keywords for the affected arguments in the function call.
:missing-timeout (W3101): *Missing timeout argument for method '%s' can cause your program to hang indefinitely*
  Used when a method needs a 'timeout' parameter in order to avoid waiting for
  a long time. If no timeout is specified explicitly the default value is used.
  For example for 'requests' the program will never time out (i.e. hang
  indefinitely).


Metrics checker
~~~~~~~~~~~~~~~

Verbatim name of the checker is ``metrics``.

Metrics checker Reports
^^^^^^^^^^^^^^^^^^^^^^^
:RP0701: Raw metrics


Miscellaneous checker
~~~~~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``miscellaneous``.

See also :ref:`miscellaneous checker's options' documentation <miscellaneous-options>`

Miscellaneous checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:fixme (W0511):
  Used when a warning note as FIXME or XXX is detected.
:use-symbolic-message-instead (I0023):
  Used when a message is enabled or disabled by id.


Modified Iteration checker
~~~~~~~~~~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``modified_iteration``.

Modified Iteration checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:modified-iterating-dict (E4702): *Iterated dict '%s' is being modified inside for loop body, iterate through a copy of it instead.*
  Emitted when items are added or removed to a dict being iterated through.
  Doing so raises a RuntimeError.
:modified-iterating-set (E4703): *Iterated set '%s' is being modified inside for loop body, iterate through a copy of it instead.*
  Emitted when items are added or removed to a set being iterated through.
  Doing so raises a RuntimeError.
:modified-iterating-list (W4701): *Iterated list '%s' is being modified inside for loop body, consider iterating through a copy of it instead.*
  Emitted when items are added or removed to a list being iterated through.
  Doing so can result in unexpected behaviour, that is why it is preferred to
  use a copy of the list.


Nested Min Max checker
~~~~~~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``nested_min_max``.

Nested Min Max checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:nested-min-max (W3301): *Do not use nested call of '%s'; it's possible to do '%s' instead*
  Nested calls ``min(1, min(2, 3))`` can be rewritten as ``min(1, 2, 3)``.


Newstyle checker
~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``newstyle``.

Newstyle checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^
:bad-super-call (E1003): *Bad first argument %r given to super()*
  Used when another argument than the current class is given as first argument
  of the super builtin.


Nonascii-Checker checker
~~~~~~~~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``nonascii-checker``.

Nonascii-Checker checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:non-ascii-file-name (W2402): *%s name "%s" contains a non-ASCII character.*
  Under python 3.5, PEP 3131 allows non-ascii identifiers, but not non-ascii
  file names.Since Python 3.5, even though Python supports UTF-8 files, some
  editors or tools don't.
:non-ascii-name (C2401): *%s name "%s" contains a non-ASCII character, consider renaming it.*
  Used when the name contains at least one non-ASCII unicode character. See
  https://peps.python.org/pep-0672/#confusing-features for a background why
  this could be bad. If your programming guideline defines that you are
  programming in English, then there should be no need for non ASCII characters
  in Python Names. If not you can simply disable this check.
:non-ascii-module-import (C2403): *%s name "%s" contains a non-ASCII character, use an ASCII-only alias for import.*
  Used when the name contains at least one non-ASCII unicode character. See
  https://peps.python.org/pep-0672/#confusing-features for a background why
  this could be bad. If your programming guideline defines that you are
  programming in English, then there should be no need for non ASCII characters
  in Python Names. If not you can simply disable this check.


Refactoring checker
~~~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``refactoring``.

See also :ref:`refactoring checker's options' documentation <refactoring-options>`

Refactoring checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:simplifiable-condition (R1726): *Boolean condition "%s" may be simplified to "%s"*
  Emitted when a boolean condition is able to be simplified.
:condition-evals-to-constant (R1727): *Boolean condition '%s' will always evaluate to '%s'*
  Emitted when a boolean condition can be simplified to a constant value.
:simplify-boolean-expression (R1709): *Boolean expression may be simplified to %s*
  Emitted when redundant pre-python 2.5 ternary syntax is used.
:consider-using-in (R1714): *Consider merging these comparisons with 'in' by using '%s %sin (%s)'. Use a set instead if elements are hashable.*
  To check if a variable is equal to one of many values, combine the values
  into a set or tuple and check if the variable is contained "in" it instead of
  checking for equality against each of the values. This is faster and less
  verbose.
:consider-merging-isinstance (R1701): *Consider merging these isinstance calls to isinstance(%s, (%s))*
  Used when multiple consecutive isinstance calls can be merged into one.
:use-dict-literal (R1735): *Consider using '%s' instead of a call to 'dict'.*
  Emitted when using dict() to create a dictionary instead of a literal '{ ...
  }'. The literal is faster as it avoids an additional function call.
:consider-using-max-builtin (R1731): *Consider using '%s' instead of unnecessary if block*
  Using the max builtin instead of a conditional improves readability and
  conciseness.
:consider-using-min-builtin (R1730): *Consider using '%s' instead of unnecessary if block*
  Using the min builtin instead of a conditional improves readability and
  conciseness.
:consider-using-sys-exit (R1722): *Consider using 'sys.exit' instead*
  Contrary to 'exit()' or 'quit()', 'sys.exit' does not rely on the site module
  being available (as the 'sys' module is always available).
:consider-using-with (R1732): *Consider using 'with' for resource-allocating operations*
  Emitted if a resource-allocating assignment or call may be replaced by a
  'with' block. By using 'with' the release of the allocated resources is
  ensured even in the case of an exception.
:super-with-arguments (R1725): *Consider using Python 3 style super() without arguments*
  Emitted when calling the super() builtin with the current class and instance.
  On Python 3 these arguments are the default and they can be omitted.
:use-list-literal (R1734): *Consider using [] instead of list()*
  Emitted when using list() to create an empty list instead of the literal [].
  The literal is faster as it avoids an additional function call.
:consider-using-dict-comprehension (R1717): *Consider using a dictionary comprehension*
  Emitted when we detect the creation of a dictionary using the dict() callable
  and a transient list. Although there is nothing syntactically wrong with this
  code, it is hard to read and can be simplified to a dict comprehension. Also
  it is faster since you don't need to create another transient list
:consider-using-generator (R1728): *Consider using a generator instead '%s(%s)'*
  If your container can be large using a generator will bring better
  performance.
:consider-using-set-comprehension (R1718): *Consider using a set comprehension*
  Although there is nothing syntactically wrong with this code, it is hard to
  read and can be simplified to a set comprehension. Also it is faster since
  you don't need to create another transient list
:consider-using-get (R1715): *Consider using dict.get for getting values from a dict if a key is present or a default if not*
  Using the builtin dict.get for getting a value from a dictionary if a key is
  present or a default if not, is simpler and considered more idiomatic,
  although sometimes a bit slower
:consider-using-join (R1713): *Consider using str.join(sequence) for concatenating strings from an iterable*
  Using str.join(sequence) is faster, uses less memory and increases
  readability compared to for-loop iteration.
:consider-using-ternary (R1706): *Consider using ternary (%s)*
  Used when one of known pre-python 2.5 ternary syntax is used.
:consider-swap-variables (R1712): *Consider using tuple unpacking for swapping variables*
  You do not have to use a temporary variable in order to swap variables. Using
  "tuple unpacking" to directly swap variables makes the intention more clear.
:trailing-comma-tuple (R1707): *Disallow trailing comma tuple*
  In Python, a tuple is actually created by the comma symbol, not by the
  parentheses. Unfortunately, one can actually create a tuple by misplacing a
  trailing comma, which can lead to potential weird bugs in your code. You
  should always use parentheses explicitly for creating a tuple.
:stop-iteration-return (R1708): *Do not raise StopIteration in generator, use return statement instead*
  According to PEP479, the raise of StopIteration to end the loop of a
  generator may lead to hard to find bugs. This PEP specify that raise
  StopIteration has to be replaced by a simple return statement
:inconsistent-return-statements (R1710): *Either all return statements in a function should return an expression, or none of them should.*
  According to PEP8, if any return statement returns an expression, any return
  statements where no value is returned should explicitly state this as return
  None, and an explicit return statement should be present at the end of the
  function (if reachable)
:redefined-argument-from-local (R1704): *Redefining argument with the local name %r*
  Used when a local name is redefining an argument, which might suggest a
  potential error. This is taken in account only for a handful of name binding
  operations, such as for iteration, with statement assignment and exception
  handler assignment.
:chained-comparison (R1716): *Simplify chained comparison between the operands*
  This message is emitted when pylint encounters boolean operation like "a < b
  and b < c", suggesting instead to refactor it to "a < b < c"
:simplifiable-if-expression (R1719): *The if expression can be replaced with %s*
  Used when an if expression can be replaced with 'bool(test)' or simply 'test'
  if the boolean cast is implicit.
:simplifiable-if-statement (R1703): *The if statement can be replaced with %s*
  Used when an if statement can be replaced with 'bool(test)'.
:too-many-nested-blocks (R1702): *Too many nested blocks (%s/%s)*
  Used when a function or a method has too many nested blocks. This makes the
  code less understandable and maintainable.
:no-else-break (R1723): *Unnecessary "%s" after "break", %s*
  Used in order to highlight an unnecessary block of code following an if
  containing a break statement. As such, it will warn when it encounters an
  else following a chain of ifs, all of them containing a break statement.
:no-else-continue (R1724): *Unnecessary "%s" after "continue", %s*
  Used in order to highlight an unnecessary block of code following an if
  containing a continue statement. As such, it will warn when it encounters an
  else following a chain of ifs, all of them containing a continue statement.
:no-else-raise (R1720): *Unnecessary "%s" after "raise", %s*
  Used in order to highlight an unnecessary block of code following an if
  containing a raise statement. As such, it will warn when it encounters an
  else following a chain of ifs, all of them containing a raise statement.
:no-else-return (R1705): *Unnecessary "%s" after "return", %s*
  Used in order to highlight an unnecessary block of code following an if
  containing a return statement. As such, it will warn when it encounters an
  else following a chain of ifs, all of them containing a return statement.
:unnecessary-dict-index-lookup (R1733): *Unnecessary dictionary index lookup, use '%s' instead*
  Emitted when iterating over the dictionary items (key-item pairs) and
  accessing the value by index lookup. The value can be accessed directly
  instead.
:unnecessary-list-index-lookup (R1736): *Unnecessary list index lookup, use '%s' instead*
  Emitted when iterating over an enumeration and accessing the value by index
  lookup. The value can be accessed directly instead.
:unnecessary-comprehension (R1721): *Unnecessary use of a comprehension, use %s instead.*
  Instead of using an identity comprehension, consider using the list, dict or
  set constructor. It is faster and simpler.
:use-yield-from (R1737): *Use 'yield from' directly instead of yielding each element one by one*
  Yielding directly from the iterator is faster and arguably cleaner code than
  yielding each element one by one in the loop.
:use-a-generator (R1729): *Use a generator instead '%s(%s)'*
  Comprehension inside of 'any', 'all', 'max', 'min' or 'sum' is unnecessary. A
  generator would be sufficient and faster.
:useless-return (R1711): *Useless return at end of function or method*
  Emitted when a single "return" or "return None" statement is found at the end
  of function or method definition. This statement can safely be removed
  because Python will implicitly return None
:use-implicit-booleaness-not-comparison (C1803): *"%s" can be simplified to "%s", if it is strictly a sequence, as an empty %s is falsey*
  Empty sequences are considered false in a boolean context. Following this
  check blindly in weakly typed code base can create hard to debug issues. If
  the value can be something else that is falsey but not a sequence (for
  example ``None``, an empty string, or ``0``) the code will not be equivalent.
:use-implicit-booleaness-not-comparison-to-string (C1804): *"%s" can be simplified to "%s", if it is strictly a string, as an empty string is falsey*
  Empty string are considered false in a boolean context. Following this check
  blindly in weakly typed code base can create hard to debug issues. If the
  value can be something else that is falsey but not a string (for example
  ``None``, an empty sequence, or ``0``) the code will not be equivalent.
:use-implicit-booleaness-not-comparison-to-zero (C1805): *"%s" can be simplified to "%s", if it is strictly an int, as 0 is falsey*
  0 is considered false in a boolean context. Following this check blindly in
  weakly typed code base can create hard to debug issues. If the value can be
  something else that is falsey but not an int (for example ``None``, an empty
  string, or an empty sequence) the code will not be equivalent.
:unnecessary-negation (C0117): *Consider changing "%s" to "%s"*
  Used when a boolean expression contains an unneeded negation, e.g. when two
  negation operators cancel each other out.
:consider-iterating-dictionary (C0201): *Consider iterating the dictionary directly instead of calling .keys()*
  Emitted when the keys of a dictionary are iterated through the ``.keys()``
  method or when ``.keys()`` is used for a membership check. It is enough to
  iterate through the dictionary itself, ``for key in dictionary``. For
  membership checks, ``if key in dictionary`` is faster.
:consider-using-dict-items (C0206): *Consider iterating with .items()*
  Emitted when iterating over the keys of a dictionary and accessing the value
  by index lookup. Both the key and value can be accessed by iterating using
  the .items() method of the dictionary instead.
:consider-using-enumerate (C0200): *Consider using enumerate instead of iterating with range and len*
  Emitted when code that iterates with range and len is encountered. Such code
  can be simplified by using the enumerate builtin.
:use-implicit-booleaness-not-len (C1802): *Do not use `len(SEQUENCE)` without comparison to determine if a sequence is empty*
  Empty sequences are considered false in a boolean context. You can either
  remove the call to 'len' (``if not x``) or compare the length against a
  scalar (``if len(x) > 1``).
:consider-using-f-string (C0209): *Formatting a regular string which could be an f-string*
  Used when we detect a string that is being formatted with format() or % which
  could potentially be an f-string. The use of f-strings is preferred. Requires
  Python 3.6 and ``py-version >= 3.6``.
:use-maxsplit-arg (C0207): *Use %s instead*
  Emitted when accessing only the first or last element of str.split(). The
  first and last element can be accessed by using str.split(sep, maxsplit=1)[0]
  or str.rsplit(sep, maxsplit=1)[-1] instead.
:use-sequence-for-iteration (C0208): *Use a sequence type when iterating over values*
  When iterating over values, sequence types (e.g., ``lists``, ``tuples``,
  ``ranges``) are more efficient than ``sets``.


Similarities checker
~~~~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``similarities``.

See also :ref:`similarities checker's options' documentation <similarities-options>`

Similarities checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:duplicate-code (R0801): *Similar lines in %s files*
  Indicates that a set of similar lines has been detected among multiple file.
  This usually means that the code should be refactored to avoid this
  duplication.

Similarities checker Reports
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:RP0801: Duplication


Spelling checker
~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``spelling``.

See also :ref:`spelling checker's options' documentation <spelling-options>`

Spelling checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^
:invalid-characters-in-docstring (C0403): *Invalid characters %r in a docstring*
  Used when a word in docstring cannot be checked by enchant.
:wrong-spelling-in-comment (C0401): *Wrong spelling of a word '%s' in a comment:*
  Used when a word in comment is not spelled correctly.
:wrong-spelling-in-docstring (C0402): *Wrong spelling of a word '%s' in a docstring:*
  Used when a word in docstring is not spelled correctly.


Stdlib checker
~~~~~~~~~~~~~~

Verbatim name of the checker is ``stdlib``.

Stdlib checker Messages
^^^^^^^^^^^^^^^^^^^^^^^
:invalid-envvar-value (E1507): *%s does not support %s type argument*
  Env manipulation functions support only string type arguments. See
  https://docs.python.org/3/library/os.html#os.getenv.
:singledispatch-method (E1519): *singledispatch decorator should not be used with methods, use singledispatchmethod instead.*
  singledispatch should decorate functions and not class/instance methods. Use
  singledispatchmethod for those cases.
:singledispatchmethod-function (E1520): *singledispatchmethod decorator should not be used with functions, use singledispatch instead.*
  singledispatchmethod should decorate class/instance methods and not
  functions. Use singledispatch for those cases.
:bad-open-mode (W1501): *"%s" is not a valid mode for open.*
  Python supports: r, w, a[, x] modes with b, +, and U (only with r) options.
  See https://docs.python.org/3/library/functions.html#open
:invalid-envvar-default (W1508): *%s default type is %s. Expected str or None.*
  Env manipulation functions return None or str values. Supplying anything
  different as a default may cause bugs. See
  https://docs.python.org/3/library/os.html#os.getenv.
:method-cache-max-size-none (W1518): *'lru_cache(maxsize=None)' or 'cache' will keep all method args alive indefinitely, including 'self'*
  By decorating a method with lru_cache or cache the 'self' argument will be
  linked to the function and therefore never garbage collected. Unless your
  instance will never need to be garbage collected (singleton) it is
  recommended to refactor code to avoid this pattern or add a maxsize to the
  cache. The default value for maxsize is 128.
:subprocess-run-check (W1510): *'subprocess.run' used without explicitly defining the value for 'check'.*
  The ``check`` keyword is set to False by default. It means the process
  launched by ``subprocess.run`` can exit with a non-zero exit code and fail
  silently. It's better to set it explicitly to make clear what the error-
  handling behavior is.
:forgotten-debug-statement (W1515): *Leaving functions creating breakpoints in production code is not recommended*
  Calls to breakpoint(), sys.breakpointhook() and pdb.set_trace() should be
  removed from code that is not actively being debugged.
:redundant-unittest-assert (W1503): *Redundant use of %s with constant value %r*
  The first argument of assertTrue and assertFalse is a condition. If a
  constant is passed as parameter, that condition will be always true. In this
  case a warning should be emitted.
:shallow-copy-environ (W1507): *Using copy.copy(os.environ). Use os.environ.copy() instead.*
  os.environ is not a dict object but proxy object, so shallow copy has still
  effects on original object. See https://bugs.python.org/issue15373 for
  reference.
:boolean-datetime (W1502): *Using datetime.time in a boolean context.*
  Using datetime.time in a boolean context can hide subtle bugs when the time
  they represent matches midnight UTC. This behaviour was fixed in Python 3.5.
  See https://bugs.python.org/issue13936 for reference. This message can't be
  emitted when using Python >= 3.5.
:deprecated-argument (W4903): *Using deprecated argument %s of method %s()*
  The argument is marked as deprecated and will be removed in the future.
:deprecated-attribute (W4906): *Using deprecated attribute %r*
  The attribute is marked as deprecated and will be removed in the future.
:deprecated-class (W4904): *Using deprecated class %s of module %s*
  The class is marked as deprecated and will be removed in the future.
:deprecated-decorator (W4905): *Using deprecated decorator %s()*
  The decorator is marked as deprecated and will be removed in the future.
:deprecated-method (W4902): *Using deprecated method %s()*
  The method is marked as deprecated and will be removed in the future.
:unspecified-encoding (W1514): *Using open without explicitly specifying an encoding*
  It is better to specify an encoding when opening documents. Using the system
  default implicitly can create problems on other operating systems. See
  https://peps.python.org/pep-0597/
:subprocess-popen-preexec-fn (W1509): *Using preexec_fn keyword which may be unsafe in the presence of threads*
  The preexec_fn parameter is not safe to use in the presence of threads in
  your application. The child process could deadlock before exec is called. If
  you must use it, keep it trivial! Minimize the number of libraries you call
  into. See https://docs.python.org/3/library/subprocess.html#popen-constructor
:bad-thread-instantiation (W1506): *threading.Thread needs the target function*
  The warning is emitted when a threading.Thread class is instantiated without
  the target function being passed as a kwarg or as a second argument. By
  default, the first parameter is the group param, not the target param.


String checker
~~~~~~~~~~~~~~

Verbatim name of the checker is ``string``.

See also :ref:`string checker's options' documentation <string-options>`

String checker Messages
^^^^^^^^^^^^^^^^^^^^^^^
:bad-string-format-type (E1307): *Argument %r does not match format type %r*
  Used when a type required by format string is not suitable for actual
  argument type
:format-needs-mapping (E1303): *Expected mapping for format string, not %s*
  Used when a format string that uses named conversion specifiers is used with
  an argument that is not a mapping.
:truncated-format-string (E1301): *Format string ends in middle of conversion specifier*
  Used when a format string terminates before the end of a conversion
  specifier.
:missing-format-string-key (E1304): *Missing key %r in format string dictionary*
  Used when a format string that uses named conversion specifiers is used with
  a dictionary that doesn't contain all the keys required by the format string.
:mixed-format-string (E1302): *Mixing named and unnamed conversion specifiers in format string*
  Used when a format string contains both named (e.g. '%(foo)d') and unnamed
  (e.g. '%d') conversion specifiers. This is also used when a named conversion
  specifier contains * for the minimum field width and/or precision.
:too-few-format-args (E1306): *Not enough arguments for format string*
  Used when a format string that uses unnamed conversion specifiers is given
  too few arguments
:bad-str-strip-call (E1310): *Suspicious argument in %s.%s call*
  The argument to a str.{l,r,}strip call contains a duplicate character,
:too-many-format-args (E1305): *Too many arguments for format string*
  Used when a format string that uses unnamed conversion specifiers is given
  too many arguments.
:bad-format-character (E1300): *Unsupported format character %r (%#02x) at index %d*
  Used when an unsupported format character is used in a format string.
:anomalous-unicode-escape-in-string (W1402): *Anomalous Unicode escape in byte string: '%s'. String constant might be missing an r or u prefix.*
  Used when an escape like \u is encountered in a byte string where it has no
  effect.
:anomalous-backslash-in-string (W1401): *Anomalous backslash in string: '%s'. String constant might be missing an r prefix.*
  Used when a backslash is in a literal string but not as an escape.
:duplicate-string-formatting-argument (W1308): *Duplicate string formatting argument %r, consider passing as named argument*
  Used when we detect that a string formatting is repeating an argument instead
  of using named string arguments
:format-combined-specification (W1305): *Format string contains both automatic field numbering and manual field specification*
  Used when a PEP 3101 format string contains both automatic field numbering
  (e.g. '{}') and manual field specification (e.g. '{0}').
:bad-format-string-key (W1300): *Format string dictionary key should be a string, not %s*
  Used when a format string that uses named conversion specifiers is used with
  a dictionary whose keys are not all strings.
:implicit-str-concat (W1404): *Implicit string concatenation found in %s*
  String literals are implicitly concatenated in a literal iterable definition
  : maybe a comma is missing ?
:bad-format-string (W1302): *Invalid format string*
  Used when a PEP 3101 format string is invalid.
:missing-format-attribute (W1306): *Missing format attribute %r in format specifier %r*
  Used when a PEP 3101 format string uses an attribute specifier ({0.length}),
  but the argument passed for formatting doesn't have that attribute.
:missing-format-argument-key (W1303): *Missing keyword argument %r for format string*
  Used when a PEP 3101 format string that uses named fields doesn't receive one
  or more required keywords.
:inconsistent-quotes (W1405): *Quote delimiter %s is inconsistent with the rest of the file*
  Quote delimiters are not used consistently throughout a module (with
  allowances made for avoiding unnecessary escaping).
:redundant-u-string-prefix (W1406): *The u prefix for strings is no longer necessary in Python >=3.0*
  Used when we detect a string with a u prefix. These prefixes were necessary
  in Python 2 to indicate a string was Unicode, but since Python 3.0 strings
  are Unicode by default.
:unused-format-string-argument (W1304): *Unused format argument %r*
  Used when a PEP 3101 format string that uses named fields is used with an
  argument that is not required by the format string.
:unused-format-string-key (W1301): *Unused key %r in format string dictionary*
  Used when a format string that uses named conversion specifiers is used with
  a dictionary that contains keys not required by the format string.
:f-string-without-interpolation (W1309): *Using an f-string that does not have any interpolated variables*
  Used when we detect an f-string that does not use any interpolation
  variables, in which case it can be either a normal string or a bug in the
  code.
:format-string-without-interpolation (W1310): *Using formatting for a string that does not have any interpolated variables*
  Used when we detect a string that does not have any interpolation variables,
  in which case it can be either a normal string without formatting or a bug in
  the code.
:invalid-format-index (W1307): *Using invalid lookup key %r in format specifier %r*
  Used when a PEP 3101 format string uses a lookup specifier ({a[1]}), but the
  argument passed for formatting doesn't contain or doesn't have that key as an
  attribute.


Threading checker
~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``threading``.

Threading checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^
:useless-with-lock (W2101): *'%s()' directly created in 'with' has no effect*
  Used when a new lock instance is created by using with statement which has no
  effect. Instead, an existing instance should be used to acquire lock.


Typecheck checker
~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``typecheck``.

See also :ref:`typecheck checker's options' documentation <typecheck-options>`

Typecheck checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^
:unsupported-assignment-operation (E1137): *%r does not support item assignment*
  Emitted when an object does not support item assignment (i.e. doesn't define
  __setitem__ method).
:unsupported-delete-operation (E1138): *%r does not support item deletion*
  Emitted when an object does not support item deletion (i.e. doesn't define
  __delitem__ method).
:invalid-unary-operand-type (E1130):
  Emitted when a unary operand is used on an object which does not support this
  type of operation.
:unsupported-binary-operation (E1131):
  Emitted when a binary arithmetic operation between two operands is not
  supported.
:no-member (E1101): *%s %r has no %r member%s*
  Used when a variable is accessed for a nonexistent member.
:not-callable (E1102): *%s is not callable*
  Used when an object being called has been inferred to a non callable object.
:unhashable-member (E1143): *'%s' is unhashable and can't be used as a %s in a %s*
  Emitted when a dict key or set member is not hashable (i.e. doesn't define
  __hash__ method).
:await-outside-async (E1142): *'await' should be used within an async function*
  Emitted when await is used outside an async function.
:redundant-keyword-arg (E1124): *Argument %r passed by position and keyword in %s call*
  Used when a function call would result in assigning multiple values to a
  function parameter, one value from a positional argument and one from a
  keyword argument.
:assignment-from-no-return (E1111): *Assigning result of a function call, where the function has no return*
  Used when an assignment is done on a function call but the inferred function
  doesn't return anything.
:assignment-from-none (E1128): *Assigning result of a function call, where the function returns None*
  Used when an assignment is done on a function call but the inferred function
  returns nothing but None.
:not-context-manager (E1129): *Context manager '%s' doesn't implement __enter__ and __exit__.*
  Used when an instance in a with statement doesn't implement the context
  manager protocol(__enter__/__exit__).
:repeated-keyword (E1132): *Got multiple values for keyword argument %r in function call*
  Emitted when a function call got multiple values for a keyword.
:invalid-metaclass (E1139): *Invalid metaclass %r used*
  Emitted whenever we can detect that a class is using, as a metaclass,
  something which might be invalid for using as a metaclass.
:missing-kwoa (E1125): *Missing mandatory keyword argument %r in %s call*
  Used when a function call does not pass a mandatory keyword-only argument.
:no-value-for-parameter (E1120): *No value for argument %s in %s call*
  Used when a function call passes too few arguments.
:not-an-iterable (E1133): *Non-iterable value %s is used in an iterating context*
  Used when a non-iterable value is used in place where iterable is expected
:not-a-mapping (E1134): *Non-mapping value %s is used in a mapping context*
  Used when a non-mapping value is used in place where mapping is expected
:invalid-sequence-index (E1126): *Sequence index is not an int, slice, or instance with __index__*
  Used when a sequence type is indexed with an invalid type. Valid types are
  ints, slices, and objects with an __index__ method.
:invalid-slice-index (E1127): *Slice index is not an int, None, or instance with __index__*
  Used when a slice index is not an integer, None, or an object with an
  __index__ method.
:invalid-slice-step (E1144): *Slice step cannot be 0*
  Used when a slice step is 0 and the object doesn't implement a custom
  __getitem__ method.
:too-many-function-args (E1121): *Too many positional arguments for %s call*
  Used when a function call passes too many positional arguments.
:unexpected-keyword-arg (E1123): *Unexpected keyword argument %r in %s call*
  Used when a function call passes a keyword argument that doesn't correspond
  to one of the function's parameter names.
:dict-iter-missing-items (E1141): *Unpacking a dictionary in iteration without calling .items()*
  Emitted when trying to iterate through a dict without calling .items()
:unsupported-membership-test (E1135): *Value '%s' doesn't support membership test*
  Emitted when an instance in membership test expression doesn't implement
  membership protocol (__contains__/__iter__/__getitem__).
:unsubscriptable-object (E1136): *Value '%s' is unsubscriptable*
  Emitted when a subscripted value doesn't support subscription (i.e. doesn't
  define __getitem__ method or __class_getitem__ for a class).
:kwarg-superseded-by-positional-arg (W1117): *%r will be included in %r since a positional-only parameter with this name already exists*
  Emitted when a function is called with a keyword argument that has the same
  name as a positional-only parameter and the function contains a keyword
  variadic parameter dict.
:keyword-arg-before-vararg (W1113): *Keyword argument before variable positional arguments list in the definition of %s function*
  When defining a keyword argument before variable positional arguments, one
  can end up in having multiple values passed for the aforementioned parameter
  in case the method is called with keyword arguments.
:non-str-assignment-to-dunder-name (W1115): *Non-string value assigned to __name__*
  Emitted when a non-string value is assigned to __name__
:arguments-out-of-order (W1114): *Positional arguments appear to be out of order*
  Emitted when the caller's argument names fully match the parameter names in
  the function signature but do not have the same order.
:isinstance-second-argument-not-valid-type (W1116): *Second argument of isinstance is not a type*
  Emitted when the second argument of an isinstance call is not a type.
:c-extension-no-member (I1101): *%s %r has no %r member%s, but source is unavailable. Consider adding this module to extension-pkg-allow-list if you want to perform analysis based on run-time introspection of living objects.*
  Used when a variable is accessed for non-existent member of C extension. Due
  to unavailability of source static analysis is impossible, but it may be
  performed by introspecting living objects in run-time.


Unicode Checker checker
~~~~~~~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``unicode_checker``.

Unicode Checker checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:bidirectional-unicode (E2502): *Contains control characters that can permit obfuscated code executed differently than displayed*
  bidirectional unicode are typically not displayed characters required to
  display right-to-left (RTL) script (i.e. Chinese, Japanese, Arabic, Hebrew,
  ...) correctly. So can you trust this code? Are you sure it displayed
  correctly in all editors? If you did not write it or your language is not
  RTL, remove the special characters, as they could be used to trick you into
  executing code, that does something else than what it looks like. More
  Information: https://en.wikipedia.org/wiki/Bidirectional_text
  https://trojansource.codes/
:invalid-character-backspace (E2510): *Invalid unescaped character backspace, use "\b" instead.*
  Moves the cursor back, so the character after it will overwrite the character
  before.
:invalid-character-carriage-return (E2511): *Invalid unescaped character carriage-return, use "\r" instead.*
  Moves the cursor to the start of line, subsequent characters overwrite the
  start of the line.
:invalid-character-esc (E2513): *Invalid unescaped character esc, use "\x1B" instead.*
  Commonly initiates escape codes which allow arbitrary control of the
  terminal.
:invalid-character-nul (E2514): *Invalid unescaped character nul, use "\0" instead.*
  Mostly end of input for python.
:invalid-character-sub (E2512): *Invalid unescaped character sub, use "\x1A" instead.*
  Ctrl+Z "End of text" on Windows. Some programs (such as type) ignore the rest
  of the file after it.
:invalid-character-zero-width-space (E2515): *Invalid unescaped character zero-width-space, use "\u200B" instead.*
  Invisible space character could hide real code execution.
:invalid-unicode-codec (E2501): *UTF-16 and UTF-32 aren't backward compatible. Use UTF-8 instead*
  For compatibility use UTF-8 instead of UTF-16/UTF-32. See also
  https://bugs.python.org/issue1503789 for a history of this issue. And
  https://softwareengineering.stackexchange.com/questions/102205/ for some
  possible problems when using UTF-16 for instance.
:bad-file-encoding (C2503): *PEP8 recommends UTF-8 as encoding for Python files*
  PEP8 recommends UTF-8 default encoding for Python files. See
  https://peps.python.org/pep-0008/#source-file-encoding


Unnecessary-Dunder-Call checker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``unnecessary-dunder-call``.

Unnecessary-Dunder-Call checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:unnecessary-dunder-call (C2801): *Unnecessarily calls dunder method %s. %s.*
  Used when a dunder method is manually called instead of using the
  corresponding function/method/operator.


Unnecessary Ellipsis checker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``unnecessary_ellipsis``.

Unnecessary Ellipsis checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:unnecessary-ellipsis (W2301): *Unnecessary ellipsis constant*
  Used when the ellipsis constant is encountered and can be avoided. A line of
  code consisting of an ellipsis is unnecessary if there is a docstring on the
  preceding line or if there is a statement in the same scope.


Unsupported Version checker
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``unsupported_version``.

Unsupported Version checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:using-assignment-expression-in-unsupported-version (W2605): *Assignment expression is not supported by all versions included in the py-version setting*
  Used when the py-version set by the user is lower than 3.8 and pylint
  encounters an assignment expression (walrus) operator.
:using-exception-groups-in-unsupported-version (W2603): *Exception groups are not supported by all versions included in the py-version setting*
  Used when the py-version set by the user is lower than 3.11 and pylint
  encounters ``except*`` or `ExceptionGroup``.
:using-f-string-in-unsupported-version (W2601): *F-strings are not supported by all versions included in the py-version setting*
  Used when the py-version set by the user is lower than 3.6 and pylint
  encounters an f-string.
:using-generic-type-syntax-in-unsupported-version (W2604): *Generic type syntax (PEP 695) is not supported by all versions included in the py-version setting*
  Used when the py-version set by the user is lower than 3.12 and pylint
  encounters generic type syntax.
:using-positional-only-args-in-unsupported-version (W2606): *Positional-only arguments are not supported by all versions included in the py-version setting*
  Used when the py-version set by the user is lower than 3.8 and pylint
  encounters positional-only arguments.
:using-final-decorator-in-unsupported-version (W2602): *typing.final is not supported by all versions included in the py-version setting*
  Used when the py-version set by the user is lower than 3.8 and pylint
  encounters a ``typing.final`` decorator.


Variables checker
~~~~~~~~~~~~~~~~~

Verbatim name of the checker is ``variables``.

See also :ref:`variables checker's options' documentation <variables-options>`

Variables checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^
:unpacking-non-sequence (E0633): *Attempting to unpack a non-sequence%s*
  Used when something which is not a sequence is used in an unpack assignment
:invalid-all-format (E0605): *Invalid format for __all__, must be tuple or list*
  Used when __all__ has an invalid format.
:potential-index-error (E0643): *Invalid index for iterable length*
  Emitted when an index used on an iterable goes beyond the length of that
  iterable.
:invalid-all-object (E0604): *Invalid object %r in __all__, must contain only strings*
  Used when an invalid (non-string) object occurs in __all__.
:no-name-in-module (E0611): *No name %r in module %r*
  Used when a name cannot be found in a module.
:possibly-used-before-assignment (E0606): *Possibly using variable %r before assignment*
  Emitted when a local variable is accessed before its assignment took place in
  both branches of an if/else switch.
:undefined-variable (E0602): *Undefined variable %r*
  Used when an undefined variable is accessed.
:undefined-all-variable (E0603): *Undefined variable name %r in __all__*
  Used when an undefined variable name is referenced in __all__.
:used-before-assignment (E0601): *Using variable %r before assignment*
  Emitted when a local variable is accessed before its assignment took place.
  Assignments in try blocks are assumed not to have occurred when evaluating
  associated except/finally blocks. Assignments in except blocks are assumed
  not to have occurred when evaluating statements outside the block, except
  when the associated try block contains a return statement.
:cell-var-from-loop (W0640): *Cell variable %s defined in loop*
  A variable used in a closure is defined in a loop. This will result in all
  closures using the same value for the closed-over variable.
:global-variable-undefined (W0601): *Global variable %r undefined at the module level*
  Used when a variable is defined through the "global" statement but the
  variable is not defined in the module scope.
:self-cls-assignment (W0642): *Invalid assignment to %s in method*
  Invalid assignment to self or cls in instance or class method respectively.
:unbalanced-dict-unpacking (W0644): *Possible unbalanced dict unpacking with %s: left side has %d label%s, right side has %d value%s*
  Used when there is an unbalanced dict unpacking in assignment or for loop
:unbalanced-tuple-unpacking (W0632): *Possible unbalanced tuple unpacking with sequence %s: left side has %d label%s, right side has %d value%s*
  Used when there is an unbalanced tuple unpacking in assignment
:possibly-unused-variable (W0641): *Possibly unused variable %r*
  Used when a variable is defined but might not be used. The possibility comes
  from the fact that locals() might be used, which could consume or not the
  said variable
:redefined-builtin (W0622): *Redefining built-in %r*
  Used when a variable or function override a built-in.
:redefined-outer-name (W0621): *Redefining name %r from outer scope (line %s)*
  Used when a variable's name hides a name defined in an outer scope or except
  handler.
:unused-import (W0611): *Unused %s*
  Used when an imported module or variable is not used.
:unused-argument (W0613): *Unused argument %r*
  Used when a function or method argument is not used.
:unused-wildcard-import (W0614): *Unused import(s) %s from wildcard import of %s*
  Used when an imported module or variable is not used from a `'from X import
  *'` style import.
:unused-variable (W0612): *Unused variable %r*
  Used when a variable is defined but not used.
:global-variable-not-assigned (W0602): *Using global for %r but no assignment is done*
  When a variable defined in the global scope is modified in an inner scope,
  the 'global' keyword is required in the inner scope only if there is an
  assignment operation done in the inner scope.
:undefined-loop-variable (W0631): *Using possibly undefined loop variable %r*
  Used when a loop variable (i.e. defined by a for loop or a list comprehension
  or a generator expression) is used outside the loop.
:global-statement (W0603): *Using the global statement*
  Used when you use the "global" statement to update a global variable. Pylint
  discourages its usage. That doesn't mean you cannot use it!
:global-at-module-level (W0604): *Using the global statement at the module level*
  Used when you use the "global" statement at the module level since it has no
  effect.
