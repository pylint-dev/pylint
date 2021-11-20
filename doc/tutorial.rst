.. _tutorial:

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
code.  This style is captured in `PEP 8`_, the "Style Guide for Python Code".
Pylint can be a quick and easy way of
seeing if your code has captured the essence of `PEP 8`_ and is therefore
``friendly`` to other potential users.

Perhaps you're not ready to share your code but you'd like to learn a bit more
about writing better code and don't know where to start.  Pylint can tell you
where you may have run astray and point you in the direction to figure out what
you have done and how to do better.

This tutorial is all about approaching coding standards with little or no
knowledge of in-depth programming or the code standards themselves.  It's the
equivalent of skipping the manual and jumping right in.

My command line prompt for these examples is:

.. sourcecode:: console

  robertk01 Desktop$

.. _PEP 8: https://www.python.org/dev/peps/pep-0008/

Getting Started
---------------

Running Pylint with no arguments will invoke the help dialogue and give you an
idea of the arguments available to you.  Do that now, i.e.:

.. sourcecode:: console

  robertk01 Desktop$ pylint
  ...
  a bunch of stuff
  ...


A couple of the options that we'll focus on here are: ::

  Commands:
    --help-msg=<msg-id>
    --generate-rcfile
  Messages control:
    --disable=<msg-ids>
  Reports:
    --reports=<y or n>
    --output-format=<format>

If you need more detail, you can also ask for an even longer help message,
like so: ::

  robertk01 Desktop$ pylint --long-help
  ...
  Even more stuff
  ...

Pay attention to the last bit of this longer help output.  This gives you a
hint of what
Pylint is going to ``pick on``: ::

  Output:
     Using the default text output, the message format is :
    MESSAGE_TYPE: LINE_NUM:[OBJECT:] MESSAGE
    There are 5 kind of message types :
    * (C) convention, for programming standard violation
    * (R) refactor, for bad code smell
    * (W) warning, for python specific problems
    * (E) error, for probable bugs in the code
    * (F) fatal, if an error occurred which prevented pylint from doing
    further processing.

When Pylint is first run on a fresh piece of code, a common complaint is that it
is too ``noisy``.  The current default configuration is set to enforce all possible
warnings.  We'll use some of the options I noted above to make it suit your
preferences a bit better (and thus make it emit messages only when needed).


Your First Pylint'ing
---------------------

We'll use a basic Python script as fodder for our tutorial.
The starting code we will use is called simplecaesar.py and is here in its
entirety:

.. sourcecode:: python

   #!/usr/bin/env python3

   import string;

   shift = 3
   choice = input("would you like to encode or decode?")
   word = input("Please enter text")
   letters = string.ascii_letters + string.punctuation + string.digits
   encoded = ''
   if choice == "encode":
       for letter in word:
           if letter == ' ':
               encoded = encoded + ' '
           else:
               x = letters.index(letter) + shift
               encoded = encoded + letters[x]
   if choice == "decode":
       for letter in word:
           if letter == ' ':
               encoded = encoded + ' '
           else:
               x = letters.index(letter) - shift
               encoded = encoded + letters[x]

   print(encoded)


Let's get started.

If we run this:

.. sourcecode:: console

  robertk01 Desktop$ pylint simplecaesar.py
  ************* Module simplecaesar
  simplecaesar.py:3:0: W0301: Unnecessary semicolon (unnecessary-semicolon)
  simplecaesar.py:1:0: C0114: Missing module docstring (missing-module-docstring)
  simplecaesar.py:5:0: C0103: Constant name "shift" doesn't conform to UPPER_CASE naming style (invalid-name)
  simplecaesar.py:9:0: C0103: Constant name "encoded" doesn't conform to UPPER_CASE naming style (invalid-name)
  simplecaesar.py:13:12: C0103: Constant name "encoded" doesn't conform to UPPER_CASE naming style (invalid-name)

  -----------------------------------
  Your code has been rated at 7.37/10


Previous experience taught me that the default output for the messages
needed a bit more info.  We can see the second line is: ::

  "simplecaesar.py:1:0: C0114: Missing module docstring (missing-module-docstring)"

This basically means that line 1 violates a convention ``C0114``.  It's telling me I really should have a docstring.
I agree, but what if I didn't fully understand what rule I violated.  Knowing only that I violated a convention
isn't much help if I'm a newbie. Another piece of information there is the
message symbol between parens, ``missing-module-docstring`` here.

If I want to read up a bit more about that, I can go back to the
command line and try this:

.. sourcecode:: console

  robertk01 Desktop$ pylint --help-msg=missing-module-docstring
  :missing-module-docstring (C0114): *Missing module docstring*
    Used when a module has no docstring.Empty modules do not require a docstring.
    This message belongs to the basic checker.


Yeah, ok. That one was a bit of a no-brainer, but I have run into error messages
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
There are 5 ``invalid-name`` messages that we will get to later.  Lastly, I
put an unnecessary semicolon at the end of the import line so I'll
fix that too. To sum up, I'll add a docstring to line 2, and remove the ``;``
from line 3.

Here is the updated code:

.. sourcecode:: python

   #!/usr/bin/env python3
   """This script prompts a user to enter a message to encode or decode
   using a classic Caesar shift substitution (3 letter shift)"""

   import string

   shift = 3
   choice = input("would you like to encode or decode?")
   word = input("Please enter text")
   letters = string.ascii_letters + string.punctuation + string.digits
   encoded = ''
   if choice == "encode":
       for letter in word:
           if letter == ' ':
               encoded = encoded + ' '
           else:
               x = letters.index(letter) + shift
               encoded = encoded + letters[x]
   if choice == "decode":
       for letter in word:
           if letter == ' ':
               encoded = encoded + ' '
           else:
               x = letters.index(letter) - shift
               encoded = encoded + letters[x]

   print(encoded)

Here is what happens when we run it:

.. sourcecode:: console

  robertk01 Desktop$ pylint simplecaesar.py
  ************* Module simplecaesar
  simplecaesar.py:7:0: C0103: Constant name "shift" doesn't conform to UPPER_CASE naming style (invalid-name)
  simplecaesar.py:11:0: C0103: Constant name "encoded" doesn't conform to UPPER_CASE naming style (invalid-name)
  simplecaesar.py:15:12: C0103: Constant name "encoded" doesn't conform to UPPER_CASE naming style (invalid-name)

  ------------------------------------------------------------------
  Your code has been rated at 8.42/10 (previous run: 7.37/10, +1.05)

Nice! Pylint told us how much our code rating has improved since our last run, and we're down to just the ``invalid-name`` messages.

There are fairly well defined conventions around naming things like instance
variables, functions, classes, etc.  The conventions focus on the use of
UPPERCASE and lowercase as well as the characters that separate multiple words
in the name.  This lends itself well to checking via a regular expression, thus
the **should match (([A-Z\_][A-Z1-9\_]*)|(__.*__))$**.

In this case Pylint is telling me that those variables appear to be constants
and should be all UPPERCASE. This is an in-house convention that has lived with Pylint
since its inception. You too can create your own in-house naming
conventions but for the purpose of this tutorial, we want to stick to the `PEP 8`_
standard. In this case, the variables I declared should follow the convention
of all lowercase.  The appropriate rule would be something like:
"should match [a-z\_][a-z0-9\_]{2,30}$".  Notice the lowercase letters in the
regular expression (a-z versus A-Z).

If we run that rule using a ``--const-rgx='[a-z\_][a-z0-9\_]{2,30}$'`` option, it
will now be quite quiet:

.. sourcecode:: console

  robertk01 Desktop$ pylint --const-rgx='[a-z_][a-z0-9_]{2,30}$' simplecaesar.py

  -------------------------------------------------------------------
  Your code has been rated at 10.00/10 (previous run: 8.42/10, +1.58)


Regular expressions can be quite a beast so take my word on this particular
example but go ahead and `read up`_ on them if you want.

.. tip::
 It would really be a pain to specify that regex on the command line all the time, particularly if we're using many other options.
 That's what a configuration file is for. We can configure our Pylint to
 store our options for us so we don't have to declare them on the command line.  Using a configuration file is a nice way of formalizing your rules and
 quickly sharing them with others. Invoking ``pylint --generate-rcfile`` will create a sample rcfile with all the options set and explained in comments.

That's it for the basic intro. More tutorials will follow.

.. _`read up`: https://docs.python.org/library/re.html
