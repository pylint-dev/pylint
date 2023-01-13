
***************************
 What's New in Pylint 2.16
***************************

.. toctree::
   :maxdepth: 2

:Release:2.16
:Date: TBA

Summary -- Release highlights
=============================

In 2.16.0 we added aggregation and composition understanding in ``pyreverse``, and a way to clear
the cache in between run in server mode (originally for the VS Code integration). Apart from the bug
fixes there's also a lot of new checks, and new extensions that have been asked for for a long time
that were implemented.

If you want to benefit from all the new checks load the following plugins::

    pylint.extensions.dict_init_mutate,
    pylint.extensions.dunder,
    pylint.extensions.typing,
    pylint.extensions.magic_value,

We still welcome any community effort to help review, integrate, and add good/bad examples to the doc for
<https://github.com/PyCQA/pylint/issues/5953>`_. This should be doable without any ``pylint`` or ``astroid``
knowledge, so this is the perfect entrypoint if you want to contribute to ``pylint`` or open source without
any experience with our code!

Last but not least @clavedeluna and @nickdrozd became triagers, welcome to the team !

.. towncrier release notes start
