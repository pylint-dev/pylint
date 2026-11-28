Classes often subclass a framework base just to supply configuration or private
hooks. To keep this check enabled for the rest of your code, use
:ref:`--exclude-too-few-public-methods <exclude-too-few-public-methods-option>`
to exempt classes with a matching ancestor.

For example, if ``app.forms.SignupForm`` inherits from ``framework.forms.BaseForm``,
add the following to ``pyproject.toml``:

.. code-block:: toml

   [tool.pylint.design]
   exclude-too-few-public-methods = ['^framework\.forms\.BaseForm$']

The pattern matches the fully qualified name of the base class, not the name
of the subclass. It exempts both direct and indirect subclasses from this
check. It does not exempt the named base class itself merely because its name
matches the pattern, and it does not change the minimum for unrelated classes.
