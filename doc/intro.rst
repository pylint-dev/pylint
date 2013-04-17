.. -*- coding: utf-8 -*-

==============
 Introduction
==============

What is Pylint?
---------------

Pylint is a tool that checks for errors in Python code, tries to enforce a
coding standard and looks for bad code smells. This is similar but nevertheless
different from what pychecker_ provides, especially since pychecker explicitly
does not bother with coding style. The default coding style used by Pylint is
close to `PEP 008`_ (aka `Guido's style guide`_). For more information about
code smells, refer to Martin Fowler's `refactoring book`_

Pylint will display a number of messages as it analyzes the code, as well as
some statistics about the number of warnings and errors found in different
files. The messages are classified under various categories such as errors and
warnings (more below). If you run Pylint twice, it will display the statistics
from the previous run together with the ones from the current run, so that you
can see if the code has improved or not.

Last but not least, the code is given an overall mark, based on the number an
severity of the warnings and errors. This has proven to be very motivating for
some programmers.

Pylint was born in 2003 at Logilab_, that funded Sylvain Thénault to lead its
development up to now.

.. _pychecker: http://pychecker.sf.net
.. _`PEP 008`: http://www.python.org/dev/peps/pep-0008/
.. _`Guido's style guide`: http://www.python.org/doc/essays/styleguide.html
.. _`refactoring book`: http://www.refactoring.com/
.. _Logilab: http://www.logilab.fr

What Pylint is not?
-------------------

What Pylint says is not to be taken as gospel and Pylint isn't smarter than you
are: it may warn you about things that you have conscientiously done.

Pylint tries hard to report as few false positives as possible for errors, but
it may be too verbose with warnings. That's for example because it tries to
detect things that may be dangerous in a context, but are not in others, or
because it checks for some things that you don't care about. Generally, you
shouldn't expect Pylint to be totally quiet about your code, so don't
necessarily be alarmed if it gives you a hell lot of messages for your project!

:Quoting Alexandre Fayolle:
  My usage pattern for Pylint is to generally run ``pylint -E`` quite often to
  get stupid errors flagged before launching an application (or before
  committing). I generally run Pylint with all the bells and whistles
  activated some time before a release, when I want to cleanup the code.
  And when I do that I simply ignore tons of the false warnings (and I
  can do that without being driven mad by this dumb program which is not
  smart enough to understand the dynamicity of Python because I only run
  it once or twice a week in this mode)

:Quoting Marteen Ter Huurne:
  In our project we just accepted that we have to make some modifications in our
  code to please Pylint:

  - stick to more naming conventions (unused variables ending in underscores,
    mix-in class names ending in "Mixin")

  - making all abstract methods explicit (rather than just not defining them in
    the superclass)

  - add ``# pylint: disable=X0123`` comments:

    - for messages which are useful in general, but not in a specific case

    - for Pylint bugs

    - for Pylint limitations (for instance Twisted's modules create a lot of
      definitions dynamically so Pylint does not know about them)

  The effort is worth it, since Pylint helps us a lot in keeping the code clean
  and finding errors early. Although most errors found by Pylint would also be
  found by the regression tests, by fixing them before committing, we save time.
  And our regression tests do not cover all code either, just the most complex
  parts.

