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
# Copyright (c) 2020 Eli Fine <ejfine@gmail.com>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2021 Maksym Humetskyi <Humetsky@gmail.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Aditya Gupta <adityagupta1089@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import pytest

from pylint.checkers import similar
from pylint.lint import PyLinter
from pylint.testutils import GenericTestReporter as Reporter

INPUT = Path(__file__).parent / ".." / "input"
SIMILAR1 = str(INPUT / "similar1")
SIMILAR2 = str(INPUT / "similar2")
SIMILAR3 = str(INPUT / "similar3")
SIMILAR4 = str(INPUT / "similar4")
SIMILAR5 = str(INPUT / "similar5")
SIMILAR6 = str(INPUT / "similar6")
SIMILAR_CLS_A = str(INPUT / "similar_cls_a.py")
SIMILAR_CLS_B = str(INPUT / "similar_cls_b.py")
EMPTY_FUNCTION_1 = str(INPUT / "similar_empty_func_1.py")
EMPTY_FUNCTION_2 = str(INPUT / "similar_empty_func_2.py")
MULTILINE = str(INPUT / "multiline-import")
HIDE_CODE_WITH_IMPORTS = str(INPUT / "hide_code_with_imports.py")


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
==%s:[0:11]
==%s:[0:11]
   import one
   from two import two
   three
   four
   five
   six
   # A full line comment
   seven
   eight
   nine
   ''' ten
TOTAL lines=62 duplicates=10 percent=16.13
"""
            % (SIMILAR1, SIMILAR2)
        ).strip()
    )


def test_ignore_docstrings():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run(["--ignore-docstrings", SIMILAR1, SIMILAR2])
    assert ex.value.code == 0
    assert (
        output.getvalue().strip()
        == (
            """
5 similar lines in 2 files
==%s:[7:15]
==%s:[7:15]
   seven
   eight
   nine
   ''' ten
   ELEVEN
   twelve '''
   thirteen
   fourteen

5 similar lines in 2 files
==%s:[0:5]
==%s:[0:5]
   import one
   from two import two
   three
   four
   five
TOTAL lines=62 duplicates=10 percent=16.13
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
TOTAL lines=62 duplicates=0 percent=0.00
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
==%s:[0:8]
==%s:[0:8]
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


def test_ignore_signatures_fail():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run([SIMILAR5, SIMILAR6])
    assert ex.value.code == 0
    assert (
        output.getvalue().strip()
        == (
            '''
9 similar lines in 2 files
==%s:[7:17]
==%s:[8:18]
       arg1: int = 3,
       arg2: Class1 = val1,
       arg3: Class2 = func3(val2),
       arg4: int = 4,
       arg5: int = 5
   ) -> Ret1:
       pass

   def example():
       """Valid function definition with docstring only."""

6 similar lines in 2 files
==%s:[0:6]
==%s:[1:7]
   @deco1(dval1)
   @deco2(dval2)
   @deco3(
       dval3,
       dval4
   )
TOTAL lines=35 duplicates=15 percent=42.86
'''
            % (SIMILAR5, SIMILAR6, SIMILAR5, SIMILAR6)
        ).strip()
    )


def test_ignore_signatures_pass():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run(["--ignore-signatures", SIMILAR5, SIMILAR6])
    assert ex.value.code == 0
    assert (
        output.getvalue().strip()
        == """
TOTAL lines=35 duplicates=0 percent=0.00
""".strip()
    )


def test_ignore_signatures_class_methods_fail():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run([SIMILAR_CLS_B, SIMILAR_CLS_A])
    assert ex.value.code == 0
    assert (
        output.getvalue().strip()
        == (
            '''
15 similar lines in 2 files
==%s:[1:18]
==%s:[1:18]
       def parent_method(
           self,
           *,
           a="",
           b=None,
           c=True,
       ):
           """Overridden method example."""

           def _internal_func(
               arg1: int = 1,
               arg2: str = "2",
               arg3: int = 3,
               arg4: bool = True,
           ):
               pass


7 similar lines in 2 files
==%s:[20:27]
==%s:[20:27]
               self,
               *,
               a=None,
               b=False,
               c="",
           ):
               pass
TOTAL lines=54 duplicates=22 percent=40.74
'''
            % (SIMILAR_CLS_A, SIMILAR_CLS_B, SIMILAR_CLS_A, SIMILAR_CLS_B)
        ).strip()
    )   


def test_ignore_signatures_class_methods_pass():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run(["--ignore-signatures", SIMILAR_CLS_B, SIMILAR_CLS_A])
    assert ex.value.code == 0
    assert (
        output.getvalue().strip()
        == """
TOTAL lines=54 duplicates=0 percent=0.00
""".strip()
    )


def test_ignore_signatures_empty_functions_fail():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run([EMPTY_FUNCTION_1, EMPTY_FUNCTION_2])
    assert ex.value.code == 0
    assert (
        output.getvalue().strip()
        == (
            '''
6 similar lines in 2 files
==%s:[1:7]
==%s:[1:7]
       arg1: int = 1,
       arg2: str = "2",
       arg3: int = 3,
       arg4: bool = True,
   ) -> None:
       """Valid function definition with docstring only."""
TOTAL lines=14 duplicates=6 percent=42.86
'''
            % (EMPTY_FUNCTION_1, EMPTY_FUNCTION_2)
        ).strip()
    )


def test_ignore_signatures_empty_functions_pass():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run(["--ignore-signatures", EMPTY_FUNCTION_1, EMPTY_FUNCTION_2])
    assert ex.value.code == 0
    assert (
        output.getvalue().strip()
        == """
TOTAL lines=14 duplicates=0 percent=0.00
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
==%s:[0:5]
==%s:[0:5]
   import one
   from two import two
   three
   four
   five
TOTAL lines=62 duplicates=5 percent=8.06
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
==%s:[11:25]
==%s:[11:25]
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
        str(INPUT / "similar_lines_a.py"),
        str(INPUT / "similar_lines_b.py"),
    )
    expected_linelists = (
        (
            "def adipiscing(elit):",
            'etiam = "id"',
            'dictum = "purus,"',
            'vitae = "pretium"',
            'neque = "Vivamus"',
            'nec = "ornare"',
            'tortor = "sit"',
            "return etiam, dictum, vitae, neque, nec, tortor",
            "class Amet:",
            "def similar_function_3_lines(self, tellus):",
            "agittis = 10",
            "tellus *= 300",
            "return agittis, tellus",
            "def lorem(self, ipsum):",
            'dolor = "sit"',
            'amet = "consectetur"',
            "return (lorem, dolor, amet)",
            "def similar_function_5_lines(self, similar):",
            "some_var = 10",
            "someother_var *= 300",
            'fusce = "sit"',
            'amet = "tortor"',
            "return some_var, someother_var, fusce, amet",
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
            "def similar_function_3_lines(self, tellus):",
            "agittis = 10",
            "tellus *= 300",
            "return agittis, tellus",
        ),
        (
            "class Nulla:",
            'tortor = "ultrices quis porta in"',
            'sagittis = "ut tellus"',
            "def pulvinar(self, blandit, metus):",
            "egestas = [mauris for mauris in zip(blandit, metus)]",
            "neque = (egestas, blandit)",
            "def similar_function_5_lines(self, similar):",
            "some_var = 10",
            "someother_var *= 300",
            'fusce = "sit"',
            'amet = "tortor"',
            'iaculis = "dolor"',
            "return some_var, someother_var, fusce, amet, iaculis, iaculis",
            "def tortor(self):",
            "ultrices = 2",
            'quis = ultricies * "porta"',
            "return ultricies, quis",
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
        with open(source_fname, encoding="utf-8") as stream:
            sim.append_stream(source_fname, stream)
        # The map bit, can you tell? ;)
        data.extend(sim.get_map_data())

    assert len(expected_linelists) == len(data)
    for source_fname, expected_lines, lineset_obj in zip(
        source_streams, expected_linelists, data
    ):
        assert source_fname == lineset_obj.name
        # There doesn't seem to be a faster way of doing this, yet.
        lines = (linespec.text for linespec in lineset_obj.stripped_lines)
        assert tuple(expected_lines) == tuple(lines)
