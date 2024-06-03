.. _pre-commit-integration:

Pre-commit integration
======================

``pylint`` can be used as a `pre-commit <https://pre-commit.com>`_ hook. We however
discourage it as pylint -- due to its speed -- is more suited to a continuous integration
job or a git ``pre-push`` hook, especially if your repository is large.

Since ``pylint`` needs to import modules and dependencies to work correctly, the
hook only works with a local installation of ``pylint`` (in your environment). It means
it can't be used with ``pre-commit.ci``, and you will need to add the following to your
``.pre-commit-config.yaml`` ::

.. sourcecode:: yaml

    ci:
      skip: [pylint]

Another limitation is that pylint should analyse all your code at once in order to best infer the
actual values that result from calls. If only some of the files are given, pylint might
miss a particular value's type and produce inferior inference for the subset. Since pre-commit slices
the files given to it in order to parallelize the processing, the result can be degraded.
It can also be unexpectedly different when the file set changes because the new slicing can change
the inference. Thus the ``require_serial`` option should be set to ``true`` if correctness and determinism
are more important than parallelization to you.

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
        require_serial: true
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
