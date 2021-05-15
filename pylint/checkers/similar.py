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

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

# pylint: disable=redefined-builtin
"""a similarities / code duplication command line tool and pylint checker
"""
import copy
import functools
from os import posix_fadvise
import re
import sys
from collections import defaultdict
from getopt import getopt
from itertools import groupby
from pathlib import Path
import itertools
import operator
from typing import Dict, Iterable, Any, Tuple, FrozenSet, List, NamedTuple, NewType

import astroid  # type: ignore

from pylint.checkers import BaseChecker, MapReduceMixin, table_lines_from_stats
from pylint.interfaces import IRawChecker
from pylint.reporters.ureports.nodes import Table
from pylint.utils import decoding_stream

REGEX_FOR_LINES_WITH_CONTENT = re.compile(r".*\w+")

Index = NewType('Index', int)
LineNumber = NewType('LineNumber', int)

LineSpecifs = NamedTuple("LineSpecifs", (('text', str), ('linenumber', int), ('linetype', Optional[str])))

class LinesChunk:
    """
    The LinesChunk object computes and stores the hash of some consecutive stripped lines of a lineset.
    """
    __slots__ = (
        '_fileid',  # The name of the file from which the LinesChunk object is generated
        '_index',  # The index in the stripped lines that is the starting of consecutive lines
        '_hash'  # The hash of some consecutive lines
        )

    def __init__(self, fileid: str, num_line: int, *lines: Iterable[str]):
        self._fileid : str  = fileid
        self._index : Index = Index(num_line)
        self._hash : int = sum(hash(x) for x in lines)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, LinesChunk):
            return NotImplemented
        return self._hash == o._hash

    def __hash__(self) -> int:
        return self._hash

    def __repr__(self) -> str:
        return f"<LinesChunk object for file {self._fileid} ({self._index}, {self._hash})>"

    def __str__(self) -> str:
        return (f"LinesChunk object for file {self._fileid}, starting at line {self._index} \n"
                f"Hash is {self._hash}")

# Couple of line numbers
class SuccessiveLinesLimits:
    """
    A class to handle the numbering of begin and end of successive lines.
    
    :note: Only the end line number can be updated.
    """
    def __init__(self, start: LineNumber, end: LineNumber):
        self._start: LineNumber = start
        self._end: LineNumber = end

    @property
    def start(self) -> LineNumber:
        return self._start

    @property
    def end(self) -> LineNumber:
        return self._end

    @end.setter
    def end(self, value: LineNumber):
        self._end = value

    def __repr__(self) -> str:
        return f"<SuccessiveLinesLimits <{self._start};{self._end}>>"

# Links LinesChunk object to the starting indices (in lineset's stripped lines)
# of the different chunk of lines that are used to compute the hash
HashToIndex_T = Dict[LinesChunk, List[Index]]

# Links index in the lineset's stripped lines to the real lines in the file
IndexToLines_T = Dict[Index, SuccessiveLinesLimits]  

class LineSetStartCouple:
    """
    Indices in both linesets that mark the beginning of successive lines
    """
    def __init__(self, fst_lineset_index: Index, snd_lineset_index: Index):
        self._fst_lineset_index = fst_lineset_index
        self._snd_lineset_index = snd_lineset_index

    def __repr__(self) -> str:
        return f"<LineSetStartCouple <{self._fst_lineset_index};{self._snd_lineset_index}>>"

    def __add__(self, value: Index):
        return LineSetStartCouple(Index(self._fst_lineset_index + value), Index(self._snd_lineset_index + value))

    def __eq__(self, other) -> bool:
        if not isinstance(other, LineSetStartCouple):
            raise NotImplemented
        return self._fst_lineset_index == other._fst_lineset_index and self._snd_lineset_index == other._snd_lineset_index

    def __hash__(self) -> int:
        return hash(self._fst_lineset_index) + hash(self._snd_lineset_index)

    @property
    def fst_lineset_index(self) -> Index:
        return self._fst_lineset_index

    @property
    def snd_lineset_index(self) -> Index:
        return self._snd_lineset_index
        

# Couples of SuccesiveLinesLimits, one for first file, another for the second file 
CplSuccessiveLinesLimits = NamedTuple("CplSuccessiveLinesLimits", (("first_file", SuccessiveLinesLimits), ("second_file", SuccessiveLinesLimits)))

# Links the indices ot the starting line in both lineset's stripped lines to 
# the start and end lines in both files
CplIndexToCplLines_T = Dict[LineSetStartCouple, CplSuccessiveLinesLimits] 


def from_file_to_dict(lineset, min_common_lines: int =4) -> Tuple[HashToIndex_T, IndexToLines_T]:
    """
    Return two dicts. The first links the hash of successive stripped lines of a lineset
    to the indices of the starting lines.
    The second dict, links the index of the starting line in the linset's stripped lines to the 
    couple [start, end] lines number in the corresponding file.

    :param lineset: lineset object (i.e the lines in a file)
    :param min_common_lines: number of successive lines that are used to compute the hash
    :return: a dict linking hashes to corresponding start index and a dict that links this
             index to the start and end lines in the file
    """
    hash2index = defaultdict(list)
    index2lines = dict()
    # Comments, docstring and other specific patterns maybe excluded -> call to _stripped_lines
    # to get only what is desired
    lines = list((x.text, x.linetype) for x in lineset._stripped_lines)
    # Need different iterators on same lines but each one is shifted 1 from the precedent
    shifted_lines = [iter(lines[i:]) for i in range(min_common_lines)]

    for index_i, *succ_lines in enumerate(zip(*shifted_lines)):
        start_linenumber = lineset._stripped_lines[index_i][1]
        try:
            end_linenumber = lineset._stripped_lines[index_i + min_common_lines][1]
        except IndexError:
            end_linenumber = lineset._stripped_lines[-1][1] + 1

        index = Index(index_i)
        index2lines[index] = SuccessiveLinesLimits(LineNumber(start_linenumber), LineNumber(end_linenumber))

        # print(f"{index_i}::{start_linenumber}->{end_linenumber} : {succ_lines}", file=sys.stderr)
        successive_lines = tuple(*succ_lines)
        l_c = LinesChunk(lineset.name, index, *successive_lines)
        hash2index[l_c].append(index)

    return hash2index, index2lines


def remove_successives(all_couples: CplIndexToCplLines_T) -> None:
    """
    Removes all successive entries in the dictionary in argument 

    For example consider the following dict:

    >>> all_couples = {
        (11, 34): ([5, 9], [27, 31]),
        (23, 79): ([15, 19], [45, 49]),
        (12, 35): ([6, 10], [28, 32])
        }
    
    There are two successives keys (11, 34) and (12, 35).
    It means there are two consecutive similar chunks of lines in both files.
    Thus remove last entry and update the last line number in the first entry
    """
    all_couples_keys : List[LineSetStartCouple] = list(all_couples.keys())
    for couple in all_couples_keys:
        to_remove = []
        test = couple + Index(1)
        while test in all_couples:
            all_couples[couple].first_file.end = all_couples[test].first_file.end
            all_couples[couple].second_file.end = all_couples[test].second_file.end
            to_remove.append(test)
            test += 1 

        for target in to_remove:
            try:
                all_couples.pop(target)
            except KeyError:
                pass


class Similar:
    """finds copy-pasted lines of code in a project"""

    def __init__(
        self,
        min_lines=4,
        ignore_comments=False,
        ignore_docstrings=False,
        ignore_imports=False,
    ):
        self.min_lines = min_lines
        self.ignore_comments = ignore_comments
        self.ignore_docstrings = ignore_docstrings
        self.ignore_imports = ignore_imports
        self.linesets = []

    def append_stream(self, streamid, stream, encoding=None):
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
                )
            )
        except UnicodeDecodeError:
            pass

    def run(self):
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

    def _display_sims(self, sims):
        """display computed similarities on stdout"""
        nb_lignes_dupliquees = 0
        for num, couples in sims:
            print()
            print(num, "similar lines in", len(couples), "files")
            couples = sorted(couples)
            lineset = idx = None
            for lineset, idx in couples:
                print(f"=={lineset.name}:{idx}")
            if lineset:
                for line in lineset._real_lines[idx : idx + num]:
                    print("  ", line.rstrip())
            nb_lignes_dupliquees += num * (len(couples) - 1)
        nb_total_lignes = sum([len(lineset) for lineset in self.linesets])
        print(
            "TOTAL lines=%s duplicates=%s percent=%.2f"
            % (
                nb_total_lignes,
                nb_lignes_dupliquees,
                nb_lignes_dupliquees * 100.0 / nb_total_lignes,
            )
        )

    def _find_common(self, lineset1, lineset2):
        """find similarities in the two given linesets"""
        min_common = 4
        hash_to_index_1, index_to_lines_1 = from_file_to_dict(lineset1, min_common)
        hash_to_index_2, index_to_lines_2 = from_file_to_dict(lineset2, min_common)

        hash_1 : FrozenSet[LinesChunk] = set(hash_to_index_1.keys())
        hash_2 : FrozenSet[LinesChunk] = set(hash_to_index_2.keys())

        common_hashes : Iterable[LinesChunk] = sorted(list(hash_1 & hash_2), key=lambda m: hash_to_index_1[m][0])

        # all_couples is a dict that links the couple of indices in both linesets that mark the beginning of 
        # successive common lines, to the corresponding starting and ending number lines in both files
        all_couples : CplIndexToCplLines_T = {}

        for c_hash in sorted(common_hashes, key=operator.attrgetter('_index')):
            for indices_in_linesets in itertools.product(hash_to_index_1[c_hash], hash_to_index_2[c_hash]):
                index_1 = indices_in_linesets[0]
                index_2 = indices_in_linesets[1]
                all_couples[LineSetStartCouple(index_1, index_2)] = CplSuccessiveLinesLimits(copy.copy(index_to_lines_1[index_1]), copy.copy(index_to_lines_2[index_2]))

        remove_successives(all_couples)
        for common_lines in all_couples.values():
            file_1_lines = common_lines.first_file
            file_2_lines = common_lines.second_file
            start_line_1, end_line_1 = file_1_lines.start, file_1_lines.end
            start_line_2, end_line_2 = file_2_lines.start, file_2_lines.end

            nb_common_lines_1 = end_line_1 - start_line_1
            nb_common_lines_2 = end_line_2 - start_line_2
            # assert(nb_common_lines_1 == nb_common_lines_2)

            if check_sim(lineset1, start_line_1, lineset2, start_line_2, nb_common_lines_1, min_common):
                yield nb_common_lines_1, lineset1, start_line_1, lineset2, start_line_2

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


def stripped_lines(lines: Iterable[str], ignore_comments: bool, ignore_docstrings: bool, ignore_imports: bool) -> List[LineSpecifs]:
    """
    Return tuples of line/line number/line type with leading/trailing whitespace and any ignored code features removed

    :param lines: a collection of lines
    :param ignore_comments: if true, any comment in the lines collection is removed from the result
    :param ignore_docstrings: if true, any line that is a docstring is removed from the result
    :param ignore_imports: if true, any line that is an import is removed from the result
    """
    if ignore_imports:
        tree = astroid.parse("".join(lines))
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

    strippedlines = []
    docstring = None
    for lineno, line in enumerate(lines, start=1):
        line = line.strip()
        ltype = None
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
                ltype = 'doc'
        if ignore_imports:
            current_line_is_import = line_begins_import.get(
                lineno, current_line_is_import
            )
            if current_line_is_import:
                line = ""
                ltype = 'import'
        if ignore_comments:
            line = line.split("#", 1)[0].strip()
        strippedlines.append(LineSpecifs(line, lineno - 1, ltype))
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
    ):
        self.name = name
        self._real_lines = lines
        self._stripped_lines = stripped_lines(
            lines, ignore_comments, ignore_docstrings, ignore_imports
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
[-i|--ignore-comments] [--ignore-docstrings] [--ignore-imports] file1..."
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
    )
    min_lines = 4
    ignore_comments = False
    ignore_docstrings = False
    ignore_imports = False
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
    if not args:
        usage(1)
    sim = Similar(min_lines, ignore_comments, ignore_docstrings, ignore_imports)
    for filename in args:
        with open(filename) as stream:
            sim.append_stream(filename, stream)
    sim.run()
    sys.exit(0)


def check_sim(ls_1: LineSet, stline_1: int, ls_2: LineSet, stline_2: int, nb_lines: int, min_lines_nb: int):
    check_cmn_lines_nb = 0
    for idx in range(nb_lines):
        line_1 = ls_1._real_lines[stline_1 + idx]
        line_2 = ls_2._real_lines[stline_2 + idx]
        if (REGEX_FOR_LINES_WITH_CONTENT.match(line_1) and
            REGEX_FOR_LINES_WITH_CONTENT.match(line_2) and
            line_1 == line_2): 
                check_cmn_lines_nb += 1
    if check_cmn_lines_nb > min_lines_nb:
        return True
    return False


if __name__ == "__main__":
    Run()
