# -*- coding: utf-8 -*-
#!/usr/bin/env python
# pylint: disable=W0404,W0622,W0613
# Copyright (c) 2006, 2009-2010, 2012-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2010 Julien Jehannet <julien.jehannet@logilab.fr>
# Copyright (c) 2012 FELD Boris <lothiraldan@gmail.com>
# Copyright (c) 2013 Benedikt Morbach <benedikt.morbach@googlemail.com>
# Copyright (c) 2013 T.Rzepka <Tobias.Rzepka@gmail.com>
# Copyright (c) 2014-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Pedro Algarvio <pedro@algarvio.me>
# Copyright (c) 2014 Brett Cannon <brett@python.org>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2014 Ricardo Gemignani <ricardo.gemignani@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Florian Bruhin <me@the-compiler.org>
# Copyright (c) 2017 Hugo <hugovk@users.noreply.github.com>
# Copyright (c) 2019 Enji Cooper <yaneurabeya@gmail.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2019 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2020 Damien Baty <damien.baty@polyconseil.fr>
# Copyright (c) 2020 Bryce Guinta <bryce.guinta@protonmail.com>
# Copyright (c) 2020 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Generic Setup script, takes package info from __pkginfo__.py file.
"""
import os
import sys
from distutils.command.build_py import build_py
from os.path import exists, isdir, join

__docformat__ = "restructuredtext en"


try:
    from setuptools import setup
    from setuptools.command import easy_install as easy_install_lib
    from setuptools.command import install_lib  # pylint: disable=unused-import

    USE_SETUPTOOLS = 1
except ImportError:
    from distutils.command import install_lib  # pylint: disable=unused-import
    from distutils.core import setup

    USE_SETUPTOOLS = 0
    easy_install_lib = None


base_dir = os.path.dirname(__file__)

__pkginfo__ = {}
with open(os.path.join(base_dir, "pylint", "__pkginfo__.py")) as pkginfo_fp:
    exec(pkginfo_fp.read(), __pkginfo__)
scripts = __pkginfo__.get("scripts", [])
data_files = __pkginfo__.get("data_files", None)
ext_modules = __pkginfo__.get("ext_modules", None)
install_requires = __pkginfo__.get("install_requires", None)
dependency_links = __pkginfo__.get("dependency_links", [])
extras_require = __pkginfo__.get("extras_require", {})
project_urls = __pkginfo__.get("project_urls", {})

readme_path = join(base_dir, "README.rst")
if exists(readme_path):
    with open(readme_path, encoding="UTF-8") as stream:
        long_description = stream.read()
else:
    long_description = ""


needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []


def ensure_scripts(linux_scripts):
    """Creates the proper script names required for each platform
    (taken from 4Suite)
    """
    from distutils import util

    if util.get_platform()[:3] == "win":
        return linux_scripts + [script + ".bat" for script in linux_scripts]
    return linux_scripts


def get_packages(directory, prefix):
    """return a list of subpackages for the given directory"""
    result = []
    for package in os.listdir(directory):
        absfile = join(directory, package)
        if isdir(absfile):
            if exists(join(absfile, "__init__.py")):
                if prefix:
                    result.append("%s.%s" % (prefix, package))
                else:
                    result.append(package)
                result += get_packages(absfile, result[-1])
    return result


def _filter_tests(files):
    testdir = join("pylint", "test")
    return [f for f in files if testdir not in f]


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
        if "--force-manifest" in sys.argv:
            sys.argv.remove("--force-manifest")
    packages = ["pylint"] + get_packages(join(base_dir, "pylint"), "pylint")
    if USE_SETUPTOOLS:
        if install_requires:
            kwargs["install_requires"] = install_requires
            kwargs["dependency_links"] = dependency_links
        kwargs["entry_points"] = {
            "console_scripts": [
                "pylint = pylint:run_pylint",
                "epylint = pylint:run_epylint",
                "pyreverse = pylint:run_pyreverse",
                "symilar = pylint:run_symilar",
            ]
        }
    kwargs["packages"] = packages
    cmdclass = {"build_py": build_py}
    if easy_install_lib:
        cmdclass["easy_install"] = easy_install
    return setup(
        name="pylint",
        version=__pkginfo__["version"],
        license=__pkginfo__["license"],
        description=__pkginfo__["description"],
        long_description=long_description,
        author=__pkginfo__["author"],
        author_email=__pkginfo__["author_email"],
        url=__pkginfo__["web"],
        scripts=ensure_scripts(scripts),
        classifiers=__pkginfo__["classifiers"],
        data_files=data_files,
        ext_modules=ext_modules,
        cmdclass=cmdclass,
        extras_require=extras_require,
        test_suite="test",
        python_requires="~=3.5",
        setup_requires=pytest_runner,
        tests_require=["pytest", "pytest-benchmark"],
        project_urls=project_urls,
        **kwargs
    )


if __name__ == "__main__":
    install()
