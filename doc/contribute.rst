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
astng and common:

* https://bitbucket.org/logilab/astng
* http://www.logilab.org/project/logilab-common

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

Pylint is developped using the mercurial_ distributed version control system.

You can clone Pylint and its dependencies from ::

  hg clone https://bitbucket.org/logilab/pylint
  hg clone https://bitbucket.org/logilab/astng
  hg clone http://hg.logilab.org/logilab/common

.. _mercurial: http://www.selenic.com/mercurial/

Got a change for Pylint?  There a few steps you must take to make sure your
patch gets accepted.

- Test your code

    - Pylint keeps a set of unit tests in the /test directory. To get your
      patch accepted you must write (or change) a test input file and message
      file in the appropriate input and messages folders.

    - In the test folder of Pylint run ``./fulltest.sh <python versions>``, make sure
      all tests pass before submitting a patch

- Add an short entry to the ChangeLog describing the change

- Write a comprehensive commit message

- Relate your change to an issue in the tracker

- Send a pull request from bitbucket
