# Copyright (c) 2010, 2012, 2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2012 Ry4an Brase <ry4an-hg@ry4an.org>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Scott Worley <scottworley@scottworley.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2019 Taewon D. Kim <kimt33@mcmaster.ca>
# Copyright (c) 2020 Frank Harrison <frank@doublethefish.com>
# Copyright (c) 2020 Eli Fine <eli88fine@gmail.com>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import pytest
from test_config import run_with_config_file

from pylint.checkers import similar
from pylint.lint import PyLinter
from pylint.testutils import GenericTestReporter as Reporter

INPUT = Path(__file__).parent / ".." / "input"
SIMILAR1 = str(INPUT / "similar1")
SIMILAR2 = str(INPUT / "similar2")
SIMILAR3 = str(INPUT / "similar3")
SIMILAR4 = str(INPUT / "similar4")
MULTILINE = str(INPUT / "multiline-import")
HIDE_CODE_WITH_IMPORTS = str(INPUT / "hide_code_with_imports.py")
SIMILAR_A = INPUT / "similar_lines_a.py"
SIMILAR_B = INPUT / "similar_lines_b.py"


def test_ignore_comments():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run(["--ignore-comments", SIMILAR1, SIMILAR2])
    assert ex.value.code == 0
    assert (
        output.getvalue().strip()
        == (
            """
10 similar lines in 2 files
==%s:0
==%s:0
   import one
   from two import two
   three
   four
   five
   six
   seven
   eight
   nine
   ''' ten
TOTAL lines=60 duplicates=10 percent=16.67
"""
            % (SIMILAR1, SIMILAR2)
        ).strip()
    )


def test_ignore_docsrings():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run(["--ignore-docstrings", SIMILAR1, SIMILAR2])
    assert ex.value.code == 0
    assert (
        output.getvalue().strip()
        == (
            """
8 similar lines in 2 files
==%s:6
==%s:6
   seven
   eight
   nine
   ''' ten
   ELEVEN
   twelve '''
   thirteen
   fourteen

5 similar lines in 2 files
==%s:0
==%s:0
   import one
   from two import two
   three
   four
   five
TOTAL lines=60 duplicates=13 percent=21.67
"""
            % ((SIMILAR1, SIMILAR2) * 2)
        ).strip()
    )


def test_ignore_imports():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run(["--ignore-imports", SIMILAR1, SIMILAR2])
    assert ex.value.code == 0
    assert (
        output.getvalue().strip()
        == """
TOTAL lines=60 duplicates=0 percent=0.00
""".strip()
    )


def test_multiline_imports():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run([MULTILINE, MULTILINE])
    assert ex.value.code == 0
    assert (
        output.getvalue().strip()
        == (
            """
8 similar lines in 2 files
==%s:0
==%s:0
   from foo import (
     bar,
     baz,
     quux,
     quuux,
     quuuux,
     quuuuux,
   )
TOTAL lines=16 duplicates=8 percent=50.00
"""
            % (MULTILINE, MULTILINE)
        ).strip()
    )


def test_ignore_multiline_imports():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run(["--ignore-imports", MULTILINE, MULTILINE])
    assert ex.value.code == 0
    assert (
        output.getvalue().strip()
        == """
TOTAL lines=16 duplicates=0 percent=0.00
""".strip()
    )


def test_no_hide_code_with_imports():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run(["--ignore-imports"] + 2 * [HIDE_CODE_WITH_IMPORTS])
    assert ex.value.code == 0
    assert "TOTAL lines=32 duplicates=16 percent=50.00" in output.getvalue()


def test_ignore_nothing():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run([SIMILAR1, SIMILAR2])
    assert ex.value.code == 0
    assert (
        output.getvalue().strip()
        == (
            """
5 similar lines in 2 files
==%s:0
==%s:0
   import one
   from two import two
   three
   four
   five
TOTAL lines=60 duplicates=5 percent=8.33
"""
            % (SIMILAR1, SIMILAR2)
        ).strip()
    )


def test_lines_without_meaningful_content_do_not_trigger_similarity():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run([SIMILAR3, SIMILAR4])
    assert ex.value.code == 0
    assert (
        output.getvalue().strip()
        == (
            """
14 similar lines in 2 files
==%s:11
==%s:11
   b = (
       (
           [
               "Lines 12-25 still trigger a similarity...",
               "...warning, because..."
           ],
           [
               "...even after ignoring lines with only symbols..."
           ],
       ),
       (
           "...there are still 5 similar lines in this code block.",
       )
   )
TOTAL lines=50 duplicates=14 percent=28.00
"""
            % (SIMILAR3, SIMILAR4)
        ).strip()
    )


def test_help():
    output = StringIO()
    with redirect_stdout(output):
        try:
            similar.Run(["--help"])
        except SystemExit as ex:
            assert ex.code == 0
        else:
            pytest.fail("not system exit")


def test_no_args():
    output = StringIO()
    with redirect_stdout(output):
        try:
            similar.Run([])
        except SystemExit as ex:
            assert ex.code == 1
        else:
            pytest.fail("not system exit")


def test_get_map_data():
    """Tests that a SimilarChecker respects the MapReduceMixin interface"""
    linter = PyLinter(reporter=Reporter())

    # Add a parallel checker to ensure it can map and reduce
    linter.register_checker(similar.SimilarChecker(linter))

    source_streams = (
        SIMILAR_A,
        SIMILAR_B,
    )
    for fname in source_streams:
        assert fname.exists(), f"File not found! {fname}"
    expected_linelists = (
        (
            "",
            "",
            "",
            "",
            "",
            "",
            "def adipiscing(elit):",
            'etiam = "id"',
            'dictum = "purus,"',
            'vitae = "pretium"',
            'neque = "Vivamus"',
            'nec = "ornare"',
            'tortor = "sit"',
            "return etiam, dictum, vitae, neque, nec, tortor",
            "",
            "",
            "class Amet:",
            "def similar_function_3_lines(self, tellus):",
            "agittis = 10",
            "tellus *= 300",
            "return agittis, tellus",
            "",
            "def lorem(self, ipsum):",
            'dolor = "sit"',
            'amet = "consectetur"',
            "return (lorem, dolor, amet)",
            "",
            "def similar_function_5_lines(self, similar):",
            "some_var = 10",
            "someother_var *= 300",
            'fusce = "sit"',
            'amet = "tortor"',
            "return some_var, someother_var, fusce, amet",
            "",
            'def __init__(self, moleskie, lectus="Mauris", ac="pellentesque"):',
            'metus = "ut"',
            'lobortis = "urna."',
            'Integer = "nisl"',
            '(mauris,) = "interdum"',
            'non = "odio"',
            'semper = "aliquam"',
            'malesuada = "nunc."',
            'iaculis = "dolor"',
            'facilisis = "ultrices"',
            'vitae = "ut."',
            "",
            "return (",
            "metus,",
            "lobortis,",
            "Integer,",
            "mauris,",
            "non,",
            "semper,",
            "malesuada,",
            "iaculis,",
            "facilisis,",
            "vitae,",
            ")",
            "",
            "def similar_function_3_lines(self, tellus):",
            "agittis = 10",
            "tellus *= 300",
            "return agittis, tellus",
        ),
        (
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "class Nulla:",
            'tortor = "ultrices quis porta in"',
            'sagittis = "ut tellus"',
            "",
            "def pulvinar(self, blandit, metus):",
            "egestas = [mauris for mauris in zip(blandit, metus)]",
            "neque = (egestas, blandit)",
            "",
            "def similar_function_5_lines(self, similar):",
            "some_var = 10",
            "someother_var *= 300",
            'fusce = "sit"',
            'amet = "tortor"',
            'iaculis = "dolor"',
            "return some_var, someother_var, fusce, amet, iaculis, iaculis",
            "",
            "",
            "def tortor(self):",
            "ultrices = 2",
            'quis = ultricies * "porta"',
            "return ultricies, quis",
            "",
            "",
            "class Commodo:",
            "def similar_function_3_lines(self, tellus):",
            "agittis = 10",
            "tellus *= 300",
            'laoreet = "commodo "',
            "return agittis, tellus, laoreet",
        ),
    )

    data = []

    # Manually perform a 'map' type function
    for source_fname in source_streams:
        sim = similar.SimilarChecker(linter)
        with open(source_fname) as stream:
            sim.append_stream(source_fname, stream)
        # The map bit, can you tell? ;)
        data.extend(sim.get_map_data())

    assert len(expected_linelists) == len(data)
    for source_fname, expected_lines, lineset_obj in zip(
        source_streams, expected_linelists, data
    ):
        assert source_fname == lineset_obj.name
        # There doesn't seem to be a faster way of doing this, yet.
        lines = (line for idx, line in lineset_obj.enumerate_stripped())
        assert tuple(expected_lines) == tuple(lines)


def _simcheck_with_config(num_jobs, min_similarity_lines, tmp_path):
    """Runs similarity-checks for a given number of jobs and min_lines via rc-file

    Does not error

        A num_jobs value of None does not set any job config at all.
        Uses the given pytest tmp_path to write the config file.
    """

    # First write the config file configuring the similarity config we want to use
    config_file = tmp_path / "setup.cfg"
    if num_jobs is None:
        # We have differences between setting the config at all and not, allow
        # None to singify no job config
        jobs_config = ""
    else:
        jobs_config = f"""
[pylint.messages control]
jobs = {num_jobs}
"""

    config = f"""
[MASTER]
persistent=no

{jobs_config}

[SIMILARITIES]
min-similarity-lines={min_similarity_lines}
"""
    config_file.write_text(config)

    # Get the path to two files that have at least some similarities
    source_streams = [
        SIMILAR_A,
        SIMILAR_B,
    ]
    for fname in source_streams:
        assert fname.exists(), f"File not found! {fname}"

    args = [
        "--disable",
        "all",  # disable all checks
        "--enable",
        "similarities",  # enable the only checks we care about
        "--persistent=no",
    ] + source_streams

    runner, exit_code, stdout = run_with_config_file(config_file, args)
    linter = runner.linter
    expected_num_jobs = 1 if num_jobs is None else num_jobs
    assert linter.config.jobs == expected_num_jobs

    checkers = linter.get_checkers()
    hitonce = False
    for checker in checkers:
        if isinstance(checker, similar.SimilarChecker):
            assert checker.config.min_similarity_lines == min_similarity_lines
            assert not hitonce
            hitonce = True
    assert hitonce

    return exit_code, stdout


@pytest.mark.parametrize("min_similarity_lines", [0, 1, 4, 1000])
def test_configuration_is_passed_to_workers(tmp_path, min_similarity_lines):
    """Tests check_parallel passes the configuration to sub-workers

    Partially tests bug #4118 and #4173"""
    exit_no_job, stdout_no_job = _simcheck_with_config(
        None, min_similarity_lines, tmp_path
    )
    exit_single, stdout_single = _simcheck_with_config(
        1, min_similarity_lines, tmp_path
    )
    exit_multi, stdout_multi = _simcheck_with_config(2, min_similarity_lines, tmp_path)

    # Check that each run agrees on the specific similarity errors found
    # Each run should be identical
    assert stdout_no_job == stdout_single
    assert stdout_single == stdout_multi

    # Check exit-codes are the same i.e. each of the runs agree on error states.
    # This should always be true if the output comparison checks above pass.
    assert exit_no_job == exit_single
    assert exit_single == exit_multi
