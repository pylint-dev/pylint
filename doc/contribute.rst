.. -*- coding: utf-8 -*-

============
 Contribute
============

Bug reports, feedback
---------------------

You think you have found a bug in Pylint? Well, this may be the case
since Pylint is under development.

Please take the time to check if it is already in the issue tracker at
https://github.com/pycqa/pylint

If you cannot find it in the tracker, create a new issue there or discuss your
problem on the code-quality@python.org mailing list.

The code-quality mailing list is also a nice place to provide feedback about
Pylint, since it is shared with other tools that aim at improving the quality of
python code.

Note that if you don't find something you have expected in Pylint's
issue tracker, it may be because it is an issue with one of its dependencies, namely
astroid:

* https://github.com/pycqa/astroid

Mailing lists
-------------

Use the code-quality@python.org mailing list for anything related
to Pylint. This is in most cases better than sending an email directly
to the author, since others will benefit from the exchange, and you'll
be more likely answered by someone subscribed to the list.

You can subscribe to this mailing list at
http://mail.python.org/mailman/listinfo/code-quality

Archives are available at
http://mail.python.org/pipermail/code-quality/

Archives before April 2013 are available at
http://lists.logilab.org/pipermail/python-projects/

Forge
-----

Pylint is developed using the git_ and mercurial_ distributed version control
systems.

You can clone Pylint and its dependencies from ::

  git clone https://github.com/pycqa/pylint
  git clone https://github.com/pycqa/astroid

.. _mercurial: http://www.selenic.com/mercurial/
.. _git: https://git-scm.com/

Got a change for Pylint?  Below are a few steps you should take to make sure
your patch gets accepted.

- Test your code

    - Pylint keeps a set of unit tests in the /test directory. The
      `test_func.py` module uses external files to have some kind of easy
      functional testing. To get your patch accepted you must write (or change)
      a test input file in the `test/input` directory and message file in the
      `test/messages` directory. Then run `python test_func.py` to ensure that
      your test is green.

    - You should also run all the tests to ensure that your change isn't
      breaking one.

- Add a short entry to the ChangeLog describing the change, except for internal
  implementation only changes

- Write a comprehensive commit message

- Relate your change to an issue in the tracker if such an issue exists (see
  `this page`_ of the GitHub documentation for more information on this)

- Send a pull request from GitHub (more on this here_)

.. _`this page`: https://help.github.com/articles/closing-issues-via-commit-messages/
.. _here: https://help.github.com/articles/using-pull-requests/


Unit test setup
---------------

To run the pylint unit tests within your checkout (without having to install
anything), you need to set PYTHONPATH so that pylint and astroid are available.
Assume you have those packages in ~/src.  If
you have a normal clone of logilab-common, it will not be properly
structured to allow import of logilab.common.  To remedy this, create the
necessary structure::

  cd ~/src
  mkdir logilab
  mv logilab-common logilab/common
  touch logilab/__init__.py

Now, set PYTHONPATH to your src directory::

  export PYTHONPATH=~/src

You now have access to the astroid, logilab.common and pylint packages
without installing them.  You can run all the unit tests like so::

  cd ~/src/pylint/test
  for f in *.py ; do
    echo $f
    python -S $f
  done

The -S flag keeps distutils from interfering with sys.path.  YMMV.


Adding new functional tests
----------------------------

Pylint comes with an easy way to write functional tests for new checks:

* put a Python file in the `test/input` directory, whose name starts with
  `func_` and should also contains the symbolic name of the tested check

* add the expected message file in the `test/messages` directory, using the
  same name but a `.txt` extension instead of `.py`

The message file should use the default text output format (without reports) and lines should be
sorted. E.g on Unix system, you may generate it using::

  pylint -rn input/func_mycheck.py | sort > pylint messages/func_mycheck.txt

Also, here are a few naming convention which are used:

* Python files starting with 'func_noerror' don't have any message file
  associated as they are expected to provide no output at all

* You may provide different input files (and associated output) depending on the
  Python interpreter version:

  * tests whose name ends with `_py<xy>.py` are used for Python >= x.y
  * tests whose name ends with `_py<_xy>.py` are used for Python < x.y

* Similarly you may provide different message files for a single input, message
  file whose name ends with '_py<xy>.txt' will be used for Python >= x.y, using
  the nearest version possible
