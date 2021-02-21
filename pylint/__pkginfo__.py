# Copyright (c) 2006-2015 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2010 Julien Jehannet <julien.jehannet@logilab.fr>
# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2014-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Brett Cannon <brett@python.org>
# Copyright (c) 2014 Ricardo Gemignani <ricardo.gemignani@gmail.com>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Moises Lopez <moylop260@vauxoo.com>
# Copyright (c) 2016 Florian Bruhin <git@the-compiler.org>
# Copyright (c) 2016 Jakub Wilk <jwilk@jwilk.net>
# Copyright (c) 2017-2018 Hugo <hugovk@users.noreply.github.com>
# Copyright (c) 2018-2020 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2019-2020 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2019 Dan Hemberger <846186+hemberger@users.noreply.github.com>
# Copyright (c) 2019 jab <jab@users.noreply.github.com>
# Copyright (c) 2020-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Damien Baty <damien.baty@polyconseil.fr>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

# pylint: disable=redefined-builtin,invalid-name
"""pylint packaging information"""


from os.path import join

# For an official release, use dev_version = None
numversion = (2, 7, 0)
dev_version = None

version = ".".join(str(num) for num in numversion)
if dev_version is not None:
    version += "-dev" + str(dev_version)

install_requires = [
    "astroid==2.5.0",
    "isort>=4.2.5,<6",
    "mccabe>=0.6,<0.7",
    "toml>=0.7.1",
]

dependency_links = []  # type: ignore

extras_require = {}
extras_require[':sys_platform=="win32"'] = ["colorama"]
extras_require["docs"] = ["sphinx~=3.2", "python-docs-theme"]

license = "GPL"
description = "python code static checker"
web = "https://github.com/PyCQA/pylint"
mailinglist = "mailto:code-quality@python.org"
project_urls = {"What's New": "https://pylint.pycqa.org/en/latest/whatsnew/"}
author = "Python Code Quality Authority"
author_email = "code-quality@python.org"

classifiers = [
    "Development Status :: 6 - Mature",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Debuggers",
    "Topic :: Software Development :: Quality Assurance",
    "Topic :: Software Development :: Testing",
]

scripts = [
    join("bin", filename) for filename in ("pylint", "symilar", "epylint", "pyreverse")
]
