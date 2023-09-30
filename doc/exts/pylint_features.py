#!/usr/bin/env python

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Script used to generate the features file before building the actual
documentation.
"""

from __future__ import annotations

import os

import sphinx
from sphinx.application import Sphinx

from pylint.lint import PyLinter
from pylint.utils import get_rst_title, print_full_documentation


# pylint: disable-next=unused-argument
def builder_inited(app: Sphinx | None) -> None:
    # PACKAGE/docs/exts/pylint_extensions.py --> PACKAGE/
    base_path = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    linter = PyLinter()
    linter.load_default_plugins()
    features = os.path.join(base_path, "doc", "user_guide", "checkers", "features.rst")
    with open(features, "w", encoding="utf-8") as stream:
        stream.write(get_rst_title("Pylint features", "="))
        stream.write(
            """
.. This file is auto-generated. Make any changes to the associated
.. docs extension in 'doc/exts/pylint_features.py'.

"""
        )
        print_full_documentation(linter, stream, False)


def setup(app: Sphinx) -> dict[str, str | bool]:
    app.connect("builder-inited", builder_inited)
    return {"version": sphinx.__display_version__, "parallel_read_safe": True}


if __name__ == "__main__":
    builder_inited(None)
