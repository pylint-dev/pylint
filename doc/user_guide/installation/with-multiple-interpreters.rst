.. _continuous-integration:

Installation with multiple interpreters
=======================================

It's always possible and safer to check on each interpreters.

But, it's also possible to analyse code written for older interpreters by using
the ``py-version`` option and setting it to the old interpreter. For example you can check
that there are no ``f-strings`` in Python 3.5 code using Python 3.8 with an up-to-date
pylint even if Python 3.5 is past end of life (EOL) and the latest pylint are not
compatible with it.
