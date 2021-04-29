# Copyright (c) 2006-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2013 buck@yelp.com <buck@yelp.com>
# Copyright (c) 2014-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Brett Cannon <brett@python.org>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Moises Lopez <moylop260@vauxoo.com>
# Copyright (c) 2017-2018 Bryce Guinta <bryce.paul.guinta@gmail.com>
# Copyright (c) 2018-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
# Copyright (c) 2019 Bruno P. Kinoshita <kinow@users.noreply.github.com>
# Copyright (c) 2020-2021 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Frank Harrison <frank@doublethefish.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Matus Valo <matusvalo@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

"""utilities methods and classes for checkers

Base id of standard checkers (used in msg and report ids):
01: base
02: classes
03: format
04: import
05: misc
06: variables
07: exceptions
08: similar
09: design_analysis
10: newstyle
11: typecheck
12: logging
13: string_format
14: string_constant
15: stdlib
16: python3
17: refactoring
18-50: not yet used: reserved for future internal checkers.
51-99: perhaps used: reserved for external checkers

The raw_metrics checker has no number associated since it doesn't emit any
messages nor reports. XXX not true, emit a 07 report !

"""

from pylint.checkers.base_checker import BaseChecker, BaseTokenChecker
from pylint.checkers.deprecated import DeprecatedMixin
from pylint.checkers.mapreduce_checker import MapReduceMixin
from pylint.utils import diff_string, register_plugins


def table_lines_from_stats(stats, old_stats, columns):
    """get values listed in <columns> from <stats> and <old_stats>,
    and return a formated list of values, designed to be given to a
    ureport.Table object
    """
    lines = []
    for m_type in columns:
        new = stats[m_type]
        old = old_stats.get(m_type)
        if old is not None:
            diff_str = diff_string(old, new)
        else:
            old, diff_str = "NC", "NC"
        new = "%.3f" % new if isinstance(new, float) else str(new)
        old = "%.3f" % old if isinstance(old, float) else str(old)
        lines += (m_type.replace("_", " "), new, old, diff_str)
    return lines


def initialize(linter):
    """initialize linter with checkers in this package"""
    register_plugins(linter, __path__[0])


__all__ = [
    "BaseChecker",
    "BaseTokenChecker",
    "initialize",
    "MapReduceMixin",
    "DeprecatedMixin",
    "register_plugins",
]
