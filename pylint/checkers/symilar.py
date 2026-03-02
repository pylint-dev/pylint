# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""A similarities / code duplication command line tool and pylint checker.

The algorithm is based on comparing the hash value of n successive lines of a file.
First the files are read and any line that doesn't fulfill requirement are removed
(comments, docstrings...)

Those stripped lines are stored in the LineSet class which gives access to them.
Then each index of the stripped lines collection is associated with the hash of n
successive entries of the stripped lines starting at the current index (n is the
minimum common lines option).

The common hashes between both linesets are then looked for. If there are matches, then
the match indices in both linesets are stored and associated with the corresponding
couples (start line number/end line number) in both files.

This association is then post-processed to handle the case of successive matches. For
example if the minimum common lines setting is set to four, then the hashes are
computed with four lines. If one of match indices couple (12, 34) is the
successor of another one (11, 33) then it means that there are in fact five lines which
are common.

Once post-processed the values of association table are the result looked for, i.e.
start and end lines numbers of common lines in both files.
"""

from __future__ import annotations

import argparse
import copy
import functools
import itertools
import re
import sys
import warnings
from collections import defaultdict
from collections.abc import Callable, Generator, Iterable, Sequence
from io import BufferedIOBase, BufferedReader, BytesIO
from itertools import chain
from typing import TYPE_CHECKING, NamedTuple, NewType, NoReturn, TextIO, TypeAlias

import astroid
from astroid import nodes

from pylint.checkers import BaseChecker, BaseRawFileChecker, table_lines_from_stats
from pylint.reporters.ureports.nodes import Section, Table
from pylint.typing import MessageDefinitionTuple, Options
from pylint.utils import LinterStats, decoding_stream

if TYPE_CHECKING:
    from pylint.lint import PyLinter

DEFAULT_MIN_SIMILARITY_LINE = 4

REGEX_FOR_LINES_WITH_CONTENT = re.compile(r".*\w+")

# Index defines a location in a LineSet stripped lines collection
Index = NewType("Index", int)

# LineNumber defines a location in a LinesSet real lines collection (the whole file lines)
LineNumber = NewType("LineNumber", int)


# LineSpecifs holds characteristics of a line in a file
class LineSpecifs(NamedTuple):
    line_number: LineNumber
    text: str


# Maps the hash of successive stripped lines to the starting indices
# (in lineset's stripped lines) of the chunks that produced that hash.
HashToIndex_T = dict[int, list[Index]]

# Links index in the lineset's stripped lines to the real lines in the file
IndexToLines_T = dict[Index, "SuccessiveLinesLimits"]


class LineSetHashResult(NamedTuple):
    """Pre-computed hash data for a LineSet, used to speed up similarity lookups."""

    hash_to_index: HashToIndex_T
    index_to_lines: IndexToLines_T


# The types the streams read by pylint can take. Originating from astroid.nodes.Module.stream() and open()
STREAM_TYPES: TypeAlias = TextIO | BufferedReader | BytesIO


class CplSuccessiveLinesLimits:
    """Holds a SuccessiveLinesLimits object for each checked file and counts the number
    of common lines between both stripped lines collections extracted from both files.
    """

    __slots__ = ("effective_cmn_lines_nb", "first_file", "second_file")

    def __init__(
        self,
        first_file: SuccessiveLinesLimits,
        second_file: SuccessiveLinesLimits,
        effective_cmn_lines_nb: int,
    ) -> None:
        self.first_file = first_file
        self.second_file = second_file
        self.effective_cmn_lines_nb = effective_cmn_lines_nb


# Links the indices to the starting line in both lineset's stripped lines to
# the start and end lines in both files
CplIndexToCplLines_T = dict["LineSetStartCouple", CplSuccessiveLinesLimits]


class SuccessiveLinesLimits:
    """A class to handle the numbering of begin and end of successive lines.

    :note: Only the end line number can be updated.
    """

    __slots__ = ("_end", "_start")

    def __init__(self, start: LineNumber, end: LineNumber) -> None:
        self._start: LineNumber = start
        self._end: LineNumber = end

    @property
    def start(self) -> LineNumber:
        return self._start

    @property
    def end(self) -> LineNumber:
        return self._end

    @end.setter
    def end(self, value: LineNumber) -> None:
        self._end = value

    def __repr__(self) -> str:
        return f"<SuccessiveLinesLimits <{self._start};{self._end}>>"


class LineSetStartCouple(NamedTuple):
    """Indices in both linesets that mark the beginning of successive lines."""

    fst_lineset_index: Index
    snd_lineset_index: Index

    def __repr__(self) -> str:
        return (
            f"<LineSetStartCouple <{self.fst_lineset_index};{self.snd_lineset_index}>>"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LineSetStartCouple):
            return NotImplemented
        return (
            self.fst_lineset_index == other.fst_lineset_index
            and self.snd_lineset_index == other.snd_lineset_index
        )

    def __hash__(self) -> int:
        return hash(self.fst_lineset_index) + hash(self.snd_lineset_index)

    def increment(self, value: Index) -> LineSetStartCouple:
        return LineSetStartCouple(
            Index(self.fst_lineset_index + value),
            Index(self.snd_lineset_index + value),
        )


LinesChunkLimits_T = tuple["LineSet", LineNumber, LineNumber]


def hash_lineset(
    lineset: LineSet, min_common_lines: int = DEFAULT_MIN_SIMILARITY_LINE
) -> LineSetHashResult:
    """Return pre-computed hash data for a lineset.

    The result contains two dicts:
    - hash_to_index: maps the hash of successive stripped lines to the starting
      indices (in lineset's stripped lines) of the chunks that produced that hash.
    - index_to_lines: maps the index of the starting line in the lineset's stripped
      lines to the start and end line numbers in the corresponding file.

    :param lineset: lineset object (i.e the lines in a file)
    :param min_common_lines: number of successive lines that are used to compute the hash
    :return: a LineSetHashResult with hash-to-index and index-to-lines mappings
    """
    hash_to_index: HashToIndex_T = defaultdict(list)
    index_to_lines: IndexToLines_T = {}
    stripped = lineset.stripped_lines
    num_lines = len(stripped)
    if num_lines < min_common_lines:
        return LineSetHashResult(hash_to_index, index_to_lines)

    # Pre-compute per-line hashes for the rolling window
    line_hashes = [hash(spec.text) for spec in stripped]

    # Seed the rolling hash with the first window
    window_hash = sum(line_hashes[:min_common_lines])

    last_index = num_lines - 1
    for i in range(num_lines - min_common_lines + 1):
        start_linenumber = LineNumber(stripped[i].line_number)
        window_end = i + min_common_lines
        end_linenumber = (
            stripped[window_end].line_number
            if window_end <= last_index
            else LineNumber(stripped[last_index].line_number + 1)
        )

        index = Index(i)
        index_to_lines[index] = SuccessiveLinesLimits(
            start=start_linenumber, end=end_linenumber
        )

        hash_to_index[window_hash].append(index)

        # Slide the window: subtract the leaving line, add the entering line
        if window_end <= last_index:
            window_hash = window_hash - line_hashes[i] + line_hashes[window_end]

    return LineSetHashResult(hash_to_index, index_to_lines)


def remove_successive(all_couples: CplIndexToCplLines_T) -> None:
    """Removes all successive entries in the dictionary in argument.

    :param all_couples: collection that has to be cleaned up from successive entries.
                        The keys are couples of indices that mark the beginning of common entries
                        in both linesets. The values have two parts. The first one is the couple
                        of starting and ending line numbers of common successive lines in the first file.
                        The second part is the same for the second file.

    For example consider the following dict:

    >>> all_couples
    {(11, 34): ([5, 9], [27, 31]),
     (23, 79): ([15, 19], [45, 49]),
     (12, 35): ([6, 10], [28, 32])}

    There are two successive keys (11, 34) and (12, 35).
    It means there are two consecutive similar chunks of lines in both files.
    Thus remove last entry and update the last line numbers in the first entry

    >>> remove_successive(all_couples)
    >>> all_couples
    {(11, 34): ([5, 10], [27, 32]),
     (23, 79): ([15, 19], [45, 49])}
    """
    couple: LineSetStartCouple
    for couple in tuple(all_couples.keys()):
        to_remove = []
        test = couple.increment(Index(1))
        while test in all_couples:
            all_couples[couple].first_file.end = all_couples[test].first_file.end
            all_couples[couple].second_file.end = all_couples[test].second_file.end
            all_couples[couple].effective_cmn_lines_nb += 1
            to_remove.append(test)
            test = test.increment(Index(1))

        for target in to_remove:
            try:
                all_couples.pop(target)
            except KeyError:
                pass


def filter_noncode_lines(
    ls_1: LineSet,
    stindex_1: Index,
    ls_2: LineSet,
    stindex_2: Index,
    common_lines_nb: int,
) -> int:
    """Return the effective number of common lines between lineset1
    and lineset2 filtered from non code lines.

    That is to say the number of common successive stripped
    lines except those that do not contain code (for example
    a line with only an ending parenthesis)

    :param ls_1: first lineset
    :param stindex_1: first lineset starting index
    :param ls_2: second lineset
    :param stindex_2: second lineset starting index
    :param common_lines_nb: number of common successive stripped lines before being filtered from non code lines
    :return: the number of common successive stripped lines that contain code
    """
    stripped_l1 = [
        lspecif.text
        for lspecif in ls_1.stripped_lines[stindex_1 : stindex_1 + common_lines_nb]
        if REGEX_FOR_LINES_WITH_CONTENT.match(lspecif.text)
    ]
    stripped_l2 = [
        lspecif.text
        for lspecif in ls_2.stripped_lines[stindex_2 : stindex_2 + common_lines_nb]
        if REGEX_FOR_LINES_WITH_CONTENT.match(lspecif.text)
    ]
    return sum(sline_1 == sline_2 for sline_1, sline_2 in zip(stripped_l1, stripped_l2))


class Commonality(NamedTuple):
    cmn_lines_nb: int
    fst_lset: LineSet
    fst_file_start: LineNumber
    fst_file_end: LineNumber
    snd_lset: LineSet
    snd_file_start: LineNumber
    snd_file_end: LineNumber


class Symilar:
    """Finds copy-pasted lines of code in a project."""

    def __init__(
        self,
        min_lines: int = DEFAULT_MIN_SIMILARITY_LINE,
        ignore_comments: bool = False,
        ignore_docstrings: bool = False,
        ignore_imports: bool = False,
        ignore_signatures: bool = False,
    ) -> None:
        # If we run in pylint mode we link the namespace objects
        if isinstance(self, BaseChecker):
            self.namespace = self.linter.config
        else:
            self.namespace = argparse.Namespace()

        self.namespace.min_similarity_lines = min_lines
        self.namespace.ignore_comments = ignore_comments
        self.namespace.ignore_docstrings = ignore_docstrings
        self.namespace.ignore_imports = ignore_imports
        self.namespace.ignore_signatures = ignore_signatures
        self.linesets: list[LineSet] = []

    def append_stream(
        self, streamid: str, stream: STREAM_TYPES, encoding: str | None = None
    ) -> None:
        """Append a file to search for similarities."""
        if isinstance(stream, BufferedIOBase):
            if encoding is None:
                raise ValueError
            readlines = decoding_stream(stream, encoding).readlines
        else:
            # hint parameter is incorrectly typed as non-optional
            readlines = stream.readlines  # type: ignore[assignment]

        try:
            lines = readlines()
        except UnicodeDecodeError:
            lines = []

        self.linesets.append(
            LineSet(
                streamid,
                lines,
                self.namespace.ignore_comments,
                self.namespace.ignore_docstrings,
                self.namespace.ignore_imports,
                self.namespace.ignore_signatures,
                line_enabled_callback=(
                    self.linter._is_one_message_enabled
                    if hasattr(self, "linter")
                    else None
                ),
            )
        )

    def run(self) -> None:
        """Start looking for similarities and display results on stdout."""
        if self.namespace.min_similarity_lines == 0:
            return
        self._display_sims(self._compute_sims())

    def _compute_sims(self) -> list[tuple[int, set[LinesChunkLimits_T]]]:
        """Compute similarities in appended files."""
        no_duplicates: dict[int, list[set[LinesChunkLimits_T]]] = defaultdict(list)

        for commonality in self._iter_sims():
            num = commonality.cmn_lines_nb
            lineset1 = commonality.fst_lset
            start_line_1 = commonality.fst_file_start
            end_line_1 = commonality.fst_file_end
            lineset2 = commonality.snd_lset
            start_line_2 = commonality.snd_file_start
            end_line_2 = commonality.snd_file_end

            duplicate = no_duplicates[num]
            couples: set[LinesChunkLimits_T]
            for couples in duplicate:
                if (lineset1, start_line_1, end_line_1) in couples or (
                    lineset2,
                    start_line_2,
                    end_line_2,
                ) in couples:
                    break
            else:
                duplicate.append(
                    {
                        (lineset1, start_line_1, end_line_1),
                        (lineset2, start_line_2, end_line_2),
                    }
                )
        sims: list[tuple[int, set[LinesChunkLimits_T]]] = []
        ensembles: list[set[LinesChunkLimits_T]]
        for num, ensembles in no_duplicates.items():
            cpls: set[LinesChunkLimits_T]
            for cpls in ensembles:
                sims.append((num, cpls))
        return sorted(sims, reverse=True)

    def _display_sims(
        self, similarities: list[tuple[int, set[LinesChunkLimits_T]]]
    ) -> None:
        """Display computed similarities on stdout."""
        report = self._get_similarity_report(similarities)
        print(report)

    def _get_similarity_report(
        self, similarities: list[tuple[int, set[LinesChunkLimits_T]]]
    ) -> str:
        """Create a report from similarities."""
        report: str = ""
        duplicated_line_number: int = 0
        for number, couples in similarities:
            report += f"\n{number} similar lines in {len(couples)} files\n"
            couples_l = sorted(couples)
            line_set = start_line = end_line = None
            for line_set, start_line, end_line in couples_l:
                report += f"=={line_set.name}:[{start_line}:{end_line}]\n"
            if line_set:
                for line in line_set._real_lines[start_line:end_line]:
                    report += f"   {line.rstrip()}\n" if line.rstrip() else "\n"
            duplicated_line_number += number * (len(couples_l) - 1)
        total_line_number: int = sum(len(lineset) for lineset in self.linesets)
        report += (
            f"TOTAL lines={total_line_number} "
            f"duplicates={duplicated_line_number} "
            f"percent={duplicated_line_number * 100.0 / total_line_number:.2f}\n"
        )
        return report

    def _find_common(
        self,
        lineset1: LineSet,
        lineset2: LineSet,
        hashes1: LineSetHashResult,
        hashes2: LineSetHashResult,
    ) -> Generator[Commonality]:
        """Find similarities in the two given linesets.

        This the core of the algorithm. The idea is to compute the hashes of a
        minimal number of successive lines of each lineset and then compare the
        hashes. Every match of such comparison is stored in a dict that links the
        couple of starting indices in both linesets to the couple of corresponding
        starting and ending lines in both files.

        Last regroups all successive couples in a bigger one. It allows to take into
        account common chunk of lines that have more than the minimal number of
        successive lines required.
        """
        common_hashes = hashes1.hash_to_index.keys() & hashes2.hash_to_index.keys()

        # all_couples is a dict that links the couple of indices in both linesets that mark the beginning of
        # successive common lines, to the corresponding starting and ending number lines in both files
        all_couples: CplIndexToCplLines_T = {}

        for chunk_hash in sorted(
            common_hashes, key=lambda h: hashes1.hash_to_index[h][0]
        ):
            for indices_in_linesets in itertools.product(
                hashes1.hash_to_index[chunk_hash], hashes2.hash_to_index[chunk_hash]
            ):
                index_1 = indices_in_linesets[0]
                index_2 = indices_in_linesets[1]
                all_couples[LineSetStartCouple(index_1, index_2)] = (
                    CplSuccessiveLinesLimits(
                        copy.copy(hashes1.index_to_lines[index_1]),
                        copy.copy(hashes2.index_to_lines[index_2]),
                        effective_cmn_lines_nb=self.namespace.min_similarity_lines,
                    )
                )

        remove_successive(all_couples)

        for cml_stripped_l, cmn_l in all_couples.items():
            start_index_1 = cml_stripped_l.fst_lineset_index
            start_index_2 = cml_stripped_l.snd_lineset_index
            nb_common_lines = cmn_l.effective_cmn_lines_nb

            com = Commonality(
                cmn_lines_nb=nb_common_lines,
                fst_lset=lineset1,
                fst_file_start=cmn_l.first_file.start,
                fst_file_end=cmn_l.first_file.end,
                snd_lset=lineset2,
                snd_file_start=cmn_l.second_file.start,
                snd_file_end=cmn_l.second_file.end,
            )

            eff_cmn_nb = filter_noncode_lines(
                lineset1, start_index_1, lineset2, start_index_2, nb_common_lines
            )

            if eff_cmn_nb > self.namespace.min_similarity_lines:
                yield com

    def _iter_sims(self) -> Generator[Commonality]:
        """Iterate on similarities among all files, by making a Cartesian
        product.
        """
        min_lines = self.namespace.min_similarity_lines
        # Cache hash_lineset results: each lineset is compared against every
        # other, so without caching it gets hashed (N-1) times.
        cache: dict[int, LineSetHashResult] = {}
        for idx, lineset in enumerate(self.linesets[:-1]):
            for lineset2 in self.linesets[idx + 1 :]:
                lid1 = id(lineset)
                if lid1 not in cache:
                    cache[lid1] = hash_lineset(lineset, min_lines)
                lid2 = id(lineset2)
                if lid2 not in cache:
                    cache[lid2] = hash_lineset(lineset2, min_lines)
                yield from self._find_common(
                    lineset, lineset2, cache[lid1], cache[lid2]
                )

    def get_map_data(self) -> list[LineSet]:
        """Returns the data we can use for a map/reduce process.

        In this case we are returning this instance's Linesets, that is all file
        information that will later be used for vectorisation.
        """
        return self.linesets

    def combine_mapreduce_data(self, linesets_collection: list[list[LineSet]]) -> None:
        """Reduces and recombines data into a format that we can report on.

        The partner function of get_map_data()
        """
        self.linesets = [line for lineset in linesets_collection for line in lineset]


def stripped_lines(
    lines: Iterable[str],
    ignore_comments: bool,
    ignore_docstrings: bool,
    ignore_imports: bool,
    ignore_signatures: bool,
    line_enabled_callback: Callable[[str, int], bool] | None = None,
) -> list[LineSpecifs]:
    """Return tuples of line/line number/line type with leading/trailing white-space and
    any ignored code features removed.

    :param lines: a collection of lines
    :param ignore_comments: if true, any comment in the lines collection is removed from the result
    :param ignore_docstrings: if true, any line that is a docstring is removed from the result
    :param ignore_imports: if true, any line that is an import is removed from the result
    :param ignore_signatures: if true, any line that is part of a function signature is removed from the result
    :param line_enabled_callback: If called with "R0801" and a line number, a return value of False will disregard
           the line
    :return: the collection of line/line number/line type tuples
    """
    ignore_lines: set[int] = set()
    if ignore_imports or ignore_signatures:
        tree = astroid.parse("".join(lines))
        if ignore_imports:
            ignore_lines.update(
                chain.from_iterable(
                    range(node.lineno, (node.end_lineno or node.lineno) + 1)
                    for node in tree.nodes_of_class((nodes.Import, nodes.ImportFrom))
                )
            )
        if ignore_signatures:

            def _get_functions(
                functions: list[nodes.NodeNG], tree: nodes.NodeNG
            ) -> list[nodes.NodeNG]:
                """Recursively get all functions including nested in the classes from
                the.

                tree.
                """
                for node in tree.body:
                    if isinstance(node, (nodes.FunctionDef, nodes.AsyncFunctionDef)):
                        functions.append(node)

                    if isinstance(
                        node,
                        (nodes.ClassDef, nodes.FunctionDef, nodes.AsyncFunctionDef),
                    ):
                        _get_functions(functions, node)

                return functions

            functions = _get_functions([], tree)
            ignore_lines.update(
                chain.from_iterable(
                    range(
                        func.lineno,
                        func.body[0].lineno if func.body else func.tolineno + 1,
                    )
                    for func in functions
                )
            )

    strippedlines = []
    docstring = None
    for lineno, line in enumerate(lines, start=1):
        if line_enabled_callback is not None and not line_enabled_callback(
            "R0801", lineno
        ):
            continue
        line = line.strip()
        if ignore_docstrings:
            if not docstring:
                if line.startswith(('"""', "'''")):
                    docstring = line[:3]
                    line = line[3:]
                elif line.startswith(('r"""', "r'''")):
                    docstring = line[1:4]
                    line = line[4:]
            if docstring:
                if line.endswith(docstring):
                    docstring = None
                line = ""
        if ignore_comments:
            line = line.split("#", 1)[0].strip()
        if lineno in ignore_lines:
            line = ""
        if line:
            strippedlines.append(
                LineSpecifs(text=line, line_number=LineNumber(lineno - 1))
            )
    return strippedlines


@functools.total_ordering
class LineSet:
    """Holds and indexes all the lines of a single source file.

    Allows for correspondence between real lines of the source file and stripped ones, which
    are the real ones from which undesired patterns have been removed.
    """

    def __init__(
        self,
        name: str,
        lines: list[str],
        ignore_comments: bool = False,
        ignore_docstrings: bool = False,
        ignore_imports: bool = False,
        ignore_signatures: bool = False,
        line_enabled_callback: Callable[[str, int], bool] | None = None,
    ) -> None:
        self.name = name
        self._real_lines = lines
        self._stripped_lines = stripped_lines(
            lines,
            ignore_comments,
            ignore_docstrings,
            ignore_imports,
            ignore_signatures,
            line_enabled_callback=line_enabled_callback,
        )

    def __str__(self) -> str:
        return f"<Lineset for {self.name}>"

    def __len__(self) -> int:
        return len(self._real_lines)

    def __getitem__(self, index: int) -> LineSpecifs:
        return self._stripped_lines[index]

    def __lt__(self, other: LineSet) -> bool:
        return self.name < other.name

    def __hash__(self) -> int:
        return id(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LineSet):
            return False
        return self.__dict__ == other.__dict__

    @property
    def stripped_lines(self) -> list[LineSpecifs]:
        return self._stripped_lines

    @property
    def real_lines(self) -> list[str]:
        return self._real_lines


MSGS: dict[str, MessageDefinitionTuple] = {
    "R0801": (
        "Similar lines in %s files\n%s",
        "duplicate-code",
        "Indicates that a set of similar lines has been detected "
        "among multiple file. This usually means that the code should "
        "be refactored to avoid this duplication.",
    )
}


def report_similarities(
    sect: Section,
    stats: LinterStats,
    old_stats: LinterStats | None,
) -> None:
    """Make a layout with some stats about duplication."""
    lines = ["", "now", "previous", "difference"]
    lines += table_lines_from_stats(stats, old_stats, "duplicated_lines")
    sect.append(Table(children=lines, cols=4, rheaders=1, cheaders=1))


# wrapper to get a pylint checker from the similar class
class SimilaritiesChecker(BaseRawFileChecker, Symilar):
    """Checks for similarities and duplicated code.

    This computation may be memory / CPU intensive, so you
    should disable it if you experience some problems.
    """

    name = "similarities"
    msgs = MSGS
    MIN_SIMILARITY_HELP = "Minimum lines number of a similarity."
    IGNORE_COMMENTS_HELP = "Comments are removed from the similarity computation"
    IGNORE_DOCSTRINGS_HELP = "Docstrings are removed from the similarity computation"
    IGNORE_IMPORTS_HELP = "Imports are removed from the similarity computation"
    IGNORE_SIGNATURES_HELP = "Signatures are removed from the similarity computation"
    # for available dict keys/values see the option parser 'add_option' method
    options: Options = (
        (
            "min-similarity-lines",
            {
                "default": DEFAULT_MIN_SIMILARITY_LINE,
                "type": "int",
                "metavar": "<int>",
                "help": MIN_SIMILARITY_HELP,
            },
        ),
        (
            "ignore-comments",
            {
                "default": True,
                "type": "yn",
                "metavar": "<y or n>",
                "help": IGNORE_COMMENTS_HELP,
            },
        ),
        (
            "ignore-docstrings",
            {
                "default": True,
                "type": "yn",
                "metavar": "<y or n>",
                "help": IGNORE_DOCSTRINGS_HELP,
            },
        ),
        (
            "ignore-imports",
            {
                "default": True,
                "type": "yn",
                "metavar": "<y or n>",
                "help": IGNORE_IMPORTS_HELP,
            },
        ),
        (
            "ignore-signatures",
            {
                "default": True,
                "type": "yn",
                "metavar": "<y or n>",
                "help": IGNORE_SIGNATURES_HELP,
            },
        ),
    )
    reports = (("RP0801", "Duplication", report_similarities),)

    def __init__(self, linter: PyLinter) -> None:
        BaseRawFileChecker.__init__(self, linter)
        Symilar.__init__(
            self,
            min_lines=self.linter.config.min_similarity_lines,
            ignore_comments=self.linter.config.ignore_comments,
            ignore_docstrings=self.linter.config.ignore_docstrings,
            ignore_imports=self.linter.config.ignore_imports,
            ignore_signatures=self.linter.config.ignore_signatures,
        )

    def open(self) -> None:
        """Init the checkers: reset linesets and statistics information."""
        self.linesets = []
        self.linter.stats.reset_duplicated_lines()

    def process_module(self, node: nodes.Module) -> None:
        """Process a module.

        the module's content is accessible via the stream object

        stream must implement the readlines method
        """
        if self.linter.current_name is None:
            # TODO: 4.0 Fix current_name
            warnings.warn(
                (
                    "In pylint 3.0 the current_name attribute of the linter object should be a string. "
                    "If unknown it should be initialized as an empty string."
                ),
                DeprecationWarning,
                stacklevel=2,
            )
        with node.stream() as stream:
            self.append_stream(self.linter.current_name, stream, node.file_encoding)

    def close(self) -> None:
        """Compute and display similarities on closing (i.e. end of parsing)."""
        total = sum(len(lineset) for lineset in self.linesets)
        duplicated = 0
        stats = self.linter.stats
        for num, couples in self._compute_sims():
            msg = []
            lineset = start_line = end_line = None
            for lineset, start_line, end_line in couples:
                msg.append(f"=={lineset.name}:[{start_line}:{end_line}]")
            msg.sort()

            if lineset:
                for line in lineset.real_lines[start_line:end_line]:
                    msg.append(line.rstrip())

            self.add_message("R0801", args=(len(couples), "\n".join(msg)))
            duplicated += num * (len(couples) - 1)
        stats.nb_duplicated_lines += int(duplicated)
        stats.percent_duplicated_lines += float(total and duplicated * 100.0 / total)

    def get_map_data(self) -> list[LineSet]:
        """Passthru override."""
        return Symilar.get_map_data(self)

    def reduce_map_data(self, linter: PyLinter, data: list[list[LineSet]]) -> None:
        """Reduces and recombines data into a format that we can report on.

        The partner function of get_map_data()

        Calls self.close() to actually calculate and report duplicate code.
        """
        Symilar.combine_mapreduce_data(self, linesets_collection=data)
        self.close()


def register(linter: PyLinter) -> None:
    linter.register_checker(SimilaritiesChecker(linter))


def Run(argv: Sequence[str] | None = None) -> NoReturn:
    """Standalone command line access point."""
    parser = argparse.ArgumentParser(
        prog="symilar", description="Finds copy pasted blocks in a set of files."
    )
    parser.add_argument("files", nargs="+")
    parser.add_argument(
        "-d",
        "--duplicates",
        type=int,
        default=DEFAULT_MIN_SIMILARITY_LINE,
        help=SimilaritiesChecker.MIN_SIMILARITY_HELP,
    )
    parser.add_argument(
        "-i",
        "--ignore-comments",
        action="store_true",
        help=SimilaritiesChecker.IGNORE_COMMENTS_HELP,
    )
    parser.add_argument(
        "--ignore-docstrings",
        action="store_true",
        help=SimilaritiesChecker.IGNORE_DOCSTRINGS_HELP,
    )
    parser.add_argument(
        "--ignore-imports",
        action="store_true",
        help=SimilaritiesChecker.IGNORE_IMPORTS_HELP,
    )
    parser.add_argument(
        "--ignore-signatures",
        action="store_true",
        help=SimilaritiesChecker.IGNORE_SIGNATURES_HELP,
    )
    parsed_args = parser.parse_args(args=argv)
    similar_runner = Symilar(
        min_lines=parsed_args.duplicates,
        ignore_comments=parsed_args.ignore_comments,
        ignore_docstrings=parsed_args.ignore_docstrings,
        ignore_imports=parsed_args.ignore_imports,
        ignore_signatures=parsed_args.ignore_signatures,
    )
    for filename in parsed_args.files:
        with open(filename, encoding="utf-8") as stream:
            similar_runner.append_stream(filename, stream)
    similar_runner.run()
    # the sys exit must be kept because of the unit tests that rely on it
    sys.exit(0)


if __name__ == "__main__":
    Run()
