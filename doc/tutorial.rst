
========
Tutorial
========

:Author: Robert Kirkpatrick


Intro
-----

Beginner to coding standards?  Pylint can be your guide to reveal what's really
going on behind the scenes and help you to become a more aware programmer.

Sharing code is a rewarding endeavor.  Putting your code ``out there`` can be
either an act of philanthropy, ``coming of age``, or a basic extension of belief
in open source.  Whatever the motivation, your good intentions may not have the
desired outcome if people find your code hard to use or understand.  The Python
community has formalized some recommended programming styles to help everyone
write code in a common, agreed-upon style that makes the most sense for shared
code.  This style is captured in PEP-8_.  Pylint can be a quick and easy way of
seeing if your code has captured the essence of PEP-8 and is therefore
``friendly`` to other potential users.

Perhaps you're not ready to share your code but you'd like to learn a bit more
about writing better code and don't know where to start.  Pylint can tell you
where you may have run astray and point you in the direction to figure out what
you have done and how to do better.

This tutorial is all about approaching coding standards with little or no
knowledge of in-depth programming or the code standards themselves.  It's the
equivalent of skipping the manual and jumping right in.

My command line prompt for these examples is:

.. sourcecode:: bash

  robertk01 Desktop$

.. _PEP-8: http://www.python.org/dev/peps/pep-0008/

Getting Started
---------------

Running Pylint with no arguments will invoke the help dialogue and give you an
idea of the arguments available to you.  Do that now, i.e.:

.. sourcecode:: bash

  robertk01 Desktop$ pylint
  ...
  a bunch of stuff
  ...


A couple of the options that we'll focus on here are: ::

  Master:
    --generate-rcfile=<file>
  Commands:
    --help-msg=<msg-id>
  Commands:
    --help-msg=<msg-id>
  Message control:
    --disable=<msg-ids>
  Reports:
    --files-output=<y_or_n>
    --reports=<y_or_n>
    --output-format=<format>

Also pay attention to the last bit of help output.  This gives you a hint of what
Pylint is going to ``pick on``: ::

  Output:
     Using the default text output, the message format is :
    MESSAGE_TYPE: LINE_NUM:[OBJECT:] MESSAGE
    There are 5 kind of message types :
    * (C) convention, for programming standard violation
    * (R) refactor, for bad code smell
    * (W) warning, for python specific problems
    * (E) error, for much probably bugs in the code
    * (F) fatal, if an error occurred which prevented pylint from doing
    further processing.

When Pylint is first run on a fresh piece of code, a common complaint is that it
is too ``noisy``.  The current default configuration is set to enforce all possible
warnings.  We'll use some of the options I noted above to make it suit your
preferences a bit better (and thus make it emit messages only when needed).


Your First Pylint'ing
---------------------

We'll use a basic python script as fodder for our tutorial.  I borrowed
extensively from the code here: http://www.daniweb.com/code/snippet748.html
The starting code we will use is called simplecaeser.py and is here in its
entirety:

.. sourcecode:: python

   1  #!/usr/bin/env python
   2
   3  import string
   4
   5  shift = 3
   6  choice = raw_input("would you like to encode or decode?")
   7  word = (raw_input("Please enter text"))
   8  letters = string.ascii_letters + string.punctuation + string.digits
   9  encoded = ''
  10  if choice == "encode":
  11      for letter in word:
  12          if letter == ' ':
  13              encoded = encoded + ' '
  14          else:
  15              x = letters.index(letter) + shift
  16              encoded=encoded + letters[x]
  17  if choice == "decode":
  18      for letter in word:
  19          if letter == ' ':
  20              encoded = encoded + ' '
  21          else:
  22              x = letters.index(letter) - shift
  23              encoded = encoded + letters[x]
  24
  25  print encoded


Let's get started.

If we run this:

.. sourcecode:: bash

  robertk01 Desktop$ pylint simplecaeser.py
  No config file found, using default configuration
  ************* Module simplecaeser
  C:  1, 0: Missing module docstring (missing-docstring)
  W:  3, 0: Uses of a deprecated module 'string' (deprecated-module)
  C:  5, 0: Invalid constant name "shift" (invalid-name)
  C:  6, 0: Invalid constant name "choice" (invalid-name)
  C:  7, 0: Invalid constant name "word" (invalid-name)
  C:  8, 0: Invalid constant name "letters" (invalid-name)
  C:  9, 0: Invalid constant name "encoded" (invalid-name)
  C: 16,12: Operator not preceded by a space
	      encoded=encoded + letters[x]
		     ^ (no-space-before-operator)


  Report
  ======
  19 statements analysed.

  Duplication
  -----------

  +-------------------------+------+---------+-----------+
  |                         |now   |previous |difference |
  +=========================+======+=========+===========+
  |nb duplicated lines      |0     |0        |=          |
  +-------------------------+------+---------+-----------+
  |percent duplicated lines |0.000 |0.000    |=          |
  +-------------------------+------+---------+-----------+



  Raw metrics
  -----------

  +----------+-------+------+---------+-----------+
  |type      |number |%     |previous |difference |
  +==========+=======+======+=========+===========+
  |code      |21     |87.50 |21       |=          |
  +----------+-------+------+---------+-----------+
  |docstring |0      |0.00  |0        |=          |
  +----------+-------+------+---------+-----------+
  |comment   |1      |4.17  |1        |=          |
  +----------+-------+------+---------+-----------+
  |empty     |2      |8.33  |2        |=          |
  +----------+-------+------+---------+-----------+



  Statistics by type
  ------------------

  +---------+-------+-----------+-----------+------------+---------+
  |type     |number |old number |difference |%documented |%badname |
  +=========+=======+===========+===========+============+=========+
  |module   |1      |1          |=          |0.00        |0.00     |
  +---------+-------+-----------+-----------+------------+---------+
  |class    |0      |0          |=          |0.00        |0.00     |
  +---------+-------+-----------+-----------+------------+---------+
  |method   |0      |0          |=          |0.00        |0.00     |
  +---------+-------+-----------+-----------+------------+---------+
  |function |0      |0          |=          |0.00        |0.00     |
  +---------+-------+-----------+-----------+------------+---------+



  Messages by category
  --------------------

  +-----------+-------+---------+-----------+
  |type       |number |previous |difference |
  +===========+=======+=========+===========+
  |convention |7      |7        |=          |
  +-----------+-------+---------+-----------+
  |refactor   |0      |0        |=          |
  +-----------+-------+---------+-----------+
  |warning    |1      |1        |=          |
  +-----------+-------+---------+-----------+
  |error      |0      |0        |=          |
  +-----------+-------+---------+-----------+



  Messages
  --------

  +-------------------------+------------+
  |message id               |occurrences |
  +=========================+============+
  |invalid-name             |5           |
  +-------------------------+------------+
  |no-space-before-operator |1           |
  +-------------------------+------------+
  |missing-docstring        |1           |
  +-------------------------+------------+
  |deprecated-module        |1           |
  +-------------------------+------------+



  Global evaluation
  -----------------
  Your code has been rated at 5.79/10


Wow.  That's a lot of stuff.  The first part is the 'messages' section while the
second part is the 'report' section.  There are two points I want to tackle here.

First point is that all the tables of statistics (i.e. the report) are a bit
overwhelming so I want to silence them.  To do that, I will use the
**--reports=n** option.

.. tip:: Many of Pylint's commonly used command line options have shortcuts.
 for example, **--reports=n** can be abbreviated to **-rn**. Pylint's man page lists
 all these shortcuts.

Second, previous experience taught me that the default output for the messages
needed a bit more info.  We can see the first line is: ::

  "C:  1: Missing docstring (missing-docstring)"

This basically means that line 1 violates a convention ``C``.  It's telling me I
really should have a docstring.  I agree, but what if I didn't fully understand
what rule I violated.  Knowing only that I violated a convention isn't much help
if I'm a newbie. Another information there is the message symbol between parens,
``missing-docstring`` here.

If I want to read up a bit more about that, I can go back to the
command line and try this:

.. sourcecode:: bash

  robertk01 Desktop$ pylint --help-msg=missing-docstring
  No config file found, using default configuration
  :missing-docstring (C0111): *Missing docstring*
    Used when a module, function, class or method has no docstring. Some special
    methods like __init__ doesn't necessarily require a docstring. This message
    belongs to the basic checker.

Yeah, ok. That one was a bit of a no-brainer but I have run into error messages
that left me with no clue about what went wrong, simply because I was unfamiliar
with the underlying mechanism of code theory.  One error that puzzled my newbie
mind was: ::

  :too-many-instance-attributes (R0902): *Too many instance attributes (%s/%s)*

I get it now thanks to Pylint pointing it out to me.  If you don't get that one,
pour a fresh cup of coffee and look into it - let your programmer mind grow!


The Next Step
-------------

Now that we got some configuration stuff out of the way, let's see what we can
do with the remaining warnings.

If we add a docstring to describe what the code is meant to do that will help.
I'm also going to be a bit cowboy and ignore the ``deprecated-module`` message
because I like to take risks in life.  A deprecation warning means that future
versions of Python may not support that code so my code may break in the future.
There are 5 ``invalid-name`` messages that we will get to later.  Lastly, I violated the
convention of using spaces around an operator such as "=" so I'll fix that too.
To sum up, I'll add a docstring to line 2, put spaces around the = sign on line
16 and use the ``--disable=deprecated-module`` to ignore the deprecation warning.

Here is the updated code:

.. sourcecode:: python

   1  #!/usr/bin/env python
   2  """This script prompts a user to enter a message to encode or decode
   3  using a classic Caeser shift substitution (3 letter shift)"""
   4
   5  import string
   6
   7  shift = 3
   8  choice = raw_input("would you like to encode or decode?")
   9  word = (raw_input("Please enter text"))
  10  letters = string.ascii_letters + string.punctuation + string.digits
  11  encoded = ''
  12  if choice == "encode":
  13      for letter in word:
  14          if letter == ' ':
  15              encoded = encoded + ' '
  16          else:
  17              x = letters.index(letter) + shift
  18              encoded = encoded + letters[x]
  19  if choice == "decode":
  20      for letter in word:
  21          if letter == ' ':
  22              encoded = encoded + ' '
  23          else:
  24              x = letters.index(letter) - shift
  25              encoded = encoded + letters[x]
  26
  27  print encoded

And here is what happens when we run it with our ``--disable=deprecated-module``
option:

.. sourcecode:: bash

  robertk01 Desktop$ pylint --reports=n --disable=deprecated-module simplecaeser.py
  No config file found, using default configuration
  ************* Module simplecaeser
  C:  7, 0: Invalid constant name "shift" (invalid-name)
  C:  8, 0: Invalid constant name "choice" (invalid-name)
  C:  9, 0: Invalid constant name "word" (invalid-name)
  C: 10, 0: Invalid constant name "letters" (invalid-name)
  C: 11, 0: Invalid constant name "encoded" (invalid-name)

Nice!  We're down to just the ``invalid-name`` messages.

There are fairly well defined conventions around naming things like instance
variables, functions, classes, etc.  The conventions focus on the use of
UPPERCASE and lowercase as well as the characters that separate multiple words
in the name.  This lends itself well to checking via a regular expression, thus
the **should match (([A-Z\_][A-Z1-9\_]*)|(__.*__))$**.

In this case Pylint is telling me that those variables appear to be constants
and should be all UPPERCASE. This is an in-house convention that lives with Pylint
since its inception. You too can create your own in-house naming
conventions but for the purpose of this tutorial, we want to stick to the PEP-8
standard. In this case, the variables I declared should follow the convention
of all lowercase.  The appropriate rule would be something like:
"should match [a-z\_][a-z0-9\_]{2,30}$".  Notice the lowercase letters in the
regular expression (a-z versus A-Z).

If we run that rule using a ``--const-rgx='[a-z\_][a-z0-9\_]{2,30}$'`` option, it
will now be quite quiet:

.. sourcecode:: bash

  robertk01 Desktop$ pylint --reports=n --disable=deprecated-module --const-rgx='[a-z_][a-z0-9_]{2,30}$'  simplecaeser.py
  No config file found, using default configuration

Regular expressions can be quite a beast so take my word on this particular
example but go ahead and `read up`_ on them if you want.

.. tip::
 It would really be a pain to have to use all these options
 on the command line all the time.  That's what the configuration file is for.  We can
 configure our Pylint to store our options for us so we don't have to declare
 them on the command line.  Using the configuration file is a nice way of formalizing your
 rules and quickly sharing them with others. Invoking ``pylint
 --generate-rcfile`` will create a sample rcfile with all the options set and
 explained in comments.

That's it for the basic intro. More tutorials will follow.

.. _`read up`: http://docs.python.org/library/re.html
