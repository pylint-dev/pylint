.. _pylint_in_textmate:

Integrate Pylint with TextMate
==============================

Install Pylint in the usual way::

    pip install pylint

Install the `Python bundle for TextMate <https://github.com/textmate/python.tmbundle>`_:

#.  select *TextMate* > *Preferences*
#.  select the *Bundles* tab
#.  find and tick the *Python* bundle in the list

You should now see it in *Bundles* > *Python*.

In *Preferences*, select the *Variables* tab. If a ``TM_PYCHECKER`` variable is not already listed, add
it, with the value ``pylint``.

The default keyboard shortcut to run the syntax checker is *Control-Shift-V* - open a ``.py`` file
in Textmate, and try it.

You should see the output in a new window:

    PyCheckMate 1.2 – Pylint 1.4.4

    No config file found, using default configuration

Then all is well, and most likely Pylint will have expressed some opinions about your Python code
(or will exit with ``0`` if your code already conforms to its expectations).

If you receive a message:

    Please install PyChecker, PyFlakes, Pylint, PEP 8 or flake8 for more extensive code checking.

That means that Pylint wasn't found, which is likely an issue with command paths - TextMate needs
be looking for Pylint on the right paths.

Check where Pylint has been installed, using ``which``::

    $ which pylint
    /usr/local/bin/pylint

The output will tell you where Pylint can be found; in this case, in ``/usr/local/bin``.

#. select *TextMate* > *Preferences*
#. select the *Variables* tab
#. find and check that a ``PATH`` variable exists, and that it contains the appropriate path (if
   the path to Pylint were ``/usr/local/bin/pylint`` as above, then the variable would need to
   contain ``/usr/local/bin``). An actual example in this case might be
   ``$PATH:/opt/local/bin:/usr/local/bin:/usr/texbin``, which includes other paths.

... and try running Pylint again.
