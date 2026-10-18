# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import textwrap
from contextlib import redirect_stdout
from io import BytesIO, StringIO
from pathlib import Path

import astroid
import pytest
from _pytest.capture import CaptureFixture

from pylint.checkers import symilar
from pylint.checkers.symilar import LineSet, LineSetStartCouple, Symilar
from pylint.lint import PyLinter
from pylint.reporters.ureports.nodes import Section, Table
from pylint.testutils import GenericTestReporter as Reporter
from pylint.utils import LinterStats

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


def test_ignore_comments() -> None:
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run(["--ignore-comments", SIMILAR1, SIMILAR2])
    assert ex.value.code == 0
    assert output.getvalue().strip() == (f"""
10 similar lines in 2 files
=={SIMILAR1}:[0:11]
=={SIMILAR2}:[0:11]
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
""").strip()


def test_ignore_docstrings() -> None:
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run(["--ignore-docstrings", SIMILAR1, SIMILAR2])
    assert ex.value.code == 0
    assert output.getvalue().strip() == (f"""
5 similar lines in 2 files
=={SIMILAR1}:[0:5]
=={SIMILAR2}:[0:5]
   import one
   from two import two
   three
   four
   five

5 similar lines in 2 files
=={SIMILAR1}:[7:15]
=={SIMILAR2}:[7:15]
   seven
   eight
   nine
   ''' ten
   ELEVEN
   twelve '''
   thirteen
   fourteen
TOTAL lines=62 duplicates=10 percent=16.13
""").strip()


def test_ignore_imports() -> None:
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run(["--ignore-imports", SIMILAR1, SIMILAR2])
    assert ex.value.code == 0
    assert output.getvalue().strip() == """
TOTAL lines=62 duplicates=0 percent=0.00
""".strip()


def test_multiline_imports() -> None:
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run([MULTILINE, MULTILINE])
    assert ex.value.code == 0
    assert output.getvalue().strip() == (f"""
8 similar lines in 2 files
=={MULTILINE}:[0:8]
=={MULTILINE}:[0:8]
   from foo import (
     bar,
     baz,
     quux,
     quuux,
     quuuux,
     quuuuux,
   )
TOTAL lines=16 duplicates=8 percent=50.00
""").strip()


def test_ignore_multiline_imports() -> None:
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run(["--ignore-imports", MULTILINE, MULTILINE])
    assert ex.value.code == 0
    assert output.getvalue().strip() == """
TOTAL lines=16 duplicates=0 percent=0.00
""".strip()


def test_ignore_signatures_fail() -> None:
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run([SIMILAR5, SIMILAR6])
    assert ex.value.code == 0
    assert output.getvalue().strip() == (f'''
9 similar lines in 2 files
=={SIMILAR5}:[7:17]
=={SIMILAR6}:[8:18]
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
=={SIMILAR5}:[0:6]
=={SIMILAR6}:[1:7]
   @deco1(dval1)
   @deco2(dval2)
   @deco3(
       dval3,
       dval4
   )
TOTAL lines=35 duplicates=15 percent=42.86
''').strip()


def test_ignore_signatures_pass() -> None:
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run(["--ignore-signatures", SIMILAR5, SIMILAR6])
    assert ex.value.code == 0
    assert output.getvalue().strip() == """
TOTAL lines=35 duplicates=0 percent=0.00
""".strip()


def test_ignore_signatures_class_methods_fail() -> None:
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run([SIMILAR_CLS_B, SIMILAR_CLS_A])
    assert ex.value.code == 0
    assert output.getvalue().strip() == (f'''
15 similar lines in 2 files
=={SIMILAR_CLS_A}:[1:18]
=={SIMILAR_CLS_B}:[1:18]
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
=={SIMILAR_CLS_A}:[20:27]
=={SIMILAR_CLS_B}:[20:27]
               self,
               *,
               a=None,
               b=False,
               c="",
           ):
               pass
TOTAL lines=54 duplicates=22 percent=40.74
''').strip()


def test_ignore_signatures_class_methods_pass() -> None:
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run(["--ignore-signatures", SIMILAR_CLS_B, SIMILAR_CLS_A])
    assert ex.value.code == 0
    assert output.getvalue().strip() == """
TOTAL lines=54 duplicates=0 percent=0.00
""".strip()


def test_ignore_signatures_empty_functions_fail() -> None:
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run([EMPTY_FUNCTION_1, EMPTY_FUNCTION_2])
    assert ex.value.code == 0
    assert output.getvalue().strip() == (f'''
6 similar lines in 2 files
=={EMPTY_FUNCTION_1}:[1:7]
=={EMPTY_FUNCTION_2}:[1:7]
       arg1: int = 1,
       arg2: str = "2",
       arg3: int = 3,
       arg4: bool = True,
   ) -> None:
       """Valid function definition with docstring only."""
TOTAL lines=14 duplicates=6 percent=42.86
''').strip()


def test_ignore_signatures_empty_functions_pass() -> None:
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run(["--ignore-signatures", EMPTY_FUNCTION_1, EMPTY_FUNCTION_2])
    assert ex.value.code == 0
    assert output.getvalue().strip() == """
TOTAL lines=14 duplicates=0 percent=0.00
""".strip()


def test_no_hide_code_with_imports() -> None:
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run(["--ignore-imports"] + 2 * [HIDE_CODE_WITH_IMPORTS])
    assert ex.value.code == 0
    assert "TOTAL lines=32 duplicates=0 percent=0.00" in output.getvalue()


def test_ignore_nothing() -> None:
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run([SIMILAR1, SIMILAR2])
    assert ex.value.code == 0
    assert output.getvalue().strip() == (f"""
5 similar lines in 2 files
=={SIMILAR1}:[0:5]
=={SIMILAR2}:[0:5]
   import one
   from two import two
   three
   four
   five
TOTAL lines=62 duplicates=5 percent=8.06
""").strip()


def test_lines_without_meaningful_content_do_not_trigger_similarity() -> None:
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run([SIMILAR3, SIMILAR4])
    assert ex.value.code == 0
    assert output.getvalue().strip() == (f"""
14 similar lines in 2 files
=={SIMILAR3}:[11:25]
=={SIMILAR4}:[11:25]
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
""").strip()


def test_help() -> None:
    output = StringIO()
    with redirect_stdout(output):
        try:
            symilar.Run(["--help"])
        except SystemExit as ex:
            assert ex.code == 0
        else:
            pytest.fail("not system exit")


def test_no_args(capsys: CaptureFixture) -> None:
    output = StringIO()
    with redirect_stdout(output):
        try:
            symilar.Run([])
        except SystemExit as ex:
            assert ex.code == 2
            out, err = capsys.readouterr()
            assert not out
            assert "the following arguments are required: files" in err
        else:
            pytest.fail("not system exit")


def test_get_map_data() -> None:
    """Tests that a SymilarChecker can return and reduce mapped data."""
    linter = PyLinter(reporter=Reporter())
    # Add a parallel checker to ensure it can map and reduce
    linter.register_checker(symilar.SimilaritiesChecker(linter))
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
        sim = symilar.SimilaritiesChecker(PyLinter())
        sim.linter.set_option("ignore-imports", False)
        sim.linter.set_option("ignore-signatures", False)
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


def test_set_duplicate_lines_to_zero() -> None:
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run(["--duplicates=0", SIMILAR1, SIMILAR2])
    assert ex.value.code == 0
    assert output.getvalue() == ""


def test_equal_short_form_option() -> None:
    """Regression test for https://github.com/pylint-dev/pylint/issues/9343"""
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run(["-d=2", SIMILAR1, SIMILAR2])
    assert ex.value.code == 0
    assert "similar lines in" in output.getvalue()


def test_space_short_form_option() -> None:
    """Regression test for https://github.com/pylint-dev/pylint/issues/9343"""
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run(["-d 2", SIMILAR1, SIMILAR2])
    assert ex.value.code == 0
    assert "similar lines in" in output.getvalue()


def test_bad_short_form_option(capsys: CaptureFixture) -> None:
    """Regression test for https://github.com/pylint-dev/pylint/issues/9343"""
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run(["-j=0", SIMILAR1, SIMILAR2])
    out, err = capsys.readouterr()
    assert ex.value.code == 2
    assert not out
    assert "unrecognized arguments: -j=0" in err


def test_line_set_start_couple_eq_non_couple() -> None:
    """``LineSetStartCouple.__eq__`` returns ``NotImplemented`` against an
    object that isn't a ``LineSetStartCouple`` so Python falls back to
    reflected comparison.
    """
    couple = LineSetStartCouple(symilar.Index(0), symilar.Index(1))
    assert couple != object()
    # pylint: disable-next=unnecessary-dunder-call
    assert couple.__eq__(object()) is NotImplemented


def test_line_set_dunder_methods() -> None:
    """Cover LineSet ``__str__``, ``__getitem__`` and non-LineSet ``__eq__``."""
    lines = ["a = 1\n", "b = 2\n", "c = 3\n"]
    lineset = LineSet("fake.py", lines)
    assert str(lineset) == "<Lineset for fake.py>"
    assert lineset[0].text == "a = 1"
    assert (lineset == "not a lineset") is False


def test_append_stream_binary_requires_encoding() -> None:
    """``append_stream`` raises ValueError when a binary stream is passed
    without an encoding.
    """
    runner = Symilar()
    with pytest.raises(ValueError):
        runner.append_stream("bin.py", BytesIO(b"a = 1\n"))


def test_report_similarities_builds_table() -> None:
    """``report_similarities`` appends a stats table to the given section."""
    stats = LinterStats()
    stats.reset_duplicated_lines()
    section = Section()
    symilar.report_similarities(section, stats, None)
    assert len(section.children) == 1
    assert isinstance(section.children[0], Table)


def test_process_module_warns_when_current_name_is_none(tmp_path: Path) -> None:
    """``SimilaritiesChecker.process_module`` warns when
    ``linter.current_name`` is None (the deprecated state).
    """
    linter = PyLinter(reporter=Reporter())
    linter.register_checker(symilar.SimilaritiesChecker(linter))
    checker = symilar.SimilaritiesChecker(linter)
    linter.current_name = None  # type: ignore[assignment]
    module_file = tmp_path / "m.py"
    module_file.write_text("a = 1\n")

    module = astroid.parse(module_file.read_text(), module_name="m")
    module.file = str(module_file)
    module.file_bytes = module_file.read_bytes()
    with pytest.warns(DeprecationWarning, match="current_name attribute"):
        checker.process_module(module)


def test_append_stream_unicode_error_yields_empty_lineset(tmp_path: Path) -> None:
    """``append_stream`` swallows ``UnicodeDecodeError`` and treats the file
    as empty rather than crashing.
    """
    bad_file = tmp_path / "bad.py"
    bad_file.write_bytes(b"\xff\xfe\xfa not valid utf-8\n")
    runner = Symilar()
    with bad_file.open("rb") as stream:
        runner.append_stream(str(bad_file), stream, encoding="utf-8")
    assert len(runner.linesets) == 1
    assert runner.linesets[0].stripped_lines == []


def test_hash_bucket_product_limit_fallback(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """When a hash bucket's Cartesian product exceeds
    ``_HASH_BUCKET_PRODUCT_LIMIT``, ``_find_common`` falls back to aligned-zip
    pairing. Mock the limit to zero so the fallback path is always taken over
    a file with repeated blocks and verify duplicate detection still reports
    the expected similar lines.

    Regression test for https://github.com/pylint-dev/pylint/pull/10881.
    """
    monkeypatch.setattr(symilar, "_HASH_BUCKET_PRODUCT_LIMIT", 0)
    # Three copies of the same 5-line block produce hash buckets with more
    # than one index, exercising the aligned-zip fallback meaningfully.
    block = "a = 1\nb = 2\nc = 3\nd = 4\ne = 5\n"
    file_a = tmp_path / "a.py"
    file_b = tmp_path / "b.py"
    file_a.write_text(block * 3)
    file_b.write_text(block * 3)

    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        symilar.Run([str(file_a), str(file_b)])
    assert ex.value.code == 0
    out = output.getvalue()
    assert "15 similar lines in 2 files" in out
    assert f"=={file_a}:[0:15]" in out
    assert f"=={file_b}:[0:15]" in out


def _common_chunks(
    source_1: str, source_2: str, ignore_local_names: bool, min_lines: int = 4
) -> list[tuple[int, list[tuple[str, int, int]]]]:
    runner = Symilar(
        min_lines=min_lines,
        ignore_comments=True,
        ignore_docstrings=True,
        ignore_imports=True,
        ignore_signatures=True,
        ignore_local_names=ignore_local_names,
    )
    for name, source in (("first.py", source_1), ("second.py", source_2)):
        runner.append_stream(name, StringIO(textwrap.dedent(source)))
    return [
        (num, sorted((lineset.name, start, end) for lineset, start, end in couples))
        for num, couples in runner._compute_sims()
    ]


RENAMED_LOCALS_1 = """
    def total(items, rate, *extras):
        subtotal = sum(extras)
        for item in items:
            subtotal += item.price * item.quantity
        taxed = subtotal * (1 + rate)
        names = [entry.name for entry in items if entry.price > taxed]
        return round(taxed, 2), names
"""
RENAMED_LOCALS_2 = """
    def compute(rows, tax, *more):
        acc = sum(more)
        for row in rows:
            acc += row.price * row.quantity
        gross = acc * (1 + tax)
        found = [x.name for x in rows if x.price > gross]
        return round(gross, 2), found
"""


def test_ignore_local_names_finds_renamed_clone() -> None:
    assert not _common_chunks(RENAMED_LOCALS_1, RENAMED_LOCALS_2, False)
    assert _common_chunks(RENAMED_LOCALS_1, RENAMED_LOCALS_2, True) == [
        (6, [("first.py", 2, 8), ("second.py", 2, 8)])
    ]


def test_ignore_local_names_keeps_raw_text() -> None:
    lineset = LineSet("a.py", ["def f(a):\n", "    b = a\n"], ignore_local_names=True)
    assert [spec.text for spec in lineset.stripped_lines] == ["def f(a):", "b = a"]
    assert lineset.stripped_lines[1].template == "\0 = \0"
    assert lineset.stripped_lines[1].local_names == ("b", "a")


def test_ignore_local_names_rejects_inconsistent_renaming() -> None:
    """Two distinct names in one copy map to a single name in the other."""
    source_1 = """
        def f(x, y):
            a = x + y
            b = a * x - y
            c = b + x * y
            d = c - y / x
            e = d * x + y
            return e, x, y
    """
    source_2 = source_1.replace("y", "x").replace("f(x, x)", "f(x, y)")
    assert not _common_chunks(source_1, source_2, True)


@pytest.mark.parametrize(
    "original, renamed",
    [
        pytest.param("LIMIT", "CEILING", id="module-global"),
        pytest.param("self.limit", "self.ceiling", id="attribute"),
        pytest.param("clamp(value, limit=3)", "clamp(value, ceiling=3)", id="kwarg"),
        pytest.param("clamp(value)", "bound(value)", id="called-function"),
        pytest.param("json.dumps(value)", "yaml.dumps(value)", id="local-import"),
        pytest.param("helper(value)", "assist(value)", id="nested-def"),
    ],
)
def test_ignore_local_names_keeps_non_local_names(original: str, renamed: str) -> None:
    template = """
        LIMIT = CEILING = 3
        def method(self, value):
            import json, yaml
            def helper(arg):
                return arg
            def assist(arg):
                return arg
            first = {expr} + 1
            second = {expr} * 2
            third = {expr} - 3
            fourth = {expr} / 4
            fifth = {expr} % 5
            return first, second, third, fourth, fifth
    """
    source_1 = template.format(expr=original)
    source_2 = template.format(expr=renamed)
    assert not _common_chunks(source_1, source_2, True, min_lines=5)


def test_ignore_local_names_global_statement_keeps_name() -> None:
    template = """
        def bump(step):
            global {name}
            {name} += step
            {name} *= step
            {name} -= step
            {name} //= step
            {name} **= step
            return {name}
    """
    found = _common_chunks(
        template.format(name="hits"), template.format(name="misses"), True
    )
    assert not found


def test_ignore_local_names_placeholder_only_lines() -> None:
    """Lines holding nothing but local names count only when verbatim."""
    template = """
        def pack({a}, {b}, {c}, {d}, {e}):
            return build(
                {a},
                {b},
                {c},
                {d},
                {e},
            )
    """
    renamed = template.format(a="v", b="w", c="x", d="y", e="z")
    original = template.format(a="a", b="b", c="c", d="d", e="e")
    assert not _common_chunks(original, renamed, True)
    assert _common_chunks(original, original, True) == _common_chunks(
        original, original, False
    )


def test_ignore_local_names_non_ascii_columns() -> None:
    """Astroid reports columns in UTF-8 bytes, not characters."""
    template = """
        def describe({name}, {other}):
            label = "é" + {name}
            label += "ü" + {other}
            label += "ö" + {name} + {other}
            label += "ß" + {other} + {name}
            label += "ñ" + {name} * 2
            return label
    """
    found = _common_chunks(
        template.format(name="first", other="second"),
        template.format(name="alpha", other="beta"),
        True,
    )
    assert found == [(6, [("first.py", 2, 8), ("second.py", 2, 8)])]


def test_ignore_local_names_except_handler_name() -> None:
    """Astroid places the handler name at the ``except`` keyword."""
    template = """
        def guard(action, {kind}):
            try:
                action()
            except {kind} as {name}:
                log({name})
                raise RuntimeError({name}) from {name}
            finally:
                action.close()
    """
    found = _common_chunks(
        template.format(name="err", kind="error_type"),
        template.format(name="exc", kind="failure"),
        True,
    )
    assert found == [(7, [("first.py", 2, 9), ("second.py", 2, 9)])]


def test_ignore_local_names_cli(tmp_path: Path) -> None:
    file_1 = tmp_path / "first.py"
    file_2 = tmp_path / "second.py"
    file_1.write_text(textwrap.dedent(RENAMED_LOCALS_1), encoding="utf-8")
    file_2.write_text(textwrap.dedent(RENAMED_LOCALS_2), encoding="utf-8")
    for flags, expected in (([], False), (["--ignore-local-names"], True)):
        output = StringIO()
        with redirect_stdout(output), pytest.raises(SystemExit) as ex:
            symilar.Run(["--ignore-signatures", *flags, str(file_1), str(file_2)])
        assert ex.value.code == 0
        assert ("6 similar lines in 2 files" in output.getvalue()) is expected


def test_ignore_local_names_checker_option() -> None:
    linter = PyLinter(reporter=Reporter())
    checker = symilar.SimilaritiesChecker(linter)
    linter.register_checker(checker)
    linter.set_option("ignore-local-names", True)
    for name, source in (("a", RENAMED_LOCALS_1), ("b", RENAMED_LOCALS_2)):
        module = astroid.parse(textwrap.dedent(source), module_name=name)
        checker.append_stream(name, StringIO(textwrap.dedent(source)), tree=module)
    assert checker._compute_sims()


@pytest.mark.parametrize(
    "source, expected",
    [
        pytest.param(
            "def f(a, *args, **kwargs): pass\n",
            "def f(\0, *\0, **\0): pass",
            id="arguments",
        ),
        pytest.param(
            "def f(rows):\n    return [row.x for row in rows]\n",
            "return [\0.x for \0 in \0]",
            id="comprehension-and-attribute",
        ),
        pytest.param(
            "def f(a):\n    return g(a, key=lambda item: item + a)\n",
            "return g(\0, key=lambda \0: \0 + \0)",
            id="lambda-and-kwarg",
        ),
        pytest.param(
            "def f(size):\n    class Box:\n        size = 3\n"
            "        def area(self):\n            return size * size\n",
            "return \0 * \0",
            id="method-skips-class-scope",
        ),
        pytest.param(
            "def f(size):\n    class Box:\n        size = 3\n",
            "size = 3",
            id="class-attribute",
        ),
        pytest.param(
            "TOTAL = 0\ndef f(step):\n    global TOTAL\n    TOTAL += step\n",
            "TOTAL += \0",
            id="global",
        ),
    ],
)
def test_ignore_local_names_template(source: str, expected: str) -> None:
    lineset = LineSet("a.py", source.splitlines(keepends=True), ignore_local_names=True)
    assert lineset.stripped_lines[-1].template == expected
