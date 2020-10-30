# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2012 FELD Boris <lothiraldan@gmail.com>
# Copyright (c) 2013-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2013 buck@yelp.com <buck@yelp.com>
# Copyright (c) 2014 LCD 47 <lcd047@gmail.com>
# Copyright (c) 2014 Brett Cannon <brett@python.org>
# Copyright (c) 2014 Ricardo Gemignani <ricardo.gemignani@gmail.com>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Pavel Roskin <proski@gnu.org>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2016 Roy Williams <roy.williams.iii@gmail.com>
# Copyright (c) 2016 xmo-odoo <xmo-odoo@users.noreply.github.com>
# Copyright (c) 2017 Bryce Guinta <bryce.paul.guinta@gmail.com>
# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2019 Mr. Senko <atodorov@mrsenko.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2019 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2020 谭九鼎 <109224573@qq.com>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2020 Guillaume Peillex <guillaume.peillex@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Functional/non regression tests for pylint"""

__all__ = [
    "_get_tests_info",
    "_tokenize_str",
    "CheckerTestCase",
    "FunctionalTestFile",
    "linter",
    "LintModuleTest",
    "Message",
    "MinimalTestReporter",
    "set_config",
    "TestReporter",
    "UPDATE_OPTION",
]

from pylint.testutils.test_reporter import MinimalTestReporter, TestReporter
from pylint.testutils.utils import (
    UPDATE_OPTION,
    CheckerTestCase,
    FunctionalTestFile,
    LintModuleTest,
    Message,
    _get_tests_info,
    _tokenize_str,
    linter,
    set_config,
)
