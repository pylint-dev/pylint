.. -*- coding: utf-8 -*-

.. _faq:

==========================
Frequently Asked Questions
==========================

1. About Pylint
===============

1.1 What is Pylint?
--------------------

Pylint is a `static code checker`_, meaning it can analyse your code without
actually running it. Pylint checks for errors, tries to enforce a coding
standard, and tries to enforce a coding style.

.. _`static code checker`: http://en.wikipedia.org/wiki/Static_code_analysis


2. Installation
===============

2.1 How do I install Pylint?
----------------------------

Everything should be explained on :ref:`installation`.

2.2 What kind of versioning system does Pylint use?
---------------------------------------------------

Pylint uses the git distributed version control system. The URL of the
repository is: https://github.com/PyCQA/pylint . To get the latest version of
Pylint from the repository, simply invoke ::

    git clone https://github.com/PyCQA/pylint

.. _git: http://git-scm.com/

2.3 What are Pylint's dependencies?
-----------------------------------

Pylint depends on astroid_ and a couple of other packages.
See the following section for details on what versions of Python are
supported.

.. _`astroid`: https://github.com/PyCQA/astroid

2.4 What versions of Python is Pylint supporting?
--------------------------------------------------

Since Pylint 2.0, the supported running environment is Python 3.4+.

That is, Pylint 2.0 is still able to analyze Python 2 files, but some
specific checks might not work, as they would assume that their running
environment was Python 2.

If you need to run pylint with Python 2, then Pylint 1.8 or 1.9 is for you.
We will still do backports of bug fixes, and possibly for various Python 3
compatibility checks, at least until 2020, after which we'll stop support
Python 2 altogether.


3. Running Pylint
=================

3.1 Can I give pylint a file as an argument instead of a module?
-----------------------------------------------------------------

Pylint expects the name of a package or module as its argument. As a
convenience,
you can give it a file name if it's possible to guess a module name from
the file's path using the python path. Some examples :

"pylint mymodule.py" should always work since the current working
directory is automatically added on top of the python path

"pylint directory/mymodule.py" will work if "directory" is a python
package (i.e. has an __init__.py file), an implicit namespace package
or if "directory" is in the python path.

"pylint /whatever/directory/mymodule.py" will work if either:

	- "/whatever/directory" is in the python path

	- your cwd is "/whatever/directory"

	- "directory" is a python package and "/whatever" is in the python
          path

        - "directory" is an implicit namespace package and is in the python path.

	- "directory" is a python package and your cwd is "/whatever" and so
          on...

3.2 Where is the persistent data stored to compare between successive runs?
----------------------------------------------------------------------------

Analysis data are stored as a pickle file in a directory which is
localized using the following rules:

* value of the PYLINTHOME environment variable if set

* ".pylint.d" subdirectory of the user's home directory if it is found
	(not always findable on Windows platforms)

* ".pylint.d" directory in the current directory

3.3 How do I find the option name (for pylintrc) corresponding to a specific command line option?
--------------------------------------------------------------------------------------------------------

You can always generate a sample pylintrc file with --generate-rcfile
Every option present on the command line before this will be included in
the rc file

For example::

	pylint --disable=bare-except,invalid-name --class-rgx='[A-Z][a-z]+' --generate-rcfile

3.4 I'd rather not run Pylint from the command line. Can I integrate it with my editor?
---------------------------------------------------------------------------------------

Much probably. Read :ref:`ide-integration`


4. Message Control
==================

4.1 Is it possible to locally disable a particular message?
-----------------------------------------------------------

Yes, this feature has been added in Pylint 0.11. This may be done by
adding "#pylint: disable=some-message,another-one" at the desired block level
or at the end of the desired line of code

4.2 Is there a way to disable a message for a particular module only?
---------------------------------------------------------------------

Yes, you can disable or enable (globally disabled) messages at the
module level by adding the corresponding option in a comment at the
top of the file: ::

	# pylint: disable=wildcard-import, method-hidden
	# pylint: enable=too-many-lines

4.3 How can I tell Pylint to never check a given module?
--------------------------------------------------------

With Pylint < 0.25, add "#pylint: disable-all" at the beginning of the
module. Pylint 0.26.1 and up have renamed that directive to
"#pylint: skip-file" (but the first version will be kept for backward
compatibility).

In order to ease finding which modules are ignored an Information-level message
`file-ignored` is emitted. With recent versions of Pylint, if you use the old
syntax, an additional `deprecated-disable-all` message is emitted.

4.4 Do I have to remember all these numbers?
--------------------------------------------

No, starting from 0.25.3, you can use symbolic names for messages::

    # pylint: disable=fixme, line-too-long


4.5 I have a callback function where I have no control over received arguments. How do I avoid getting unused argument warnings?
----------------------------------------------------------------------------------------------------------------------------------

Prefix (ui) the callback's name by `cb_`, as in cb_onclick(...). By
doing so arguments usage won't be checked. Another solution is to
use one of the names defined in the "dummy-variables" configuration
variable for unused argument ("_" and "dummy" by default).

4.6 What is the format of the configuration file?
---------------------------------------------------

Pylint uses ConfigParser from the standard library to parse the configuration
file.  It means that if you need to disable a lot of messages, you can use
tricks like: ::

    # disable wildcard-import, method-hidden and too-many-lines because I do
    # not want it
    disable= wildcard-import,
     method-hidden,
     too-many-lines


4.7 Why are there a bunch of messages disabled by default?
----------------------------------------------------------

pylint does have some messages disabled by default, either because
they are prone to false positives or that they are opinionated enough
for not being included as default messages. But most of the disabled
messages are from the Python 3 porting checker, which is disabled by
default. It needs special activation with the ``--py3k`` flag.

5. Classes and Inheritance
==========================


5.1 When is Pylint considering a class as an abstract class?
-------------------------------------------------------------

A class is considered as an abstract class if at least one of its
methods is doing nothing but raising NotImplementedError.

5.2 How do I avoid "access to undefined member" messages in my mixin classes?
-------------------------------------------------------------------------------

To do so you have to set the ignore-mixin-members option to
"yes" (this is the default value) and to name your mixin class with
a name which ends with "mixin" (whatever case).


6. Troubleshooting
==================

6.1 Pylint gave my code a negative rating out of ten. That can't be right!
--------------------------------------------------------------------------

Even though the final rating Pylint renders is nominally out of ten, there's no
lower bound on it. By default, the formula to calculate score is ::

    10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10)

However, this option can be changed in the Pylint rc file. If having negative
values really bugs you, you can set the formula to be the maximum of 0 and the
above expression.


6.2 I think I found a bug in Pylint. What should I do?
-------------------------------------------------------

Read :ref:`Bug reports, feedback`

6.3 I have a question about Pylint that isn't answered here.
------------------------------------------------------------

Read :ref:`Mailing lists`
