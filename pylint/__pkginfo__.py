# pylint: disable=W0622,C0103
# Copyright (c) 2003-2014 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""pylint packaging information"""
from __future__ import absolute_import

import sys
from os.path import join


modname = distname = 'pylint'

numversion = (1, 5, 6)
version = '.'.join([str(num) for num in numversion])

install_requires = [
    'astroid>=1.4.5,<1.5.0',
    'six',
]

if sys.platform == 'win32':
    install_requires.append('colorama')


license = 'GPL'
description = "python code static checker"
web = 'http://www.pylint.org'
mailinglist = "mailto://code-quality@python.org"
author = 'Logilab'
author_email = 'python-projects@lists.logilab.org'

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
