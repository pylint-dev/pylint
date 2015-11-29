.. -*- coding: utf-8 -*-

============
 Contribute
============

Bug reports, feedback
---------------------

You think you have found a bug in Pylint? Well, this may be the case
since Pylint is under development.

Please take the time to check if it is already in the issue tracker at
https://bitbucket.org/logilab/pylint

If you can not find it in the tracker, create a new issue there or discuss your
problem on the code-quality@python.org mailing list.

The code-quality mailing list is also a nice place to provide feedback about
Pylint, since it is shared with other tools that aim at improving the quality of
python code.

Note that if you don't find something you have expected in Pylint's
issue tracker, it may be because it is an issue with one of its dependencies, namely
astroid.

* https://bitbucket.org/logilab/astroid

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

Pylint is developed using the mercurial_ distributed version control system.

You can clone Pylint and its dependencies from ::

  hg clone https://bitbucket.org/logilab/pylint
  hg clone https://bitbucket.org/logilab/astroid
  hg clone http://hg.logilab.org/logilab/common

.. _mercurial: http://www.selenic.com/mercurial/

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
  `this page`_ of Bitbucket documentation for more information on this)

- Send a pull request from Bitbucket (more on this here_)

.. _`this page`: https://confluence.atlassian.com/display/BITBUCKET/Resolve+issues+automatically+when+users+push+code
.. _here: https://confluence.atlassian.com/display/BITBUCKET/Work+with+pull+requests


Unit test setup
---------------

If you have tox installed, running ``tox`` command should be
enough to get you started. Otherwise, you can follow this recipe
for running the tests for pylint::

   python setup.py develop # or ``pip install -e .``
   cd pylint/test
   python -m unittest discover -p "*test*"


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
