.. _pre-commit-integration:

Pre-commit integration
======================

``pylint`` can be used as a `pre-commit <https://pre-commit.com>`_ hook.

Since ``pylint`` needs to import modules and dependencies to work correctly, the
hook only works with a local installation of ``pylint`` (in your environment).
If you installed ``pylint`` locally it can be added to ``.pre-commit-config.yaml``
as follows:

.. sourcecode:: yaml

  - repo: local
    hooks:
      - id: pylint
        name: pylint
        entry: pylint
        language: system
        types: [python]
        args:
          [
            "-rn", # Only display messages
            "-sn", # Don't display the score
          ]

You can use ``args`` to pass command line arguments as described in the :ref:`tutorial`.
A hook with more arguments could look something like this:

.. sourcecode:: yaml

  - repo: local
    hooks:
      - id: pylint
        name: pylint
        entry: pylint
        language: system
        types: [python]
        args:
          [
            "-rn", # Only display messages
            "-sn", # Don't display the score
            "--rcfile=pylintrc", # Link to your config file
            "--load-plugins=pylint.extensions.docparams", # Load an extension
          ]
