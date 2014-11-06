.. -*- coding: utf-8 -*-

===============
 Configuration
===============

Naming Styles
-------------

Pylint recognizes a number of different name types internally. With a few
exceptions, the type of the name is governed by the location the assignment to a
name is found in, and not the type of object assigned.

``module``
   Module and package names, same as the file names.
``const``
   Module-level constants, any variable defined at module level that is not bound to a class object.
``class``
   Names in ``class`` statements, as well as names bound to class objects at module level.
``function``
   Functions, toplevel or nested in functions or methods.
``method``
   Methods, functions defined in class bodies. Includes static and class methods.
``attr``
   Attributes created on class instances inside methods.
``argument``
   Arguments to any function type, including lambdas.
``variable``
   Local variables in function scopes.
``class-attribute``
   Attributes defined in class bodies.
``inlinevar``
   Loop variables in list comprehensions and generator expressions.

For each naming style, a separate regular expression matching valid names of
this type can be defined. By default, the regular expressions will enforce PEP8
names.

Regular expressions for the names are anchored at the beginning, any anchor for
the end must be supplied explicitly. Any name not matching the regular
expression will lead to an instance of ``invalid-name``.


.. option:: --module-rgx=<regex>

   Default value: ``[a-z_][a-z0-9_]{2,30}$``

.. option:: --const-rgx=<regex>

   Default value: ``[a-z_][a-z0-9_]{2,30}$``

.. option:: --class-rgx=<regex>

   Default value: ``'[A-Z_][a-zA-Z0-9]+$``

.. option:: --function-rgx=<regex>

   Default value: ``[a-z_][a-z0-9_]{2,30}$``

.. option:: --method-rgx=<regex>

   Default value: ``[a-z_][a-z0-9_]{2,30}$``

.. option:: --attr-rgx=<regex>

   Default value: ``[a-z_][a-z0-9_]{2,30}$``

.. option:: --argument-rgx=<regex>

   Default value: ``[a-z_][a-z0-9_]{2,30}$``

.. option:: --variable-rgx=<regex>

   Default value: ``[a-z_][a-z0-9_]{2,30}$``

.. option:: --class-attribute-rgx=<regex>

   Default value: ``([A-Za-z_][A-Za-z0-9_]{2,30}|(__.*__))$``

.. option:: --inlinevar-rgx=<regex>

   Default value: ``[A-Za-z_][A-Za-z0-9_]*$``

Multiple Naming Styles
^^^^^^^^^^^^^^^^^^^^^^

Large code bases that have been worked on for multiple years often exhibit an
evolution in style as well. In some cases, modules can be in the same package,
but still have different naming style based on the stratum they belong to.
However, intra-module consistency should still be required, to make changes
inside a single file easier. For this case, Pylint supports regular expression
with several named capturing group.

Rather than emitting name warnings immediately, Pylint will determine the
prevalent naming style inside each module and enforce it on all names.

Consider the following (simplified) example::

   pylint --function-rgx='(?:(?P<snake>[a-z_]+)|(?P<camel>_?[A-Z]+))$' sample.py

The regular expression defines two naming styles, ``snake`` for snake-case
names, and ``camel`` for camel-case names.

In ``sample.py``, the function name on line 1 and 7 will mark the module
and enforce the match of named group ``snake`` for the remaining names in
the module::

   def valid_snake_case(arg):
      ...

   def InvalidCamelCase(arg):
      ...

   def more_valid_snake_case(arg):
    ...

Because of this, the name on line 4 will trigger an ``invalid-name`` warning,
even though the name matches the given regex.

Matches named ``exempt`` or ``ignore`` can be used for non-tainting names, to
prevent built-in or interface-dictated names to trigger certain naming styles.

.. option:: --name-group=<name1:name2:...,...>

   Default value: empty

   Format: comma-separated groups of colon-separated names.

   This option can be used to combine name styles. For example, ``function:method`` enforces that functions and methods use the same style, and a style triggered by either name type carries over to the other. This requires that the regular expression for the combined name types use the same group names.

Name Hints
^^^^^^^^^^

.. option:: --include-naming-hint=y|n

   Default: off

   Include a hint for the correct name format with every ``invalid-name`` warning.

   Name hints default to the regular expression, but can be separately configured with the ``--<name-type>-hint`` options.
