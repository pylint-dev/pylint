.. _all-configurations-options:

=============
Configuration
=============

Pylint is highly configurable. There are a lot of options to follow the needs of
various projects and a lot of checks to activate if they suit your style.

You can generate a sample configuration file with ``--generate-toml-config``
or ``--generate-rcfile``. Every option present on the command line before this
will be included in the file.

For example::

    pylint --disable=bare-except,invalid-name --class-rgx='[A-Z][a-z]+' --generate-toml-config

In practice, it is often better to create a minimal configuration file which only contains
configuration overrides. For all other options, Pylint will use its default values.

.. tip::

    TOML basic strings use backslashes as escape characters, so each literal
    backslash must be doubled. Pylint's generated TOML configuration does this
    automatically. When writing regular expression options by hand, single-quoted
    `literal strings <https://toml.io/en/v1.0.0#string>`_ avoid the extra escaping.

    The ``ignore-paths`` option reserves backslashes as Windows path separators,
    so they cannot escape regular expression metacharacters. Use a character class
    instead. For example:

    .. code-block:: toml

       [tool.pylint.main]
       ignore-paths = ['^.*[.]pyi$']

.. note::

    The internals that create the configuration files fall back to the default values if
    no other value was given. This means that some values depend on the interpreter that
    was used to generate the file. Most notably ``py-version`` which defaults to the
    current interpreter.

.. toctree::
   :maxdepth: 2
   :titlesonly:

   all-options
