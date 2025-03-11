======================
 OSS-Fuzz integration
======================

Platform overview
-----------------

`OSS-Fuzz <https://google.github.io/oss-fuzz/>`_ is Google's free fuzzing platform for open source
software. It runs astroid's fuzz targets to help detect reliability issues that could affect astroid
and Pylint.

Google provides public `build logs <https://oss-fuzz-build-logs.storage.googleapis.com/index.html#astroid>`_
and `fuzzing stats <https://introspector.oss-fuzz.com/project-profile?project=astroid>`_, but most
of the details about bug reports and fuzzed testcases require approved access.

Gaining access
^^^^^^^^^^^^^^

The configuration files for the OSS-Fuzz integration can be found in the
`OSS-Fuzz repository <https://github.com/google/oss-fuzz/tree/master/projects/astroid>`_.
The ``project.yaml`` file controls who has access to bug reports and testcases. Ping the
maintainers if you'd like to be added to the list (note: a Google account is required for
access).

Fuzzing progress
----------------

Once you have access to OSS-Fuzz, you can log in to https://oss-fuzz.com/ with your Google account
to see a dashboard of astroid's fuzzing progress.

Testcases
^^^^^^^^^

The dashboard contains a link to a `testcases page <https://oss-fuzz.com/testcases?project=astroid&open=yes>`_
that lists all testcases that currently trigger a bug in astroid.

Every testcase has a dedicated page with links to view and download a minimized testcase for
reproducing the failure. Each testcase page also contains a stacktrace for the failure and stats
about how often the failure is encountered while fuzzing.

Reproducing a failure
"""""""""""""""""""""

You can download a minimized testcase and run it locally to debug a failure on your machine.
For example, to reproduce a failure with the ``fuzz_parse`` fuzz target, you can run the following
commands:

.. code:: bash

  mkdir fuzzing-repro
  cd fuzzing-repro

  # Note: Atheris doesn't support Python 3.12+ yet:
  # https://github.com/google/atheris/issues/82
  uv venv --python 3.11
  source .venv/bin/activate

  git clone https://github.com/pylint-dev/astroid.git
  cd astroid

  uv pip install atheris==2.3.0
  uv pip install --editable .

  # Save the minimized testcase as `minimized.py` in the astroid directory

  cat << EOF > ./run_fuzz_parse.py

  import astroid
  import atheris

  with open('minimized.py', 'rb') as f:
      fdp = atheris.FuzzedDataProvider(f.read())

  code = fdp.ConsumeUnicodeNoSurrogates(fdp.ConsumeIntInRange(0, 4096))
  astroid.builder.parse(code)
  EOF

  python ./run_fuzz_parse.py


If the failure does not reproduce locally, you can try reproducing the issue in an OSS-Fuzz
container:

.. code:: bash

  git clone https://github.com/google/oss-fuzz.git
  cd oss-fuzz

  python infra/helper.py build_image astroid
  python infra/helper.py build_fuzzers astroid
  python infra/helper.py reproduce astroid fuzz_parse minimized.py

Some failures may only be reproducible in an OSS-Fuzz container because of differences in Python
versions between the OSS-Fuzz platform and your local environment.

Code coverage
^^^^^^^^^^^^^

The dashboard also links to code coverage data for individual fuzz targets and combined code
coverage data for all targets (click on the "TOTAL COVERAGE" link for the combined data).

The combined coverage data is helpful for identifying coverage gaps, insufficient corpus data, and
potential candidates for future fuzz targets.

Bug reports
^^^^^^^^^^^

Bug reports for new failures are automatically filed in the OSS-Fuzz bug tracker with an
`astroid label <https://issues.oss-fuzz.com/issues?q=project:astroid%20status:open>`_.
Make sure you are logged in to view all existing issues.

Build maintenance
-----------------

Google runs compiled fuzz targets on Google Compute Engine VMs. This architecture requires each
project to provide a ``Dockerfile`` and ``build.sh`` script to download code, configure
dependencies, compile fuzz targets, and package any corpus files.

astroid's build files and fuzz-target code can be found in the
`OSS-Fuzz repo <https://github.com/google/oss-fuzz/blob/master/projects/astroid/>`_.

If dependencies change or if new fuzz targets are added, then you may need to modify the build files
and build a new Docker image for OSS-Fuzz.

Building an image
^^^^^^^^^^^^^^^^^

Run the following commands to build astroid's OSS-Fuzz image and fuzz targets:

.. code:: bash

  git clone https://github.com/google/oss-fuzz.git
  cd oss-fuzz

  python infra/helper.py build_image astroid
  python infra/helper.py build_fuzzers astroid

Any changes you make to the build files must be submitted as pull requests to the OSS-Fuzz repo.

Debugging build failures
""""""""""""""""""""""""

You can debug build failures during the ``build_fuzzers`` stage by creating a container and manually
running the ``compile`` command:

.. code:: bash

  # Create a container for building fuzz targets
  python infra/helper.py shell astroid

  # Run this command inside the container to build the fuzz targets
  compile

The ``build.sh`` script will be located at ``/src/build.sh`` inside the container.

Quick links
-----------

- `OSS-Fuzz dashboard <https://oss-fuzz.com/>`_
- `OSS-Fuzz configuration files, build scripts, and fuzz targets for astroid <https://github.com/google/oss-fuzz/tree/master/projects/astroid>`_
- `All open OSS-Fuzz bugs for astroid <https://issues.oss-fuzz.com/issues?q=project:astroid%20status:open>`_
- `Google's OSS-Fuzz documentation <https://google.github.io/oss-fuzz/>`_
