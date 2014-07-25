#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0404,W0622,W0704,W0613
# copyright 2003-2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of pylint.
#
# pylint is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option) any
# later version.
#
# pylint is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with pylint.  If not, see <http://www.gnu.org/licenses/>.
"""Generic Setup script, takes package info from __pkginfo__.py file.
"""
__docformat__ = "restructuredtext en"

import os
import sys
import shutil
from os.path import isdir, exists, join

try:
    if os.environ.get('NO_SETUPTOOLS'):
        raise ImportError()
    from setuptools import setup
    from setuptools.command import install_lib
    USE_SETUPTOOLS = 1
except ImportError:
    from distutils.core import setup
    from distutils.command import install_lib
    USE_SETUPTOOLS = 0

try:
    # pylint: disable=no-name-in-module
    # python3
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    # pylint: disable=no-name-in-module
    # python2.x
    from distutils.command.build_py import build_py

sys.modules.pop('__pkginfo__', None)
# import optional features
__pkginfo__ = __import__("__pkginfo__")
# import required features
from __pkginfo__ import modname, version, license, description, \
     web, author, author_email, classifiers

distname = getattr(__pkginfo__, 'distname', modname)
scripts = getattr(__pkginfo__, 'scripts', [])
data_files = getattr(__pkginfo__, 'data_files', None)
subpackage_of = getattr(__pkginfo__, 'subpackage_of', None)
include_dirs = getattr(__pkginfo__, 'include_dirs', [])
ext_modules = getattr(__pkginfo__, 'ext_modules', None)
install_requires = getattr(__pkginfo__, 'install_requires', None)
dependency_links = getattr(__pkginfo__, 'dependency_links', [])

STD_BLACKLIST = ('CVS', '.svn', '.hg', 'debian', 'dist', 'build')

IGNORED_EXTENSIONS = ('.pyc', '.pyo', '.elc', '~')

if exists('README'):
    long_description = open('README').read()
else:
    long_description = ''

def ensure_scripts(linux_scripts):
    """Creates the proper script names required for each platform
    (taken from 4Suite)
    """
    from distutils import util
    if util.get_platform()[:3] == 'win':
        return linux_scripts + [script + '.bat' for script in linux_scripts]
    return linux_scripts

def get_packages(directory, prefix):
    """return a list of subpackages for the given directory"""
    result = []
    for package in os.listdir(directory):
        absfile = join(directory, package)
        if isdir(absfile):
            if exists(join(absfile, '__init__.py')):
                if prefix:
                    result.append('%s.%s' % (prefix, package))
                else:
                    result.append(package)
                result += get_packages(absfile, result[-1])
    return result

EMPTY_FILE = '''"""generated file, don't modify or your data will be lost"""
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    pass
'''

class MyInstallLib(install_lib.install_lib):
    """extend install_lib command to handle package __init__.py and
    include_dirs variable if necessary
    """
    def run(self):
        """overridden from install_lib class"""
        install_lib.install_lib.run(self)
        # create Products.__init__.py if needed
        if subpackage_of:
            product_init = join(self.install_dir, subpackage_of, '__init__.py')
            if not exists(product_init):
                self.announce('creating %s' % product_init)
                stream = open(product_init, 'w')
                stream.write(EMPTY_FILE)
                stream.close()
        # manually install included directories if any
        if include_dirs:
            if subpackage_of:
                base = join(subpackage_of, modname)
            else:
                base = modname
            for directory in include_dirs:
                dest = join(self.install_dir, base, directory)
                if sys.version_info >= (3, 0):
                    exclude = set(('func_unknown_encoding.py',
                                   'func_invalid_encoded_data.py'))
                else:
                    exclude = set()
                shutil.rmtree(dest, ignore_errors=True)
                shutil.copytree(directory, dest)
                # since python2.5's copytree doesn't support the ignore
                # parameter, the following loop to remove the exclude set
                # was added
                for (dirpath, _, filenames) in os.walk(dest):
                    for n in filenames:
                        if n in exclude:
                            os.remove(os.path.join(dirpath, n))
                if sys.version_info >= (3, 0):
                    # process manually python file in include_dirs (test data)
                    # pylint: disable=no-name-in-module
                    from distutils.util import run_2to3
                    print('running 2to3 on', dest)
                    run_2to3([dest])

    # override this since pip/easy_install attempt to byte compile test data
    # files, some of them being syntactically wrong by design, and this scares
    # the end-user
    def byte_compile(self, files):
        testdir = join('pylint', 'test')
        files = [f for f in files if testdir not in f]
        install_lib.install_lib.byte_compile(self, files)

def install(**kwargs):
    """setup entry point"""
    if USE_SETUPTOOLS:
        if '--force-manifest' in sys.argv:
            sys.argv.remove('--force-manifest')
    # install-layout option was introduced in 2.5.3-1~exp1
    elif sys.version_info < (2, 5, 4) and '--install-layout=deb' in sys.argv:
        sys.argv.remove('--install-layout=deb')
    if subpackage_of:
        package = subpackage_of + '.' + modname
        kwargs['package_dir'] = {package : '.'}
        packages = [package] + get_packages(os.getcwd(), package)
        if USE_SETUPTOOLS:
            kwargs['namespace_packages'] = [subpackage_of]
    else:
        kwargs['package_dir'] = {modname : '.'}
        packages = [modname] + get_packages(os.getcwd(), modname)
    if USE_SETUPTOOLS:
        if install_requires:
            kwargs['install_requires'] = install_requires
            kwargs['dependency_links'] = dependency_links
        kwargs['entry_points'] = {'console_scripts': [
            'pylint = pylint:run_pylint',
            'pylint-gui = pylint:run_pylint_gui',
            'epylint = pylint:run_epylint',
            'pyreverse = pylint:run_pyreverse',
            'symilar = pylint:run_symilar',
        ]}
    kwargs['packages'] = packages
    return setup(name=distname,
                 version=version,
                 license=license,
                 description=description,
                 long_description=long_description,
                 author=author,
                 author_email=author_email,
                 url=web,
                 scripts=ensure_scripts(scripts),
                 classifiers=classifiers,
                 data_files=data_files,
                 ext_modules=ext_modules,
                 cmdclass={'install_lib': MyInstallLib,
                           'build_py': build_py},
                 **kwargs)

if __name__ == '__main__':
    install()
