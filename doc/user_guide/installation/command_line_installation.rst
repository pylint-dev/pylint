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

The newest pylint supports all Python interpreters that are not past end of life.

We recommend to use the latest interpreter because we rely on the ``ast`` builtin
module that gets better with each new Python interpreter. For example a Python
3.6 interpreter can't analyse 3.8 syntax (amongst others, because of the new walrus operator) while a 3.8
interpreter can also deal with Python 3.6. See :ref:`using pylint with multiple interpreters <continuous-integration>` for more details.

.. note::
    You can also use ``conda`` or your system package manager on debian based OS.
    These package managers lag a little behind as they are maintained by a separate
    entity on a slower release cycle.

    .. code-block:: sh

       conda install pylint

    .. code-block:: sh

       sudo apt-get install pylint
