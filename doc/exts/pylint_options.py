# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Script used to generate the options page."""

from __future__ import annotations

import re
from collections import defaultdict
from inspect import getmodule
from pathlib import Path
from typing import Dict, List, NamedTuple

import tomlkit
from sphinx.application import Sphinx

from pylint.checkers import initialize as initialize_checkers
from pylint.checkers.base_checker import BaseChecker
from pylint.extensions import initialize as initialize_extensions
from pylint.lint import PyLinter
from pylint.typing import OptionDict
from pylint.utils import get_rst_title


class OptionsData(NamedTuple):
    name: str
    optdict: OptionDict
    checker: BaseChecker
    extension: bool


OptionsDataDict = Dict[str, List[OptionsData]]

PYLINT_BASE_PATH = Path(__file__).resolve().parent.parent.parent
"""Base path to the project folder."""

PYLINT_USERGUIDE_PATH = PYLINT_BASE_PATH / "doc" / "user_guide"
"""Path to the messages documentation folder."""


def _register_all_checkers_and_extensions(linter: PyLinter) -> None:
    """Registers all checkers and extensions found in the default folders."""
    initialize_checkers(linter)
    initialize_extensions(linter)


def _get_all_options(linter: PyLinter) -> OptionsDataDict:
    """Get all options registered to a linter and return the data."""
    all_options: OptionsDataDict = defaultdict(list)
    for checker in sorted(linter.get_checkers()):
        ch_name = checker.name
        for option in checker.options:
            all_options[ch_name].append(
                OptionsData(
                    option[0],
                    option[1],
                    checker,
                    getmodule(checker).__name__.startswith("pylint.extensions."),  # type: ignore[union-attr]
                )
            )

    return all_options


def _create_checker_section(
    checker: str, options: list[OptionsData], linter: PyLinter
) -> str:
    checker_string = get_rst_title(f"``{checker.capitalize()}`` Checker", "^")
    toml_doc = tomlkit.document()
    pylint_tool_table = tomlkit.table(is_super_table=True)
    toml_doc.add(tomlkit.key(["tool", "pylint"]), pylint_tool_table)

    checker_table = tomlkit.table()

    for option in sorted(options, key=lambda x: x.name):
        checker_string += get_rst_title(f"--{option.name}", '"')
        checker_string += f"\nDescription:\n  *{option.optdict.get('help')}*\n\n"
        if option.optdict.get("default") == "":
            checker_string += 'Default:\n  ``""``\n\n\n'
        else:
            checker_string += f"Default:\n  ``{option.optdict.get('default')}``\n\n\n"

        # Start adding the option to the toml example
        if option.optdict.get("hide_from_config_file"):
            continue

        # Get current value of option
        value = getattr(linter.config, option.name.replace("-", "_"))

        # Create a comment if the option has no value
        if value is None:
            checker_table.add(tomlkit.comment(f"{option.name} ="))
            checker_table.add(tomlkit.nl())
            continue

        # Tomlkit doesn't support regular expressions
        if isinstance(value, re.Pattern):
            value = value.pattern
        elif (
            isinstance(value, (list, tuple))
            and value
            and isinstance(value[0], re.Pattern)
        ):
            value = [i.pattern for i in value]

        # Add to table
        checker_table.add(option.name, value)
        checker_table.add(tomlkit.nl())

    pylint_tool_table.add(options[0].checker.name.lower(), checker_table)
    toml_string = "\n".join(
        f"   {i}" if i else "" for i in tomlkit.dumps(toml_doc).split("\n")
    )
    checker_string += f"""
.. raw:: html

   <details>
   <summary><a>Example configuration section</a></summary>

**Note:** Only ``pylint.tool`` is required, the section title is not. These are the default values.

.. code-block:: toml

{toml_string}

.. raw:: html

   </details>
"""

    return checker_string


def _write_options_page(options: OptionsDataDict, linter: PyLinter) -> None:
    """Create or overwrite the options page."""
    sections: list[str] = [
        ".. This file is auto-generated. Make any changes to the associated\n"
        ".. docs extension in 'doc/exts/pylint_options.py'.",
        get_rst_title("Standard Checkers:", "^"),
    ]
    found_extensions = False

    for checker, checker_options in options.items():
        if not found_extensions and checker_options[0].extension:
            sections.append(get_rst_title("Extensions:", "^"))
            found_extensions = True
        sections.append(_create_checker_section(checker, checker_options, linter))

    sections_string = "\n\n".join(sections)
    with open(
        PYLINT_USERGUIDE_PATH / "configuration" / "all-options.rst",
        "w",
        encoding="utf-8",
    ) as stream:
        stream.write(
            f"""

{sections_string}"""
        )


# pylint: disable-next=unused-argument
def build_options_page(app: Sphinx | None) -> None:
    """Overwrite messages files by printing the documentation to a stream.

    Documentation is written in ReST format.
    """
    # Create linter, register all checkers and extensions and get all options
    linter = PyLinter()
    _register_all_checkers_and_extensions(linter)

    options = _get_all_options(linter)

    # Write options page
    _write_options_page(options, linter)


def setup(app: Sphinx) -> None:
    """Connects the extension to the Sphinx process."""
    # Register callback at the builder-inited Sphinx event
    # See https://www.sphinx-doc.org/en/master/extdev/appapi.html
    app.connect("builder-inited", build_options_page)


if __name__ == "__main__":
    pass
    # Uncomment to allow running this script by your local python interpreter
    # build_options_page(None)
