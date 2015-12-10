
.. image:: https://drone.io/bitbucket.org/logilab/pylint/status.png
    :alt: drone.io Build Status
    :target: https://drone.io/bitbucket.org/logilab/pylint

README for Pylint - http://www.pylint.org/
==========================================

Pylint is a Python source code analyzer which looks for programming errors,
helps enforcing a coding standard and sniffs for some code smells (as defined in
Martin Fowler's Refactoring book).

Pylint has many rules enabled by default, way too much to silence them all on a
minimally sized program. It's highly configurable and handle pragmas to control
it from within your code. Additionally, it is possible to write plugins to add
your own checks.

It's a free software distributed under the GNU Public Licence.

Development is hosted on bitbucket: https://bitbucket.org/logilab/pylint/

You can use the code-quality@python.org mailing list to discuss about
Pylint. Subscribe at https://mail.python.org/mailman/listinfo/code-quality/
or read the archives at https://mail.python.org/pipermail/code-quality/

Install
-------

Pylint requires astroid package (the later the better).

* https://bitbucket.org/logilab/astroid

Installation should be as simple as ::

    python -m pip install astroid


If you want to install from a source distribution, extract the tarball and run
the following commands ::

    hg update master
    python setup.py install

You'll have to install dependencies in a similar way. For debian and
rpm packages, use your usual tools according to your Linux distribution.

More information about installation and available distribution format
may be found in the user manual in the *doc* subdirectory.

Documentation
-------------

Look in the doc/ subdirectory or at http://docs.pylint.org

Pylint is shipped with following additional commands:

* pyreverse: an UML diagram generator
* symilar: an independent similarities checker
* epylint: Emacs and Flymake compatible Pylint
* pylint-gui: a graphical interface