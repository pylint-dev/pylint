In order to be raised, this message need a `custom deprecation checker`_ (follow link for a full example).

Loading this custom checker using ``load-plugins`` would start raising ``deprecated-argument``.
The actual replacement then need to be studied on a case by case basis by reading the
deprecation warning or the release notes.

.. _`custom deprecation checker`: https://github.com/pylint-dev/pylint/blob/main/examples/deprecation_checker.py
