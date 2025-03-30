The :ref:`allowed-redefined-builtins <variables-options>` option lets you specify names that are permitted to shadow built-ins.

However, this option is not effective for redefinitions at the module level or for global variables. For example:

Module-Level Redefinitions::

    # module_level_redefine.py
    id = 1  # Shadows the built-in `id`

Global Variable Redefinitions::

    # global_variable_redefine.py
    def my_func():
        global len
        len = 1  # Shadows the built-in `len`

Rationale:

Shadowing built-ins at the global scope is discouraged because it obscures their behavior
throughout the entire module, increasing the risk of subtle bugs when the built-in is needed elsewhere.
In contrast, local redefinitions are acceptable as their impact is confined to a specific scope,
reducing unintended side effects and simplifying debugging.
