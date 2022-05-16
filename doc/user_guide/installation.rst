.. _installation:

Installation
============

Command line
------------

Pylint is installable using a package manager. Your package manager will find a version that
works with your interpreter. We recommend ``pip``:

.. code-block:: sh

   pip install pylint

Use the newest Python interpreter if you can.

It's possible to analyse code written for older interpreters by using the ``py-version``
option and setting it to the old interpreter. For example you can check that there are
no ``f-strings`` in Python 3.5 code using Python 3.8 with an up-to-date pylint even if
Python 3.5 is past end of life (EOL).

We do not guarantee that ``py-version`` will work for all EOL python interpreters indefinitely,
(for anything before python 3.5, it's probably not). If a newer version does not work for you,
the best available pylint might be an old version that works with your old interpreter but
without the bug fixes and feature of later versions.

NB: You can also use ``conda`` or your system package manager on debian based OS.
These package managers lag a little behind as they are maintained by a separate
entity on a slower release cycle.

.. code-block:: sh

   conda install pylint

.. code-block:: sh

   sudo apt-get install pylint


Editor integration
------------------

.. _ide-integration:

- Eclipse_
- Emacs_
- `Eric IDE`_ in the `Project > Check` menu,
- gedit_ (`another option for gedit`_)
- :ref:`Flymake <pylint_in_flymake>`
- `Jupyter Notebook`_
- Komodo_
- :ref:`PyCharm <pylint_in_pycharm>`
- PyDev_
- pyscripter_ in the `Tool -> Tools` menu.
- Spyder_ in the `View -> Panes -> Static code analysis`
- :ref:`TextMate <pylint_in_textmate>`
- Vim_
- :ref:`Visual Studio Code <visual-studio-code>` in the `Preferences -> Settings` menu
- `Visual Studio`_ in the `Python > Run PyLint` command on a project's context menu.
- WingIDE_

.. _Eclipse: https://www.pydev.org/manual_adv_pylint.html
.. _Emacs: https://www.emacswiki.org/emacs/PythonProgrammingInEmacs
.. _Eric IDE: https://eric-ide.python-projects.org/
.. _gedit: https://launchpad.net/gedit-pylint-2
.. _another option for gedit: https://wiki.gnome.org/Apps/Gedit/PylintPlugin
.. _Jupyter Notebook:  https://github.com/nbQA-dev/nbQA
.. _Komodo: https://mateusz.loskot.net/post/2006/01/15/running-pylint-from-komodo/
.. _pydev: https://www.pydev.org/manual_adv_pylint.html
.. _pyscripter: https://github.com/pyscripter/pyscripter
.. _spyder: https://docs.spyder-ide.org/current/panes/pylint.html
.. _Vim: https://www.vim.org/scripts/script.php?script_id=891
.. _Visual Studio: https://docs.microsoft.com/visualstudio/python/code-pylint
.. _WingIDE: https://wingware.com/doc/warnings/external-checkers
