# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Create UML diagrams for classes and modules in <packages>."""

from __future__ import annotations

import sys
from collections.abc import Sequence
from typing import NoReturn

from pylint import constants
from pylint.config.arguments_manager import _ArgumentsManager
from pylint.config.arguments_provider import _ArgumentsProvider
from pylint.lint.utils import fix_import_path
from pylint.pyreverse import writer
from pylint.pyreverse.diadefslib import DiadefsHandler
from pylint.pyreverse.inspector import Linker, project_from_files
from pylint.pyreverse.utils import (
    check_graphviz_availability,
    check_if_graphviz_supports_format,
    insert_default_options,
)
from pylint.typing import Options

DIRECTLY_SUPPORTED_FORMATS = (
    "dot",
    "vcg",
    "puml",
    "plantuml",
    "mmd",
    "html",
)

OPTIONS: Options = (
    (
        "filter-mode",
        dict(
            short="f",
            default="PUB_ONLY",
            dest="mode",
            type="string",
            action="store",
            metavar="<mode>",
            help="""filter attributes and functions according to
    <mode>. Correct modes are :
                            'PUB_ONLY' filter all non public attributes
                                [DEFAULT], equivalent to PRIVATE+SPECIAL_A
                            'ALL' no filter
                            'SPECIAL' filter Python special functions
                                except constructor
                            'OTHER' filter protected and private
                                attributes""",
        ),
    ),
    (
        "class",
        dict(
            short="c",
            action="extend",
            metavar="<class>",
            type="csv",
            dest="classes",
            default=None,
            help="create a class diagram with all classes related to <class>;\
 this uses by default the options -ASmy",
        ),
    ),
    (
        "show-ancestors",
        dict(
            short="a",
            action="store",
            metavar="<ancestor>",
            type="int",
            default=None,
            help="show <ancestor> generations of ancestor classes not in <projects>",
        ),
    ),
    (
        "all-ancestors",
        dict(
            short="A",
            default=None,
            action="store_true",
            help="show all ancestors off all classes in <projects>",
        ),
    ),
    (
        "show-associated",
        dict(
            short="s",
            action="store",
            metavar="<association_level>",
            type="int",
            default=None,
            help="show <association_level> levels of associated classes not in <projects>",
        ),
    ),
    (
        "all-associated",
        dict(
            short="S",
            default=None,
            action="store_true",
            help="show recursively all associated off all associated classes",
        ),
    ),
    (
        "show-builtin",
        dict(
            short="b",
            action="store_true",
            default=False,
            help="include builtin objects in representation of classes",
        ),
    ),
    (
        "module-names",
        dict(
            short="m",
            default=None,
            type="yn",
            metavar="<y or n>",
            help="include module name in representation of classes",
        ),
    ),
    (
        "only-classnames",
        dict(
            short="k",
            action="store_true",
            default=False,
            help="don't show attributes and methods in the class boxes; this disables -f values",
        ),
    ),
    (
        "output",
        dict(
            short="o",
            dest="output_format",
            action="store",
            default="dot",
            metavar="<format>",
            type="string",
            help=(
                f"create a *.<format> output file if format is available. Available formats are: {', '.join(DIRECTLY_SUPPORTED_FORMATS)}. "
                f"Any other format will be tried to create by means of the 'dot' command line tool, which requires a graphviz installation."
            ),
        ),
    ),
    (
        "colorized",
        dict(
            dest="colorized",
            action="store_true",
            default=False,
            help="Use colored output. Classes/modules of the same package get the same color.",
        ),
    ),
    (
        "max-color-depth",
        dict(
            dest="max_color_depth",
            action="store",
            default=2,
            metavar="<depth>",
            type="int",
            help="Use separate colors up to package depth of <depth>",
        ),
    ),
    (
        "ignore",
        dict(
            type="csv",
            metavar="<file[,file...]>",
            dest="ignore_list",
            default=constants.DEFAULT_IGNORE_LIST,
            help="Files or directories to be skipped. They should be base names, not paths.",
        ),
    ),
    (
        "project",
        dict(
            default="",
            type="string",
            short="p",
            metavar="<project name>",
            help="set the project name.",
        ),
    ),
    (
        "output-directory",
        dict(
            default="",
            type="path",
            short="d",
            action="store",
            metavar="<output_directory>",
            help="set the output directory path.",
        ),
    ),
)


class Run(_ArgumentsManager, _ArgumentsProvider):
    """Base class providing common behaviour for pyreverse commands."""

    options = OPTIONS
    name = "pyreverse"

    # For mypy issue, see https://github.com/python/mypy/issues/10342
    def __init__(self, args: Sequence[str]) -> NoReturn:  # type: ignore[misc]
        _ArgumentsManager.__init__(self, prog="pyreverse", description=__doc__)
        _ArgumentsProvider.__init__(self, self)

        # Parse options
        insert_default_options()
        args = self._parse_command_line_configuration(args)

        if self.config.output_format not in DIRECTLY_SUPPORTED_FORMATS:
            check_graphviz_availability()
            print(
                f"Format {self.config.output_format} is not supported natively. Pyreverse will try to generate it using Graphviz..."
            )
            check_if_graphviz_supports_format(self.config.output_format)

        sys.exit(self.run(args))

    def run(self, args: list[str]) -> int:
        """Checking arguments and run project."""
        if not args:
            print(self.help())
            return 1
        with fix_import_path(args):
            project = project_from_files(
                args,
                project_name=self.config.project,
                black_list=self.config.ignore_list,
            )
            linker = Linker(project, tag=True)
            handler = DiadefsHandler(self.config)
            diadefs = handler.get_diadefs(project, linker)
        writer.DiagramWriter(self.config).write(diadefs)
        return 0


if __name__ == "__main__":
    Run(sys.argv[1:])
