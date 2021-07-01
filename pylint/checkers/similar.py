# Copyright (c) 2006, 2008-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2012 Ry4an Brase <ry4an-hg@ry4an.org>
# Copyright (c) 2012 Google, Inc.
# Copyright (c) 2012 Anthony VEREZ <anthony.verez.external@cassidian.com>
# Copyright (c) 2014-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Brett Cannon <brett@python.org>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2017, 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2017 Mikhail Fesenko <proggga@gmail.com>
# Copyright (c) 2018 Scott Worley <scottworley@scottworley.com>
# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
# Copyright (c) 2019, 2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2019 Taewon D. Kim <kimt33@mcmaster.ca>
# Copyright (c) 2020 Frank Harrison <frank@doublethefish.com>
# Copyright (c) 2020 Eli Fine <ejfine@gmail.com>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Shiv Venkatasubrahmanyam <shvenkat@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 bot <bot@noreply.github.com>
# Copyright (c) 2021 Aditya Gupta <adityagupta1089@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

# pylint: disable=redefined-builtin
"""a similarities / code duplication command line tool and pylint checker
"""
import functools
import re
import sys
from collections import defaultdict
from getopt import getopt
from io import TextIOWrapper
from itertools import chain, groupby
from typing import List, Tuple

import astroid

from pylint.checkers import BaseChecker, MapReduceMixin, table_lines_from_stats
from pylint.interfaces import IRawChecker
from pylint.reporters.ureports.nodes import Table
from pylint.utils import decoding_stream

REGEX_FOR_LINES_WITH_CONTENT = re.compile(r".*\w+")


class Similar:
    """finds copy-pasted lines of code in a project"""

    def __init__(
        self,
        min_lines: int = 4,
        ignore_comments: bool = False,
        ignore_docstrings: bool = False,
        ignore_imports: bool = False,
        ignore_signatures: bool = False,
    ) -> None:
        self.min_lines = min_lines
        self.ignore_comments = ignore_comments
        self.ignore_docstrings = ignore_docstrings
        self.ignore_imports = ignore_imports
        self.ignore_signatures = ignore_signatures
        self.linesets: List["LineSet"] = []

    def append_stream(
        self, streamid: str, stream: TextIOWrapper, encoding=None
    ) -> None:
        """append a file to search for similarities"""
        if encoding is None:
            readlines = stream.readlines
        else:
            readlines = decoding_stream(stream, encoding).readlines
        try:
            self.linesets.append(
                LineSet(
                    streamid,
                    readlines(),
                    self.ignore_comments,
                    self.ignore_docstrings,
                    self.ignore_imports,
                    self.ignore_signatures,
                )
            )
        except UnicodeDecodeError:
            pass

    def run(self) -> None:
        """start looking for similarities and display results on stdout"""
        self._display_sims(self._compute_sims())

    def _compute_sims(self):
        """compute similarities in appended files"""
        no_duplicates = defaultdict(list)
        for num, lineset1, idx1, lineset2, idx2 in self._iter_sims():
            duplicate = no_duplicates[num]
            for couples in duplicate:
                if (lineset1, idx1) in couples or (lineset2, idx2) in couples:
                    couples.add((lineset1, idx1))
                    couples.add((lineset2, idx2))
                    break
            else:
                duplicate.append({(lineset1, idx1), (lineset2, idx2)})
        sims = []
        for num, ensembles in no_duplicates.items():
            for couples in ensembles:
                sims.append((num, couples))
        sims.sort()
        sims.reverse()
        return sims

    def _display_sims(self, similarities: List[Tuple]) -> None:
        """Display computed similarities on stdout"""
        report = self._get_similarity_report(similarities)
        print(report)

    def _get_similarity_report(self, similarities: List[Tuple]) -> str:
        """Create a report from similarities"""
        report: str = ""
        duplicated_line_number: int = 0
        for number, files in similarities:
            report += f"\n{number} similar lines in {len(files)} files\n"
            files = sorted(files)
            line_set = idx = None
            for line_set, idx in files:
                report += f"=={line_set.name}:{idx}\n"
            if line_set:
                for line in line_set._real_lines[idx : idx + number]:
                    report += f"   {line.rstrip()}\n" if line.rstrip() else "\n"
            duplicated_line_number += number * (len(files) - 1)
        total_line_number: int = sum(len(lineset) for lineset in self.linesets)
        report += "TOTAL lines={} duplicates={} percent={:.2f}\n".format(
            total_line_number,
            duplicated_line_number,
            duplicated_line_number * 100.0 / total_line_number,
        )
        return report

    def _find_common(self, lineset1, lineset2):
        """find similarities in the two given linesets"""
        lines1 = lineset1.enumerate_stripped
        lines2 = lineset2.enumerate_stripped
        find = lineset2.find
        index1 = 0
        min_lines = self.min_lines
        while index1 < len(lineset1):
            skip = 1
            num = 0
            for index2 in find(lineset1[index1]):
                num_lines_with_content = 0
                for num, ((_, line1), (_, line2)) in enumerate(
                    zip(lines1(index1), lines2(index2))
                ):
                    if line1 != line2:
                        if num_lines_with_content > min_lines:
                            yield num, lineset1, index1, lineset2, index2
                        skip = max(skip, num)
                        break
                    if re.match(REGEX_FOR_LINES_WITH_CONTENT, line1):
                        num_lines_with_content += 1
                else:
                    # we may have reached the end
                    num += 1
                    if num_lines_with_content > min_lines:
                        yield num, lineset1, index1, lineset2, index2
                    skip = max(skip, num)
            index1 += skip

    def _iter_sims(self):
        """iterate on similarities among all files, by making a cartesian
        product
        """
        for idx, lineset in enumerate(self.linesets[:-1]):
            for lineset2 in self.linesets[idx + 1 :]:
                yield from self._find_common(lineset, lineset2)

    def get_map_data(self):
        """Returns the data we can use for a map/reduce process

        In this case we are returning this instance's Linesets, that is all file
        information that will later be used for vectorisation.
        """
        return self.linesets

    def combine_mapreduce_data(self, linesets_collection):
        """Reduces and recombines data into a format that we can report on

        The partner function of get_map_data()"""
        self.linesets = [line for lineset in linesets_collection for line in lineset]


def stripped_lines(
    lines,
    ignore_comments: bool,
    ignore_docstrings: bool,
    ignore_imports: bool,
    ignore_signatures: bool,
):
    """return lines with leading/trailing whitespace and any ignored code
    features removed
    """
    if ignore_imports or ignore_signatures:
        tree = astroid.parse("".join(lines))
    if ignore_imports:
        node_is_import_by_lineno = (
            (node.lineno, isinstance(node, (astroid.Import, astroid.ImportFrom)))
            for node in tree.body
        )
        line_begins_import = {
            lineno: all(is_import for _, is_import in node_is_import_group)
            for lineno, node_is_import_group in groupby(
                node_is_import_by_lineno, key=lambda x: x[0]
            )
        }
        current_line_is_import = False
    if ignore_signatures:
        functions = [
            n
            for n in tree.body
            if isinstance(n, (astroid.FunctionDef, astroid.AsyncFunctionDef))
        ]
        signature_lines = set(
            chain(
                *(
                    range(func.fromlineno, func.body[0].lineno)
                    for func in functions
                    if func.body
                )
            )
        )

    strippedlines = []
    docstring = None
    for lineno, line in enumerate(lines, start=1):
        line = line.strip()
        if ignore_docstrings:
            if not docstring:
                if line.startswith('"""') or line.startswith("'''"):
                    docstring = line[:3]
                    line = line[3:]
                elif line.startswith('r"""') or line.startswith("r'''"):
                    docstring = line[1:4]
                    line = line[4:]
            if docstring:
                if line.endswith(docstring):
                    docstring = None
                line = ""
        if ignore_imports:
            current_line_is_import = line_begins_import.get(
                lineno, current_line_is_import
            )
            if current_line_is_import:
                line = ""
        if ignore_comments:
            line = line.split("#", 1)[0].strip()
        if ignore_signatures and lineno in signature_lines:
            line = ""
        strippedlines.append(line)
    return strippedlines


@functools.total_ordering
class LineSet:
    """Holds and indexes all the lines of a single source file"""

    def __init__(
        self,
        name,
        lines,
        ignore_comments=False,
        ignore_docstrings=False,
        ignore_imports=False,
        ignore_signatures=False,
    ):
        self.name = name
        self._real_lines = lines
        self._stripped_lines = stripped_lines(
            lines, ignore_comments, ignore_docstrings, ignore_imports, ignore_signatures
        )
        self._index = self._mk_index()

    def __str__(self):
        return "<Lineset for %s>" % self.name

    def __len__(self):
        return len(self._real_lines)

    def __getitem__(self, index):
        return self._stripped_lines[index]

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if not isinstance(other, LineSet):
            return False
        return self.__dict__ == other.__dict__

    def enumerate_stripped(self, start_at=0):
        """return an iterator on stripped lines, starting from a given index
        if specified, else 0
        """
        idx = start_at
        if start_at:
            lines = self._stripped_lines[start_at:]
        else:
            lines = self._stripped_lines
        for line in lines:
            # if line:
            yield idx, line
            idx += 1

    def find(self, stripped_line):
        """return positions of the given stripped line in this set"""
        return self._index.get(stripped_line, ())

    def _mk_index(self):
        """create the index for this set"""
        index = defaultdict(list)
        for line_no, line in enumerate(self._stripped_lines):
            if line:
                index[line].append(line_no)
        return index


MSGS = {
    "R0801": (
        "Similar lines in %s files\n%s",
        "duplicate-code",
        "Indicates that a set of similar lines has been detected "
        "among multiple file. This usually means that the code should "
        "be refactored to avoid this duplication.",
    )
}


def report_similarities(sect, stats, old_stats):
    """make a layout with some stats about duplication"""
    lines = ["", "now", "previous", "difference"]
    lines += table_lines_from_stats(
        stats, old_stats, ("nb_duplicated_lines", "percent_duplicated_lines")
    )
    sect.append(Table(children=lines, cols=4, rheaders=1, cheaders=1))


# wrapper to get a pylint checker from the similar class
class SimilarChecker(BaseChecker, Similar, MapReduceMixin):
    """checks for similarities and duplicated code. This computation may be
    memory / CPU intensive, so you should disable it if you experiment some
    problems.
    """

    __implements__ = (IRawChecker,)
    # configuration section name
    name = "similarities"
    # messages
    msgs = MSGS
    # configuration options
    # for available dict keys/values see the optik parser 'add_option' method
    options = (
        (
            "min-similarity-lines",  # type: ignore
            {
                "default": 4,
                "type": "int",
                "metavar": "<int>",
                "help": "Minimum lines number of a similarity.",
            },
        ),
        (
            "ignore-comments",
            {
                "default": True,
                "type": "yn",
                "metavar": "<y or n>",
                "help": "Ignore comments when computing similarities.",
            },
        ),
        (
            "ignore-docstrings",
            {
                "default": True,
                "type": "yn",
                "metavar": "<y or n>",
                "help": "Ignore docstrings when computing similarities.",
            },
        ),
        (
            "ignore-imports",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y or n>",
                "help": "Ignore imports when computing similarities.",
            },
        ),
        (
            "ignore-signatures",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y or n>",
                "help": "Ignore function signatures when computing similarities.",
            },
        ),
    )
    # reports
    reports = (("RP0801", "Duplication", report_similarities),)  # type: ignore

    def __init__(self, linter=None):
        BaseChecker.__init__(self, linter)
        Similar.__init__(
            self, min_lines=4, ignore_comments=True, ignore_docstrings=True
        )
        self.stats = None

    def set_option(self, optname, value, action=None, optdict=None):
        """method called to set an option (registered in the options list)

        Overridden to report options setting to Similar
        """
        BaseChecker.set_option(self, optname, value, action, optdict)
        if optname == "min-similarity-lines":
            self.min_lines = self.config.min_similarity_lines
        elif optname == "ignore-comments":
            self.ignore_comments = self.config.ignore_comments
        elif optname == "ignore-docstrings":
            self.ignore_docstrings = self.config.ignore_docstrings
        elif optname == "ignore-imports":
            self.ignore_imports = self.config.ignore_imports
        elif optname == "ignore-signatures":
            self.ignore_signatures = self.config.ignore_signatures

    def open(self):
        """init the checkers: reset linesets and statistics information"""
        self.linesets = []
        self.stats = self.linter.add_stats(
            nb_duplicated_lines=0, percent_duplicated_lines=0
        )

    def process_module(self, node):
        """process a module

        the module's content is accessible via the stream object

        stream must implement the readlines method
        """
        with node.stream() as stream:
            self.append_stream(self.linter.current_name, stream, node.file_encoding)

    def close(self):
        """compute and display similarities on closing (i.e. end of parsing)"""
        total = sum(len(lineset) for lineset in self.linesets)
        duplicated = 0
        stats = self.stats
        for num, couples in self._compute_sims():
            msg = []
            lineset = idx = None
            for lineset, idx in couples:
                msg.append(f"=={lineset.name}:{idx}")
            msg.sort()

            if lineset:
                for line in lineset._real_lines[idx : idx + num]:
                    msg.append(line.rstrip())

            self.add_message("R0801", args=(len(couples), "\n".join(msg)))
            duplicated += num * (len(couples) - 1)
        stats["nb_duplicated_lines"] = duplicated
        stats["percent_duplicated_lines"] = total and duplicated * 100.0 / total

    def get_map_data(self):
        """Passthru override"""
        return Similar.get_map_data(self)

    @classmethod
    def reduce_map_data(cls, linter, data):
        """Reduces and recombines data into a format that we can report on

        The partner function of get_map_data()"""
        recombined = SimilarChecker(linter)
        recombined.open()
        Similar.combine_mapreduce_data(recombined, linesets_collection=data)
        recombined.close()


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(SimilarChecker(linter))


def usage(status=0):
    """display command line usage information"""
    print("finds copy pasted blocks in a set of files")
    print()
    print(
        "Usage: symilar [-d|--duplicates min_duplicated_lines] \
[-i|--ignore-comments] [--ignore-docstrings] [--ignore-imports] [--ignore-signatures] file1..."
    )
    sys.exit(status)


def Run(argv=None):
    """standalone command line access point"""
    if argv is None:
        argv = sys.argv[1:]

    s_opts = "hdi"
    l_opts = (
        "help",
        "duplicates=",
        "ignore-comments",
        "ignore-imports",
        "ignore-docstrings",
        "ignore-signatures",
    )
    min_lines = 4
    ignore_comments = False
    ignore_docstrings = False
    ignore_imports = False
    ignore_signatures = False
    opts, args = getopt(argv, s_opts, l_opts)
    for opt, val in opts:
        if opt in ("-d", "--duplicates"):
            min_lines = int(val)
        elif opt in ("-h", "--help"):
            usage()
        elif opt in ("-i", "--ignore-comments"):
            ignore_comments = True
        elif opt in ("--ignore-docstrings",):
            ignore_docstrings = True
        elif opt in ("--ignore-imports",):
            ignore_imports = True
        elif opt in ("--ignore-signatures",):
            ignore_signatures = True
    if not args:
        usage(1)
    sim = Similar(
        min_lines, ignore_comments, ignore_docstrings, ignore_imports, ignore_signatures
    )
    for filename in args:
        with open(filename) as stream:
            sim.append_stream(filename, stream)
    sim.run()
    sys.exit(0)


if __name__ == "__main__":
    Run()
