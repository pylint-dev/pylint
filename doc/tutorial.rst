.. _tutorial:

========
Tutorial
========

This tutorial is all about approaching coding standards with little or no
knowledge of in-depth programming or the code standards themselves.  It's the
equivalent of skipping the manual and jumping right in.

The command line prompt for these examples is:

.. sourcecode:: console

  tutor Desktop$

.. _PEP 8: https://peps.python.org/pep-0008/

Getting Started
---------------

Running Pylint with the ``--help`` arguments will give you an idea of the arguments
available. Do that now, i.e.:

.. sourcecode:: console

  pylint --help


A couple of the options that we'll focus on here are: ::

  Commands:
    --help-msg=<msg-id>
    --generate-toml-config
  Messages control:
    --disable=<msg-ids>
  Reports:
    --reports=<y or n>
    --output-format=<format>

If you need more detail, you can also ask for an even longer help message: ::

  pylint --long-help

Pay attention to the last bit of this longer help output. This gives you a
hint of what Pylint is going to ``pick on``: ::

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
is too ``noisy``.  The default configuration enforce a lot of warnings.
We'll use some of the options we noted above to make it suit your
preferences a bit better.

Your First Pylint'ing
---------------------

We'll use a basic Python script with ``black`` already applied on it,
as fodder for our tutorial. The starting code we will use is called
``simplecaesar.py`` and is here in its entirety:

.. sourcecode:: python

    #!/usr/bin/env python3

    import string

    shift = 3
    choice = input("would you like to encode or decode?")
    word = input("Please enter text")
    letters = string.ascii_letters + string.punctuation + string.digits
    encoded = ""
    if choice == "encode":
        for letter in word:
            if letter == " ":
                encoded = encoded + " "
            else:
                x = letters.index(letter) + shift
                encoded = encoded + letters[x]
    if choice == "decode":
        for letter in word:
            if letter == " ":
                encoded = encoded + " "
            else:
                x = letters.index(letter) - shift
                encoded = encoded + letters[x]

    print(encoded)


Let's get started. If we run this:

.. sourcecode:: console

    tutor Desktop$ pylint simplecaesar.py
    ************* Module simplecaesar
    simplecaesar.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    simplecaesar.py:5:0: C0103: Constant name "shift" doesn't conform to UPPER_CASE naming style (invalid-name)
    simplecaesar.py:8:0: C0103: Constant name "letters" doesn't conform to UPPER_CASE naming style (invalid-name)
    simplecaesar.py:9:0: C0103: Constant name "encoded" doesn't conform to UPPER_CASE naming style (invalid-name)
    simplecaesar.py:13:12: C0103: Constant name "encoded" doesn't conform to UPPER_CASE naming style (invalid-name)
    simplecaesar.py:15:12: C0103: Constant name "x" doesn't conform to UPPER_CASE naming style (invalid-name)
    simplecaesar.py:16:12: C0103: Constant name "encoded" doesn't conform to UPPER_CASE naming style (invalid-name)
    simplecaesar.py:20:12: C0103: Constant name "encoded" doesn't conform to UPPER_CASE naming style (invalid-name)
    simplecaesar.py:22:12: C0103: Constant name "x" doesn't conform to UPPER_CASE naming style (invalid-name)
    simplecaesar.py:23:12: C0103: Constant name "encoded" doesn't conform to UPPER_CASE naming style (invalid-name)

    -----------------------------------
    Your code has been rated at 4.74/10


We can see the second line is: ::

  "simplecaesar.py:1:0: C0114: Missing module docstring (missing-module-docstring)"

This basically means that line 1 at column 0 violates the convention ``C0114``.
Another piece of information is the message symbol between parens,
``missing-module-docstring``.

If we want to read up a bit more about that, we can go back to the
command line and try this:

.. sourcecode:: console

  tutor Desktop$ pylint --help-msg=missing-module-docstring
  :missing-module-docstring (C0114): *Missing module docstring*
    Used when a module has no docstring.Empty modules do not require a docstring.
    This message belongs to the basic checker.

That one was a bit of a no-brainer, but we can also run into error messages
where we are unfamiliar with the underlying code theory.

The Next Step
-------------

Now that we got some configuration stuff out of the way, let's see what we can
do with the remaining warnings. If we add a docstring to describe what the code
is meant to do that will help. There are ``invalid-name`` messages that we will
get to later. Here is the updated code:

.. sourcecode:: python

    #!/usr/bin/env python3

    """This script prompts a user to enter a message to encode or decode
    using a classic Caesar shift substitution (3 letter shift)"""

    import string

    shift = 3
    choice = input("would you like to encode or decode?")
    word = input("Please enter text")
    letters = string.ascii_letters + string.punctuation + string.digits
    encoded = ""
    if choice == "encode":
        for letter in word:
            if letter == " ":
                encoded = encoded + " "
            else:
                x = letters.index(letter) + shift
                encoded = encoded + letters[x]
    if choice == "decode":
        for letter in word:
            if letter == " ":
                encoded = encoded + " "
            else:
                x = letters.index(letter) - shift
                encoded = encoded + letters[x]

    print(encoded)

Here is what happens when we run it:

.. sourcecode:: console

    tutor Desktop$ pylint simplecaesar.py
    ************* Module simplecaesar
    simplecaesar.py:8:0: C0103: Constant name "shift" doesn't conform to UPPER_CASE naming style (invalid-name)
    simplecaesar.py:11:0: C0103: Constant name "letters" doesn't conform to UPPER_CASE naming style (invalid-name)
    simplecaesar.py:12:0: C0103: Constant name "encoded" doesn't conform to UPPER_CASE naming style (invalid-name)
    simplecaesar.py:16:12: C0103: Constant name "encoded" doesn't conform to UPPER_CASE naming style (invalid-name)
    simplecaesar.py:18:12: C0103: Constant name "x" doesn't conform to UPPER_CASE naming style (invalid-name)
    simplecaesar.py:19:12: C0103: Constant name "encoded" doesn't conform to UPPER_CASE naming style (invalid-name)
    simplecaesar.py:23:12: C0103: Constant name "encoded" doesn't conform to UPPER_CASE naming style (invalid-name)
    simplecaesar.py:25:12: C0103: Constant name "x" doesn't conform to UPPER_CASE naming style (invalid-name)
    simplecaesar.py:26:12: C0103: Constant name "encoded" doesn't conform to UPPER_CASE naming style (invalid-name)

    ------------------------------------------------------------------
    Your code has been rated at 5.26/10 (previous run: 4.74/10, +0.53)

Nice! Pylint told us how much our code rating has improved since our last run,
and we're down to just the ``invalid-name`` messages.

There are fairly well defined conventions around naming things like instance
variables, functions, classes, etc.  The conventions focus on the use of
UPPERCASE and lowercase as well as the characters that separate multiple words
in the name.  This lends itself well to checking via a regular expression, thus
the **should match (([A-Z\_][A-Z1-9\_]*)|(__.*__))$**.

In this case Pylint is telling us that those variables appear to be constants
and should be all UPPERCASE. This is an in-house convention that has lived with Pylint
since its inception. You too can create your own in-house naming
conventions but for the purpose of this tutorial, we want to stick to the `PEP 8`_
standard. In this case, the variables we declared should follow the convention
of all lowercase.  The appropriate rule would be something like:
"should match [a-z\_][a-z0-9\_]{2,30}$".  Notice the lowercase letters in the
regular expression (a-z versus A-Z).

If we run that rule using a ``--const-rgx='[a-z\_][a-z0-9\_]{2,30}$'`` option, it
will now be quite quiet:

.. sourcecode:: console

    tutor Desktop$ pylint simplecaesar.py --const-rgx='[a-z\_][a-z0-9\_]{2,30}$'
    ************* Module simplecaesar
    simplecaesar.py:18:12: C0103: Constant name "x" doesn't conform to '[a-z\\_][a-z0-9\\_]{2,30}$' pattern (invalid-name)
    simplecaesar.py:25:12: C0103: Constant name "x" doesn't conform to '[a-z\\_][a-z0-9\\_]{2,30}$' pattern (invalid-name)

    ------------------------------------------------------------------
    Your code has been rated at 8.95/10 (previous run: 5.26/10, +3.68)

You can `read up`_ on regular expressions or use `a website to help you`_.

.. tip::
 It would really be a pain to specify that regex on the command line all the time, particularly if we're using many other options.
 That's what a configuration file is for. We can configure our Pylint to
 store our options for us so we don't have to declare them on the command line.  Using a configuration file is a nice way of formalizing your rules and
 quickly sharing them with others. Invoking ``pylint --generate-toml-config`` will create a sample ``.toml`` section with all the options set and explained in comments.
 This can then be added to your ``pyproject.toml`` file or any other ``.toml`` file pointed to with the ``--rcfile`` option.

.. _`read up`: https://docs.python.org/library/re.html
.. _`a website to help you`: https://regex101.com/
