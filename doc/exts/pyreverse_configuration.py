# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Script used to generate the pyreverse configuration page."""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

from sphinx.application import Sphinx

from pylint.pyreverse.main import Run
from pylint.typing import OptionDict
from pylint.utils import get_rst_title


class OptionsData(NamedTuple):
    name: str
    optdict: OptionDict


PYREVERSE_PATH = Path(__file__).resolve().parent.parent / "pyreverse"
"""Path to the pyreverse documentation folder."""


def _write_config_page(run: Run) -> None:
    """Create or overwrite the configuration page."""
    sections: list[str] = [
        ".. This file is auto-generated. Make any changes to the associated\n"
        ".. docs extension in 'doc/exts/pyreverse_configuration.py'.\n\n",
        get_rst_title("Pyreverse Configuration", "^"),
    ]

    options: list[OptionsData] = [OptionsData(name, info) for name, info in run.options]

    config_string = ""
    for option in sorted(options, key=lambda x: x.name):
        config_string += get_rst_title(f"--{option.name}", '"')
        config_string += f"*{option.optdict.get('help')}*\n\n"

        if option.optdict.get("default") == "":
            config_string += '**Default:** ``""``\n\n\n'
        else:
            config_string += f"**Default:**  ``{option.optdict.get('default')}``\n\n\n"

    sections.append(config_string)
    final_page = "\n\n".join(sections)

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
