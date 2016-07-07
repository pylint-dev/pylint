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
from __future__ import absolute_import, print_function
__docformat__ = "restructuredtext en"

import os
import sys
import shutil
from os.path import isdir, exists, join

try:
    if os.environ.get('NO_SETUPTOOLS'):
        raise ImportError()
    from setuptools import setup
    from setuptools.command import easy_install as easy_install_lib
    from setuptools.command import install_lib
    USE_SETUPTOOLS = 1
except ImportError:
    from distutils.core import setup
    from distutils.command import install_lib
    USE_SETUPTOOLS = 0
    easy_install_lib = None

from distutils.command.build_py import build_py


base_dir = os.path.dirname(__file__)

__pkginfo__ = {}
with open(os.path.join(base_dir, "pylint", "__pkginfo__.py")) as f:
    exec(f.read(), __pkginfo__)
modname = __pkginfo__['modname']
distname = __pkginfo__.get('distname', modname)
scripts = __pkginfo__.get('scripts', [])
data_files = __pkginfo__.get('data_files', None)
include_dirs = __pkginfo__.get('include_dirs', [])
ext_modules = __pkginfo__.get('ext_modules', None)
install_requires = __pkginfo__.get('install_requires', None)
dependency_links = __pkginfo__.get('dependency_links', [])
extras_require = __pkginfo__.get('extras_require', {})

readme_path = join(base_dir, 'README')
if exists(readme_path):
    with open(readme_path) as stream:
        long_description = stream.read()
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


def _filter_tests(files):
    testdir = join('pylint', 'test')
    return [f for f in files if testdir not in f]


class MyInstallLib(install_lib.install_lib):
    """extend install_lib command to handle package __init__.py and
    include_dirs variable if necessary
    """
    def run(self):
        """overridden from install_lib class"""
        install_lib.install_lib.run(self)
        # manually install included directories if any
        if include_dirs:
            for directory in include_dirs:
                dest = join(self.install_dir, directory)
                if sys.version_info >= (3, 0):
                    exclude = set(['invalid_encoded_data*',
                                   'unknown_encoding*'])
                else:
                    exclude = set()
                shutil.rmtree(dest, ignore_errors=True)
                shutil.copytree(directory, dest,
                                ignore=shutil.ignore_patterns(*exclude))

    # override this since pip/easy_install attempt to byte compile test data
    # files, some of them being syntactically wrong by design, and this scares
    # the end-user
    def byte_compile(self, files):
        files = _filter_tests(files)
        install_lib.install_lib.byte_compile(self, files)


if easy_install_lib:
    class easy_install(easy_install_lib.easy_install):
        # override this since pip/easy_install attempt to byte compile
        # test data files, some of them being syntactically wrong by design,
        # and this scares the end-user
        def byte_compile(self, files):
            files = _filter_tests(files)
            easy_install_lib.easy_install.byte_compile(self, files)


def install(**kwargs):
    """setup entry point"""
    if USE_SETUPTOOLS:
        if '--force-manifest' in sys.argv:
            sys.argv.remove('--force-manifest')
    # install-layout option was introduced in 2.5.3-1~exp1
    elif sys.version_info < (2, 5, 4) and '--install-layout=deb' in sys.argv:
        sys.argv.remove('--install-layout=deb')
    packages = [modname] + get_packages(join(base_dir, 'pylint'), modname)
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
    cmdclass = {'install_lib': MyInstallLib,
                'build_py': build_py}
    if easy_install_lib:
        cmdclass['easy_install'] = easy_install
    return setup(name=distname,
                 version=__pkginfo__['version'],
                 license=__pkginfo__['license'],
                 description=__pkginfo__['description'],
                 long_description=long_description,
                 author=__pkginfo__['author'],
                 author_email=__pkginfo__['author_email'],
                 url=__pkginfo__['web'],
                 scripts=ensure_scripts(scripts),
                 classifiers=__pkginfo__['classifiers'],
                 data_files=data_files,
                 ext_modules=ext_modules,
                 cmdclass=cmdclass,
                 extras_require=extras_require,
                 **kwargs)

if __name__ == '__main__':
    install()
