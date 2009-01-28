#!/usr/bin/env python
# pylint: disable-msg=W0404,W0622,W0704,W0613,W0152
"""Generic Setup script, takes package info from __pkginfo__.py file.

:copyright: 2003-2009 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: General Public License version 2 - http://www.gnu.org/licenses
"""
__docformat__ = "restructuredtext en"

import os
import sys
import shutil
from os.path import isdir, exists, join, walk

try:
    from setuptools import setup
    from setuptools.command import install_lib
    USE_SETUPTOOLS = 1
except ImportError:    
    from distutils.core import setup
    from distutils.command import install_lib
    USE_SETUPTOOLS = 0
    

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
    from __pkginfo__ import data_files
except ImportError:
    data_files = None
try:
    from __pkginfo__ import subpackage_of
except ImportError:
    subpackage_of = None
try:
    from __pkginfo__ import include_dirs
except ImportError:
    include_dirs = []
try:
    from __pkginfo__ import ext_modules
except ImportError:
    ext_modules = None
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
        scripts_ = [script + '.bat' for script in linux_scripts]
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
            if exists(join(absfile, '__init__.py')) or \
                   package in ('test', 'tests'):
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


EMPTY_FILE = '''"""generated file, don\'t modify or your data will be lost"""
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    pass
'''

class MyInstallLib(install_lib.install_lib):
    """extend install_lib command to handle  package __init__.py and
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
                export(directory, dest)
        
def install(**kwargs):
    """setup entry point"""
    if subpackage_of:
        package = subpackage_of + '.' + modname
        kwargs['package_dir'] = {package : '.'}
        packages = [package] + get_packages(os.getcwd(), package)
        if USE_SETUPTOOLS:
            kwargs['namespace_packages'] = [subpackage_of]
    else:
        kwargs['package_dir'] = {modname : '.'}
        packages = [modname] + get_packages(os.getcwd(), modname)
    if USE_SETUPTOOLS and install_requires:
        kwargs['install_requires'] = install_requires
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
                 data_files = data_files,
                 ext_modules = ext_modules,
                 cmdclass = {'install_lib': MyInstallLib},
                 **kwargs
                 )
            
if __name__ == '__main__' :
    install()
