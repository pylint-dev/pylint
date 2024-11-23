# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Script used to generate the options page."""

from __future__ import annotations

import re
from collections import defaultdict
from inspect import getmodule
from pathlib import Path
from typing import NamedTuple

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


OptionsDataDict = dict[str, list[OptionsData]]

PYLINT_BASE_PATH = Path(__file__).resolve().parent.parent.parent
"""Base path to the project folder."""

PYLINT_USERGUIDE_PATH = PYLINT_BASE_PATH / "doc" / "user_guide"
"""Path to the messages documentation folder."""

DYNAMICALLY_DEFINED_OPTIONS: dict[str, dict[str, str]] = {
    # Option name, key / values we want to modify
    "py-version": {"default": "sys.version_info[:2]"},
    "spelling-dict": {
        "choices": "Values from 'enchant.Broker().list_dicts()' depending on your local enchant installation",
        "help": "Spelling dictionary name. Available dictionaries depends on your local enchant installation",
    },
}


def _register_all_checkers_and_extensions(linter: PyLinter) -> None:
    """Registers all checkers and extensions found in the default folders."""
    initialize_checkers(linter)
    initialize_extensions(linter)


def _get_all_options(linter: PyLinter) -> OptionsDataDict:
    """Get all options registered to a linter and return the data."""
    all_options: OptionsDataDict = defaultdict(list)
    for checker in sorted(linter.get_checkers()):
        for option_name, option_info in checker.options:
            changes_to_do = DYNAMICALLY_DEFINED_OPTIONS.get(option_name, {})
            if changes_to_do:
                for key_to_change, new_value in changes_to_do.items():
                    print(
                        f"Doc value for {option_name!r}['{key_to_change}'] changed to "
                        f"{new_value!r} (instead of {option_info[key_to_change]!r})"
                    )
                    option_info[key_to_change] = new_value
            all_options[checker.name].append(
                OptionsData(
                    option_name,
                    option_info,
                    checker,
                    getmodule(checker).__name__.startswith("pylint.extensions."),  # type: ignore[union-attr]
                )
            )

    return all_options


def _create_checker_section(
    checker: str, options: list[OptionsData], linter: PyLinter
) -> str:
    checker_string = f".. _{checker}-options:\n\n"
    checker_string += get_rst_title(f"``{checker.capitalize()}`` **Checker**", "-")

    toml_doc = tomlkit.document()
    tool_table = tomlkit.table(is_super_table=True)
    toml_doc.add(tomlkit.key("tool"), tool_table)
    pylint_tool_table = tomlkit.table(is_super_table=True)
    tool_table.add(tomlkit.key("pylint"), pylint_tool_table)

    checker_table = tomlkit.table()

    for option in sorted(options, key=lambda x: x.name):
        checker_string += get_rst_title(f"--{option.name}", '"')
        checker_string += f"*{option.optdict.get('help')}*\n\n"
        if option.optdict.get("default") == "":
            checker_string += '**Default:** ``""``\n\n\n'
        else:
            checker_string += f"**Default:**  ``{option.optdict.get('default')}``\n\n\n"

        # Start adding the option to the toml example
        if option.optdict.get("hide_from_config_file"):
            continue

        # Get current value of option
        try:
            value = DYNAMICALLY_DEFINED_OPTIONS[option.name]["default"]
        except KeyError:
            value = getattr(linter.config, option.name.replace("-", "_"))

        # Create a comment if the option has no value
        if value is None:
            checker_table.add(tomlkit.comment(f"{option.name} ="))
            checker_table.add(tomlkit.nl())
            continue

        # Display possible choices
        choices = option.optdict.get("choices", "")
        if choices:
            checker_table.add(tomlkit.comment(f"Possible choices: {choices}"))

        # Tomlkit doesn't support regular expressions
        if isinstance(value, re.Pattern):
            value = value.pattern
        elif (
            isinstance(value, (list, tuple))
            and value
            and isinstance(value[0], re.Pattern)
        ):
            value = [i.pattern for i in value]

        # Sorting in order for the output to be the same on all interpreters
        # Don't sort everything here, alphabetical order do not make a lot of sense
        # for options most of the time. Only dict based 'unstable' options need this
        if isinstance(value, (list, tuple)) and option.name in ["disable"]:
            value = sorted(value, key=lambda x: str(x))

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

**Note:** Only ``tool.pylint`` is required, the section title is not. These are the default values.

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
        ".. docs extension in 'doc/exts/pylint_options.py'.\n\n"
        ".. _all-options:",
        get_rst_title("Standard Checkers", "^"),
    ]
    found_extensions = False
    # We can't sort without using the 'key' keyword because if keys in 'options' were
    # checkers then it wouldn't be possible to have a checker with the same name
    # spanning multiple classes. It would make pylint plugin code less readable by
    # forcing to use a single class / file.
    for checker_name, checker_options in sorted(
        options.items(), key=lambda x: x[1][0].checker
    ):
        if not found_extensions and checker_options[0].extension:
            sections.append(get_rst_title("Extensions", "^"))
            found_extensions = True
        sections.append(_create_checker_section(checker_name, checker_options, linter))

    all_options_path = PYLINT_USERGUIDE_PATH / "configuration" / "all-options.rst"
    sections_string = "\n\n".join(sections)
    with open(all_options_path, "w", encoding="utf-8") as stream:
        stream.write(f"\n\n{sections_string}")


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


def setup(app: Sphinx) -> dict[str, bool]:
    """Connects the extension to the Sphinx process."""
    # Register callback at the builder-inited Sphinx event
    # See https://www.sphinx-doc.org/en/master/extdev/appapi.html
    app.connect("builder-inited", build_options_page)
    return {"parallel_read_safe": True}


if __name__ == "__main__":
    print("Uncomment the following line to allow running this script directly.")
    # build_options_page(None)
