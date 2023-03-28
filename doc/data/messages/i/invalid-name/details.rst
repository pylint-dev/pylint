Pylint recognizes a number of different name types internally. With a few
exceptions, the type of the name is governed by the location the assignment to a
name is found in, and not the type of object assigned.

+--------------------+---------------------------------------------------------------------------------------------------+
| Name Type          | Description                                                                                       |
+====================+===================================================================================================+
| ``module``         | Module and package names, same as the file names.                                                 |
+--------------------+---------------------------------------------------------------------------------------------------+
| ``const``          | Module-level constants, any variable defined at module level that is not bound to a class object. |
+--------------------+---------------------------------------------------------------------------------------------------+
| ``class``          | Names in ``class`` statements, as well as names bound to class objects at module level.           |
+--------------------+---------------------------------------------------------------------------------------------------+
| ``function``       | Functions, toplevel or nested in functions or methods.                                            |
+--------------------+---------------------------------------------------------------------------------------------------+
| ``method``         | Methods, functions defined in class bodies. Includes static and class methods.                    |
+--------------------+---------------------------------------------------------------------------------------------------+
| ``attr``           | Attributes created on class instances inside methods.                                             |
+--------------------+---------------------------------------------------------------------------------------------------+
| ``argument``       | Arguments to any function type, including lambdas.                                                |
+--------------------+---------------------------------------------------------------------------------------------------+
| ``variable``       | Local variables in function scopes.                                                               |
+--------------------+---------------------------------------------------------------------------------------------------+
| ``class-attribute``| Attributes defined in class bodies.                                                               |
+--------------------+---------------------------------------------------------------------------------------------------+
| ``class-const``    | Enum constants and class variables annotated with ``ClassVar``                                    |
+--------------------+---------------------------------------------------------------------------------------------------+
| ``inlinevar``      | Loop variables in list comprehensions and generator expressions.                                  |
+--------------------+---------------------------------------------------------------------------------------------------+
| ``typevar``        | Type variable declared with ``TypeVar``.                                                          |
+--------------------+---------------------------------------------------------------------------------------------------+
| ``typealias``      | Type alias declared with ``TypeAlias`` or assignments of ``Union``.                               |
+--------------------+---------------------------------------------------------------------------------------------------+

Default behavior
~~~~~~~~~~~~~~~~
By default, Pylint will enforce PEP8_-suggested names.

Predefined Naming Styles
~~~~~~~~~~~~~~~~~~~~~~~~
Pylint provides set of predefined naming styles. Those predefined
naming styles may be used to adjust Pylint configuration to coding
style used in linted project.

Following predefined naming styles are available:

* ``snake_case``
* ``camelCase``
* ``PascalCase``
* ``UPPER_CASE``
* ``any`` - fake style which does not enforce any limitations

Following options are exposed:

.. option:: --module-naming-style=<style>

.. option:: --const-naming-style=<style>

.. option:: --class-naming-style=<style>

.. option:: --function-naming-style=<style>

.. option:: --method-naming-style=<style>

.. option:: --attr-naming-style=<style>

.. option:: --argument-naming-style=<style>

.. option:: --variable-naming-style=<style>

.. option:: --class-attribute-naming-style=<style>

.. option:: --class-const-naming-style=<style>

.. option:: --inlinevar-naming-style=<style>

Predefined Naming Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Pylint provides predefined naming patterns for some names. These patterns are often
based on a Naming Style but there is no option to choose one of the styles mentioned above.
The pattern can be overwritten with the options discussed below.

The following type of names are checked with a predefined pattern:

+--------------------+-------------------------------------------------------+------------------------------------------------------------+
| Name type          | Good names                                            | Bad names                                                  |
+====================+=======================================================+============================================================+
| ``typevar``        | ``T``, ``_CallableT``, ``_T_co``, ``AnyStr``,         | ``DICT_T``, ``CALLABLE_T``, ``ENUM_T``, ``DeviceType``,    |
|                    | ``DeviceTypeT``, ``IPAddressT``                       | ``_StrType``                                               |
+--------------------+-------------------------------------------------------+------------------------------------------------------------+
| ``typealias``      | ``GoodName``, ``_GoodName``, ``IPAddressType``,       | ``BadNameT``, ``badName``, ``TBadName``, ``TypeBadName``,  |
|                    |  ``GoodName2`` and other PascalCase variants that     |  ``_1BadName``                                             |
|                    |  don't start with ``T`` or ``Type``. This is to       |                                                            |
|                    |  distinguish them from ``typevars``. Note that        |                                                            |
|                    |  ``TopName`` is allowed but ``TTopName`` isn't.       |                                                            |
+--------------------+-------------------------------------------------------+------------------------------------------------------------+

Custom regular expressions
~~~~~~~~~~~~~~~~~~~~~~~~~~

If predefined naming styles are too limited, checker behavior may be further
customized. For each name type, a separate regular expression matching valid
names of this type can be defined. If any of custom regular expressions are
defined, it overrides ``*-naming-style`` option value.

Regular expressions for the names are anchored at the beginning, any anchor for
the end must be supplied explicitly. Any name not matching the regular
expression will lead to an instance of ``invalid-name``.


.. option:: --module-rgx=<regex>

.. option:: --const-rgx=<regex>

.. option:: --class-rgx=<regex>

.. option:: --function-rgx=<regex>

.. option:: --method-rgx=<regex>

.. option:: --attr-rgx=<regex>

.. option:: --argument-rgx=<regex>

.. option:: --variable-rgx=<regex>

.. option:: --class-attribute-rgx=<regex>

.. option:: --class-const-rgx=<regex>

.. option:: --inlinevar-rgx=<regex>

.. option:: --typevar-rgx=<regex>

.. option:: --typealias-rgx=<regex>

Multiple naming styles for custom regular expressions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Large code bases that have been worked on for multiple years often exhibit an
evolution in style as well. In some cases, modules can be in the same package,
but still have different naming style based on the stratum they belong to.
However, intra-module consistency should still be required, to make changes
inside a single file easier. For this case, Pylint supports regular expression
with several named capturing group.

Rather than emitting name warnings immediately, Pylint will determine the
prevalent naming style inside each module and enforce it on all names.

Consider the following (simplified) example::

   pylint --function-rgx='(?:(?P<snake>[a-z_]+)|(?P<camel>[a-z]+([A-Z][a-z]*)*))$' sample.py

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
~~~~~~~~~~

.. option:: --include-naming-hint=y|n

   Default: off

   Include a hint (regular expression used) for the correct name format with every ``invalid-name`` warning.

.. _PEP8: https://peps.python.org/pep-0008
