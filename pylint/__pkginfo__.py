# Copyright (c) 2003-2016 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

# pylint: disable=W0622,C0103
"""pylint packaging information"""
from __future__ import absolute_import

from os.path import join


modname = distname = 'pylint'

numversion = (1, 6, 4)
version = '.'.join([str(num) for num in numversion])

install_requires = [
    'astroid>=1.4.5,<1.5.0',
    'six',
    'isort >= 4.2.5',
    'mccabe',
]

extras_require = {}
extras_require[':sys_platform=="win32"'] = ['colorama']
extras_require[':python_version=="2.7"'] = ['configparser', 'backports.functools_lru_cache']


license = 'GPL'
description = "python code static checker"
web = 'https://github.com/PyCQA/pylint'
mailinglist = "mailto:code-quality@python.org"
author = 'Python Code Quality Authority'
author_email = 'code-quality@python.org'

classifiers = ['Development Status :: 4 - Beta',
               'Environment :: Console',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: GNU General Public License (GPL)',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 2',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development :: Debuggers',
               'Topic :: Software Development :: Quality Assurance',
               'Topic :: Software Development :: Testing'
              ]


long_desc = """\
 Pylint is a Python source code analyzer which looks for programming
 errors, helps enforcing a coding standard and sniffs for some code
 smells (as defined in Martin Fowler's Refactoring book)
 .
 Pylint can be seen as another PyChecker since nearly all tests you
 can do with PyChecker can also be done with Pylint. However, Pylint
 offers some more features, like checking length of lines of code,
 checking if variable names are well-formed according to your coding
 standard, or checking if declared interfaces are truly implemented,
 and much more.
 .
 Additionally, it is possible to write plugins to add your own checks.
 .
 Pylint is shipped with "pylint-gui", "pyreverse" (UML diagram generator)
 and "symilar" (an independent similarities checker)."""

scripts = [join('bin', filename)
           for filename in ('pylint', 'pylint-gui', "symilar", "epylint",
                            "pyreverse")]

include_dirs = [join('pylint', 'test')]
