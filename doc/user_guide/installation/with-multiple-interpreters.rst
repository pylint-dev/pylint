.. _continuous-integration:

Installation with multiple interpreters
=======================================

It's possible to analyse code written for older or multiple interpreters by using
the ``py-version`` option and setting it to the oldest supported interpreter of your code. For example you can check
that there are no ``f-strings`` in Python 3.5 code using Python 3.8 with an up-to-date
pylint even if Python 3.5 is past end of life (EOL) and the version of pylint you use is not
compatible with it.

We do not guarantee that ``py-version`` will work for all EOL Python interpreters indefinitely,
(for anything before Python 3.5, it probably won't). If a newer version does not work for you,
the best available pylint might be an old version that works with your old interpreter but
without the bug fixes and features of later versions.
