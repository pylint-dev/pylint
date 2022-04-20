# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import argparse


# This class could and should be replaced with a simple dataclass when support for Python < 3.7 is dropped.
# A NamedTuple is not possible as some tests need to modify attributes during the test.
class PyreverseConfig(
    argparse.Namespace
):  # pylint: disable=too-many-instance-attributes, too-many-arguments
    """Holds the configuration options for Pyreverse.

    The default values correspond to the defaults of the options' parser.
    """

    def __init__(
        self,
        mode: str = "PUB_ONLY",
        classes: list[str] | None = None,
        show_ancestors: int | None = None,
        all_ancestors: bool | None = None,
        show_associated: int | None = None,
        all_associated: bool | None = None,
        show_builtin: bool = False,
        module_names: bool | None = None,
        only_classnames: bool = False,
        output_format: str = "dot",
        colorized: bool = False,
        max_color_depth: int = 2,
        ignore_list: tuple[str, ...] = tuple(),
        project: str = "",
        output_directory: str = "",
    ) -> None:
        super().__init__()
        self.mode = mode
        if classes:
            self.classes = classes
        else:
            self.classes = []
        self.show_ancestors = show_ancestors
        self.all_ancestors = all_ancestors
        self.show_associated = show_associated
        self.all_associated = all_associated
        self.show_builtin = show_builtin
        self.module_names = module_names
        self.only_classnames = only_classnames
        self.output_format = output_format
        self.colorized = colorized
        self.max_color_depth = max_color_depth
        self.ignore_list = ignore_list
        self.project = project
        self.output_directory = output_directory
