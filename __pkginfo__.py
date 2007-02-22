# pylint: disable-msg=W0622,C0103
# Copyright (c) 2003-2007 LOGILAB S.A. (Paris, FRANCE).
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
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""pylint packaging information"""

modname = 'pylint'

numversion = (0, 13, 0)
version = '.'.join([str(num) for num in numversion])

license = 'GPL'
copyright = '''Copyright (c) 2003-2007 Sylvain Thenault (thenault@gmail.com).
Copyright (c) 2003-2007 LOGILAB S.A. (Paris, FRANCE).
http://www.logilab.fr/ -- mailto:contact@logilab.fr'''

short_desc = "python code static checker"
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
 Additionally, it is possible to write plugins to add your own checks."""

author = "Sylvain Thenault"
author_email = "sylvain.thenault@logilab.fr"

web = "http://www.logilab.org/project/name/%s" % modname
ftp = "ftp://ftp.logilab.org/pub/%s" % modname
mailinglist = "mailto://python-projects@logilab.org"

from os.path import join
scripts = [join('bin', filename)
           for filename in ('pylint', 'pylint-gui', "symilar")]

include_dirs = [join('test', 'input'), join('test', 'messages'),
                join('test', 'regrtest_data')]

pyversions = ["2.3", "2.4"]

debian_uploader = 'Alexandre Fayolle <afayolle@debian.org>'

classifiers =  ['Development Status :: 4 - Beta',
                'Environment :: Console',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: GNU General Public License (GPL)',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Topic :: Software Development :: Debuggers',
                'Topic :: Software Development :: Quality Assurance',
                'Topic :: Software Development :: Testing',
                ]
