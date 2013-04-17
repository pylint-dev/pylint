.. -*- coding: utf-8 -*-

============
 Contribute
============

Bug reports, feedback
---------------------

You think you have found a bug in Pylint? Well, this may be the case
since Pylint is under development. Please take the time to send a bug
report to python-projects@logilab.org if you've not found it already reported on
the `tracker page`_. This mailing list is also a nice place to
discuss Pylint issues, see below for more information about Pylint's related
lists.

You can check for already reported bugs, planned features on Pylint's tracker
web page: https://bitbucket.org/logilab/pylint/issues

Notice that if you don't find something you have expected in Pylint's
tracker page, it may be on the tracker page of one of its dependencies, namely
astng and common:

* https://bitbucket.org/logilab/astng/issues
* http://www.logilab.org/project/logilab-common

.. _`tracker page`: https://bitbucket.org/logilab/pylint/issues

Mailing lists
-------------

Use the python-projects@logilab.org mailing list for anything related
to Pylint. This is in most cases better than sending an email directly
to the author, since others will benefit from the exchange, and you'll
be more likely answered by someone subscribed to the list. This is a
moderated mailing list, so if you're not subscribed email you send will have to
be validated first before actually being sent on the list.

You can subscribe to this mailing list at
http://lists.logilab.org/mailman/listinfo/python-projects

Archives are available at
http://lists.logilab.org/pipermail/python-projects/

If you prefer speaking French instead of English, you can use the
generic forum-fr@logilab.org mailing list:

* (un)subscribe: http://lists.logilab.org/mailman/listinfo/forum-fr
* archives: http://lists.logilab.org/pipermail/forum-fr

Notice though that this list has a very low traffic since most Pylint related
discussions are done on the python-projects mailing list.

Development
-----------

Pylint is developped using the mercurial_ version control system. This is a very
cool distributed VCS and its usage is very similar to other ones such as cvs or
subversion (though the distributed feature introduced some different usage
patterns). See mercurial_ home page for installation on your computer and basic
usage. Note that it's very easy to send us patches using `hg email` command ;).

You can get the in-development Pylint source code from its bitbucket repository: ::

  hg clone https://bitbucket.org/logilab/pylint

The same is true for Pylint dependencies (if you use Pylint code from the
repository, you should usually use code from the repository as well for astng
and logilab-common): ::

  hg clone https://bitbucket.org/logilab/astng
  hg clone http://hg.logilab.org/logilab/common

.. _mercurial: http://www.selenic.com/mercurial/

Got a patch for Pylint?  There a few steps you must take to make sure your
patch gets accepted.

* Test your code

    * Pylint keeps a set of unit tests in the /test directory. To get your
      patch accepted you must write (or change) a test input file and message
      file in the appropriate input and messages folders.

    * In the test folder of pylint run ./fulltest.sh (python version), make sure
      all tests pass before submitting a patch

* Add an entry to the ChangeLog describing the change

* Take care of the commit message

* Relate your change to a tracker issue

If you don't want to bother with mercurial, you can still create a diff and
post it to the mailing list or as attachment to a tracker issue.
