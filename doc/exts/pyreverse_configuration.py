# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Script used to generate the pyreverse configuration page."""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

from sphinx.application import Sphinx

from pylint.pyreverse.main import OPTIONS_GROUPS, Run
from pylint.typing import OptionDict
from pylint.utils import get_rst_title


class OptionsData(NamedTuple):
    name: str
    optdict: OptionDict


PYREVERSE_PATH = (
    Path(__file__).resolve().parent.parent / "additional_tools" / "pyreverse"
)
"""Path to the pyreverse documentation folder."""


def _write_config_page(run: Run) -> None:
    """Create or overwrite the configuration page."""
    sections: list[str] = [
        f"""\
.. This file is auto-generated. Make any changes to the associated
.. docs extension in 'doc/exts/pyreverse_configuration.py'.


{get_rst_title("Usage", "#")}

``pyreverse`` is run from the command line using the following syntax::

  pyreverse [options] <packages>

where ``<packages>`` is one or more Python packages or modules to analyze.

The available options are organized into the following categories:

* :ref:`filtering-and-scope` - Control which classes and relationships appear in your diagrams
* :ref:`display-options` - Customize the visual appearance including colors and labels
* :ref:`output-control` - Select output formats and set the destination directory
* :ref:`project-configuration` - Define project settings like source roots and ignored files
"""
    ]
    options: list[OptionsData] = [OptionsData(name, info) for name, info in run.options]
    option_groups: dict[str, list[str]] = {g: [] for g in OPTIONS_GROUPS.values()}

    for option in sorted(options, key=lambda x: x.name):
        option_string = get_rst_title(f"--{option.name}", "-")
        option_string += f"*{option.optdict.get('help')}*\n\n"

        if option.optdict.get("default") == "":
            option_string += '**Default:** ``""``\n\n\n'
        else:
            option_string += f"**Default:**  ``{option.optdict.get('default')}``\n\n\n"

        option_groups[str(option.optdict.get("group"))].append(option_string)

    for group_title in OPTIONS_GROUPS.values():
        ref_title = group_title.lower().replace(" ", "-")
        sections.append(
            f"""\
.. _{ref_title}:

{get_rst_title(group_title, "=")}

{"".join(option_groups[group_title])}"""
        )

    # Join all sections and remove the final two newlines
    final_page = "\n\n".join(sections)[:-2]

    with open(PYREVERSE_PATH / "configuration.rst", "w", encoding="utf-8") as stream:
        stream.write(final_page)


# pylint: disable-next=unused-argument
def build_options_page(app: Sphinx | None) -> None:
    # Write configuration page
    _write_config_page(Run([]))


def setup(app: Sphinx) -> dict[str, bool]:
    """Connects the extension to the Sphinx process."""
    # Register callback at the builder-inited Sphinx event
    # See https://www.sphinx-doc.org/en/master/extdev/appapi.html
    app.connect("builder-inited", build_options_page)
    return {"parallel_read_safe": True}
