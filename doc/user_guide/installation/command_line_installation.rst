.. _installation:

Command line installation
-------------------------

Pylint is installable using a package manager. Your package manager will find a version that
works with your interpreter. We recommend ``pip``:

.. code-block:: sh

   pip install pylint

Use the newest Python interpreter if you can.

It's possible to analyse code written for older interpreters by using the ``py-version``
option and setting it to the old interpreter. For example you can check that there are
no ``f-strings`` in Python 3.5 code using Python 3.8 with an up-to-date Pylint even if
Python 3.5 is past end of life (EOL).

We do not guarantee that ``py-version`` will work for all EOL python interpreters indefinitely,
(for anything before python 3.5, it probably won't). If a newer version does not work for you,
the best available Pylint might be an old version that works with your old interpreter but
without the bug fixes and features of later versions.

.. note::
    You can also use ``conda`` or your system package manager on debian based OS.
    These package managers lag a little behind as they are maintained by a separate
    entity on a slower release cycle.

    .. code-block:: sh

       conda install pylint

    .. code-block:: sh

       sudo apt-get install pylint
