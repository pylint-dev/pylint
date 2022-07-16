.. _installation:

Command line installation
-------------------------

Pylint is installable using a package manager. Your package manager will find a version that
works with your interpreter. We recommend ``pip``:

.. code-block:: sh

   pip install pylint

Or if you want to also check spelling with ``enchant`` (you might need to
`install the enchant C library <https://pyenchant.github.io/pyenchant/install.html#installing-the-enchant-c-library>`_):

.. code-block:: sh

   pip install pylint[spelling]

The newest pylint support python interpreters that are not past end of life.

.. note::
    You can also use ``conda`` or your system package manager on debian based OS.
    These package managers lag a little behind as they are maintained by a separate
    entity on a slower release cycle.

    .. code-block:: sh

       conda install pylint

    .. code-block:: sh

       sudo apt-get install pylint
