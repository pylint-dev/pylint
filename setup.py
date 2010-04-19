#!/usr/bin/env python
# pylint: disable=W0404,W0622,W0704,W0613
"""Generic Setup script, takes package info from __pkginfo__.py file.

:copyright: 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: General Public License version 2 - http://www.gnu.org/licenses
"""
__docformat__ = "restructuredtext en"

import os
import sys
import shutil
from os.path import isdir, exists, join, walk

# FIXME : setup.py doesn't work with setuptools so we use distutils

try:
    if os.environ.get('NO_SETUPTOOLS'):
        raise ImportError()
    from setuptools import setup
    USE_SETUPTOOLS = 1
except ImportError:
    from distutils.core import setup
    USE_SETUPTOOLS = 0
#assert USE_SETUPTOOLS

sys.modules.pop('__pkginfo__', None)
# import required features
from __pkginfo__ import modname, version, license, short_desc, long_desc, \
     web, author, author_email, classifiers
# import optional features
try:
    from __pkginfo__ import distname
except ImportError:
    distname = modname
try:
    from __pkginfo__ import scripts
except ImportError:
    scripts = []
try:
    from __pkginfo__ import install_requires
except ImportError:
    install_requires = None

STD_BLACKLIST = ('CVS', '.svn', '.hg', 'debian', 'dist', 'build')

IGNORED_EXTENSIONS = ('.pyc', '.pyo', '.elc', '~')


def ensure_scripts(linux_scripts):
    """
    Creates the proper script names required for each platform
    (taken from 4Suite)
    """
    from distutils import util
    if util.get_platform()[:3] == 'win':
        scripts_ = linux_scripts + [script + '.bat'
                for script in linux_scripts]
    else:
        scripts_ = linux_scripts
    return scripts_


def get_packages(directory, prefix):
    """return a list of subpackages for the given directory
    """
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

def export(from_dir, to_dir,
           blacklist=STD_BLACKLIST,
           ignore_ext=IGNORED_EXTENSIONS):
    """make a mirror of from_dir in to_dir, omitting directories and files
    listed in the black list
    """
    def make_mirror(arg, directory, fnames):
        """walk handler"""
        for norecurs in blacklist:
            try:
                fnames.remove(norecurs)
            except ValueError:
                pass
        for filename in fnames:
            # don't include binary files
            if filename[-4:] in ignore_ext:
                continue
            if filename[-1] == '~':
                continue
            src = join(directory, filename)
            dest = to_dir + src[len(from_dir):]
            print >> sys.stderr, src, '->', dest
            if os.path.isdir(src):
                if not exists(dest):
                    os.mkdir(dest)
            else:
                if exists(dest):
                    os.remove(dest)
                shutil.copy2(src, dest)
    try:
        os.mkdir(to_dir)
    except OSError, ex:
        # file exists ?
        import errno
        if ex.errno != errno.EEXIST:
            raise
    walk(from_dir, make_mirror, None)


def install(**kwargs):
    """setup entry point"""
    kwargs['package_dir'] = {modname : '.'}
    packages = [modname] + get_packages(os.getcwd(), modname)
    if USE_SETUPTOOLS:
        if install_requires:
            kwargs['install_requires'] = install_requires
        if '--force-manifest' in sys.argv:
            sys.argv.remove('--force-manifest')
    kwargs['packages'] = packages
    return setup(name = distname,
                 version = version,
                 license = license,
                 description = short_desc,
                 long_description = long_desc,
                 author = author,
                 author_email = author_email,
                 url = web,
                 classifiers = classifiers,
                 scripts = ensure_scripts(scripts),
                 **kwargs
                 )

if __name__ == '__main__' :
    install()
