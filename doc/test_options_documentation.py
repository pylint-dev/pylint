# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the options documentation generation (doc/exts/pylint_options.py)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

pytest.importorskip("sphinx")

# ``doc/exts`` is not a package - add it to ``sys.path`` so
# ``pylint_options`` is importable both inside the sphinx build
# (conf.py already does this) and when pytest is invoked from the
# project root.
_EXTS_PATH = str(Path(__file__).resolve().parent / "exts")
if _EXTS_PATH not in sys.path:
    sys.path.insert(0, _EXTS_PATH)

import pylint_options  # type: ignore[import-not-found, unused-ignore]  # pylint: disable=wrong-import-position,import-error  # noqa: E402

from pylint.checkers.base_checker import BaseChecker  # noqa: E402  # pylint: disable=wrong-import-position
from pylint.extensions.mccabe import McCabeMethodChecker  # noqa: E402  # pylint: disable=wrong-import-position
from pylint.lint import PyLinter  # noqa: E402  # pylint: disable=wrong-import-position
from pylint.typing import MessageDefinitionTuple  # noqa: E402  # pylint: disable=wrong-import-position


def test_colliding_extension_names_contains_design() -> None:
    colliding = pylint_options._get_colliding_extension_names()
    assert "design" in colliding
    # Today only ``design`` (core vs mccabe) collides.
    assert colliding == frozenset({"design"})


def test_get_options_anchor_single_source_of_truth() -> None:
    get_anchor = pylint_options._get_options_anchor
    # Colliding extension -> module-based anchor.
    assert get_anchor("design", "pylint.extensions.mccabe") == "pylint.extensions.mccabe-options"
    # Core checker (module is None) keeps name-based anchor even when colliding.
    assert get_anchor("design", None) == "design-options"
    # Non-colliding extensions keep name-based anchors.
    assert get_anchor("dunder", "pylint.extensions.dunder") == "dunder-options"
    assert get_anchor("typing", "pylint.extensions.typing") == "typing-options"
    assert get_anchor("broad_try_clause", "pylint.extensions.broad_try_clause") == "broad_try_clause-options"


def test_all_options_splits_design_checker() -> None:
    linter = PyLinter()
    pylint_options._register_all_checkers_and_extensions(linter)
    options = pylint_options._get_all_options(linter)

    # Two distinct sections: core ``design`` and colliding ext ``pylint.extensions.mccabe``.
    assert "design" in options
    assert "pylint.extensions.mccabe" in options

    core_option_names = {o.name for o in options["design"]}
    mccabe_option_names = {o.name for o in options["pylint.extensions.mccabe"]}

    assert "max-complexity" in mccabe_option_names
    assert "max-complexity" not in core_option_names

    # The colliding ext section must be flagged as extension, core as non-extension.
    assert all(o.extension for o in options["pylint.extensions.mccabe"])
    assert not any(o.extension for o in options["design"])

    # Non-colliding extension anchors are unchanged (name-based).
    assert "dunder" in options
    assert "typing" in options
    assert "broad_try_clause" in options
    # No module-based keys leaked for non-colliding extensions.
    assert "pylint.extensions.dunder" not in options
    assert "pylint.extensions.typing" not in options


def test_create_checker_section_titles() -> None:
    linter = PyLinter()
    pylint_options._register_all_checkers_and_extensions(linter)
    options = pylint_options._get_all_options(linter)

    core_section = pylint_options._create_checker_section(
        "design", options["design"], linter
    )
    assert ".. _design-options:" in core_section
    assert "``Design`` **Checker**" in core_section
    # Core section must NOT have a module suffix.
    assert "(``design``)" not in core_section
    assert "(``pylint.extensions.mccabe``)" not in core_section

    mccabe_section = pylint_options._create_checker_section(
        "pylint.extensions.mccabe", options["pylint.extensions.mccabe"], linter
    )
    assert ".. _pylint.extensions.mccabe-options:" in mccabe_section
    assert "``Design`` **Checker** (``pylint.extensions.mccabe``)" in mccabe_section


def test_get_full_documentation_options_anchor_kwarg() -> None:
    """``BaseChecker.get_full_documentation`` must honour ``options_anchor``.

    Default -> ``<design-options>``; explicit module anchor ->
    ``<pylint.extensions.mccabe-options>``.
    """
    linter = PyLinter()
    checker: BaseChecker = McCabeMethodChecker(linter)
    options = list(checker._options_and_values())
    assert options, "McCabe checker must expose --max-complexity"

    default_doc = checker.get_full_documentation(
        msgs=checker.msgs,
        options=options,
        reports=checker.reports,
        module="pylint.extensions.mccabe",
        show_options=False,
    )
    assert "<design-options>" in default_doc

    module_doc = checker.get_full_documentation(
        msgs=checker.msgs,
        options=options,
        reports=checker.reports,
        module="pylint.extensions.mccabe",
        show_options=False,
        options_anchor="pylint.extensions.mccabe-options",
    )
    assert "<pylint.extensions.mccabe-options>" in module_doc
    assert "<design-options>" not in module_doc

    # Non-colliding checker must be unaffected when the kwarg is not passed.
    # Use a tiny ad-hoc checker to avoid coupling to a specific extension.
    from pylint.checkers.base_checker import BaseChecker as _BC  # local import

    class _DummyChecker(_BC):
        name = "dummy_test_checker_xyz"
        msgs: dict[str, MessageDefinitionTuple] = {}
        options = (
            (
                "dummy-opt",
                {"default": 1, "type": "int", "metavar": "<int>", "help": "dummy"},
            ),
        )

    dummy = _DummyChecker(linter)
    dummy_opts = list(dummy._options_and_values())
    dummy_doc = dummy.get_full_documentation(
        msgs=dummy.msgs,
        options=dummy_opts,
        reports=dummy.reports,
        module="pylint.extensions.dummy_test_checker_xyz",
        show_options=False,
    )
    assert "<dummy_test_checker_xyz-options>" in dummy_doc
