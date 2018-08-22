
README for Pylint - http://pylint.pycqa.org/
============================================

.. image:: https://travis-ci.org/PyCQA/pylint.svg?branch=master
    :target: https://travis-ci.org/PyCQA/pylint

.. image:: https://ci.appveyor.com/api/projects/status/rbvwhakyj1y09atb/branch/master?svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/PCManticore/pylint

.. image:: https://coveralls.io/repos/github/PyCQA/pylint/badge.svg?branch=master
    :target: https://coveralls.io/github/PyCQA/pylint?branch=master


.. image:: https://img.shields.io/pypi/v/pylint.svg
    :alt: Pypi Package version
    :target: https://pypi.python.org/pypi/pylint

.. image:: https://readthedocs.org/projects/pylint/badge/?version=latest
    :target: http://pylint.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Pylint is a Python static code analysis tool which looks for programming errors,
helps enforcing a coding standard, sniffs for code smells and offers simple refactoring
suggestions.

It's highly configurable, having special pragmas to control its errors and warnings
from within your code, as well as from an extensive configuration file.
It is also possible to write your own plugins for adding your own checks or for
extending pylint in one way or another.

It's a free software distributed under the GNU General Public Licence.

Development is hosted on GitHub: https://github.com/PyCQA/pylint/

You can use the code-quality@python.org mailing list to discuss about
Pylint. Subscribe at https://mail.python.org/mailman/listinfo/code-quality/
or read the archives at https://mail.python.org/pipermail/code-quality/

Pull requests are amazing and most welcome.

Install
-------

Pylint can be simply installed by running::

    pip install pylint


If you want to install from a source distribution, extract the tarball and run
the following command ::

    python setup.py install


Do make sure to do the same for astroid, which is used internally by pylint.

For debian and rpm packages, use your usual tools according to your Linux distribution.

More information about installation and available distribution format
can be found here_.

Documentation
-------------

The documentation lives at http://pylint.pycqa.org/.

Pylint is shipped with following additional commands:

* pyreverse: an UML diagram generator
* symilar: an independent similarities checker
* epylint: Emacs and Flymake compatible Pylint


Testing
-------

We use tox_ for running the test suite. You should be able to install it with::

    pip install tox pytest


To run the test suite for a particular Python version, you can do::

    tox -e py27


For more detailed information, check the documentation.

.. _here: http://pylint.pycqa.org/en/latest/user_guide/installation.html
.. _tox: https://tox.readthedocs.io/en/latest/
