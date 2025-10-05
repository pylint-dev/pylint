
***************************
 What's New in Pylint 4.0
***************************

.. toctree::
   :maxdepth: 2

:Release:4.0
:Date: TBA

Summary -- Release highlights
=============================

- Pylint now supports Python 3.14.

- Pylint's inference engine (``astroid``) is now much more precise,
  understanding implicit booleanness and ternary expressions. (Thanks @zenlyj!)

Consider this example:

.. code-block:: python

    class Result:
        errors: dict | None = None

    result = Result()
    if result.errors:
        result.errors[field_key]
        # inference engine understands result.errors cannot be None
        # pylint no longer raises unsubscriptable-object

The required ``astroid`` version is now 4.0.0. See the
`astroid changelog <https://pylint.readthedocs.io/projects/astroid/en/latest/changelog.html#what-s-new-in-astroid-4-0-0>`_
for additional fixes, features, and performance improvements applicable to pylint.

- Handling of ``invalid-name`` at the module level was patchy. Now,
  module-level constants that are reassigned are treated as variables and checked
  against ``--variable-rgx`` rather than ``--const-rgx``. Module-level lists,
  sets, and objects can pass against either regex.

Here, ``LIMIT`` is reassigned, so pylint only uses ``--variable-rgx``:

.. code-block:: python

    LIMIT = 500  # [invalid-name]
    if sometimes:
        LIMIT = 1  # [invalid-name]

If this is undesired, refactor using *exclusive* assignment so that it is
evident that this assignment happens only once:

.. code-block:: python

    if sometimes:
        LIMIT = 1
    else:
        LIMIT = 500  # exclusive assignment: uses const regex, no warning

Lists, sets, and objects still pass against either ``const-rgx`` or ``variable-rgx``
even if reassigned, but are no longer completely skipped:

.. code-block:: python

    MY_LIST = []
    my_list = []
    My_List = []  # [invalid-name]

Remember to adjust the
`regexes <https://pylint.readthedocs.io/en/latest/user_guide/messages/convention/invalid-name.html>`_
and
`allow lists <https://pylint.readthedocs.io/en/latest/user_guide/configuration/all-options.html#good-names>`_
to your liking.

.. towncrier release notes start
