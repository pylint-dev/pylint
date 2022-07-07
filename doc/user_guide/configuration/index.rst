.. _all-configurations-options:

=============
Configuration
=============

Pylint is highly configurable. There are a lot of options to follow the needs of
various projects and a lot of checks to activate if they suit your style.

You can generate a sample configuration file with ``--generate-toml-config``
or ``--generate-rcfile``. Every option present on the command line before this
will be included in the file

For example::

    pylint --disable=bare-except,invalid-name --class-rgx='[A-Z][a-z]+' --generate-toml-config

.. toctree::
   :maxdepth: 2
   :titlesonly:

   all-options
