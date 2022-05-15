.. _installation:

Installation
============

Command line
------------

Pylint is installable using a package manager. Your package manager will
find a version that works with your interpreter. For example with pip:

.. code-block:: sh

   pip install pylint

Use the newest Python interpreter if you can.

It's possible to analyse code written for older interpreters by using the ``py-version``
option and setting it to the old interpreter. For example you can check that there are
no ``f-strings`` in Python 3.5 code using Python 3.8 with an up-to-date pylint even if
Python 3.5 is past end of life (EOL).

We do not guarantee that ``py-version`` will work for all EOL python interpreter indefinitely,
(for anything before python 3.5, it's probably not). If a newer version does not work for you,
the best available pylint might be an old version that works with your old interpreter but
without the bug fixes and feature of latest pylints.

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

To use Pylint with:

 - Emacs_, see https://www.emacswiki.org/emacs/PythonProgrammingInEmacs,
 - Vim_, see https://www.vim.org/scripts/script.php?script_id=891,
 - `Visual Studio`_, see https://docs.microsoft.com/visualstudio/python/code-pylint,
 - Eclipse_ and PyDev_, see https://www.pydev.org/manual_adv_pylint.html,
 - Komodo_, see https://mateusz.loskot.net/post/2006/01/15/running-pylint-from-komodo/,
 - gedit_, see https://launchpad.net/gedit-pylint-2 or https://wiki.gnome.org/Apps/Gedit/PylintPlugin,
 - WingIDE_, see https://wingware.com/doc/warnings/external-checkers,
 - PyCharm_, see :ref:`the section below <pylint_in_pycharm>`,
 - TextMate_, see :ref:`the section below <pylint_in_textmate>`
 - `Visual Studio Code`_, see https://code.visualstudio.com/docs/python/linting,
 - `Visual Studio Code`_ Pylint Extension see, https://marketplace.visualstudio.com/items?itemName=ms-python.pylint,
 - `Visual Studio`_, see https://docs.microsoft.com/en-us/visualstudio/python/linting-python-code,
 - `Jupyter Notebook`_, see https://github.com/nbQA-dev/nbQA,

Pylint is integrated in:

 - `Visual Studio`_, see the `Python > Run PyLint` command on a project's context menu.
 - Eric_ IDE, see the `Project > Check` menu,
 - Spyder_, see the `View -> Panes -> Static code analysis` pane and
   its `corresponding documentation <https://docs.spyder-ide.org/current/panes/pylint.html>`_.
 - pyscripter_, see the `Tool -> Tools` menu.
 - `Visual Studio Code`_, see the `Preferences -> Settings` menu.

.. _Emacs: https://www.gnu.org/software/emacs/
.. _Vim: https://www.vim.org/
.. _Visual Studio: https://visualstudio.microsoft.com/
.. _Eclipse: https://www.eclipse.org/
.. _Eric: https://eric-ide.python-projects.org/
.. _pyscripter: https://github.com/pyscripter/pyscripter
.. _pydev: https://www.pydev.org/
.. _Komodo: https://www.activestate.com/products/komodo-ide/
.. _gedit: https://wiki.gnome.org/Apps/Gedit
.. _WingIDE: https://www.wingware.com/
.. _spyder: https://www.spyder-ide.org/
.. _PyCharm: https://www.jetbrains.com/pycharm/
.. _TextMate: https://macromates.com
.. _Visual Studio Code: https://code.visualstudio.com/
.. _Jupyter Notebook: https://jupyter.org/
