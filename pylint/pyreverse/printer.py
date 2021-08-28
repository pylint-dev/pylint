# Copyright (c) 2021 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""
Base class defining the interface for a printer.
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, NamedTuple, Optional

from astroid import nodes

from pylint.pyreverse.utils import get_annotation_label


class NodeType(Enum):
    CLASS = "class"
    INTERFACE = "interface"
    PACKAGE = "package"


class EdgeType(Enum):
    INHERITS = "inherits"
    IMPLEMENTS = "implements"
    ASSOCIATION = "association"
    USES = "uses"


class Layout(Enum):
    LEFT_TO_RIGHT = "LR"
    RIGHT_TO_LEFT = "RL"
    TOP_TO_BOTTOM = "TB"
    BOTTOM_TO_TOP = "BT"


class NodeProperties(NamedTuple):
    label: str
    attrs: Optional[List[str]] = None
    methods: Optional[List[nodes.FunctionDef]] = None
    color: Optional[str] = None
    fontcolor: Optional[str] = None


class Printer(ABC):
    """Base class defining the interface for a printer"""

    def __init__(
        self,
        title: str,
        layout: Optional[Layout] = None,
        use_automatic_namespace: Optional[bool] = None,
    ):
        self.title: str = title
        self.layout = layout
        self.use_automatic_namespace = use_automatic_namespace
        self.lines: List[str] = []
        self._indent = ""
        self._open_graph()

    def _inc_indent(self):
        """increment indentation"""
        self._indent += "  "

    def _dec_indent(self):
        """decrement indentation"""
        self._indent = self._indent[:-2]

    @abstractmethod
    def _open_graph(self) -> None:
        """Emit the header lines, i.e. all boilerplate code that defines things like layout etc."""

    def emit(self, line: str, force_newline: Optional[bool] = True) -> None:
        if force_newline and not line.endswith("\n"):
            line += "\n"
        self.lines.append(self._indent + line)

    @abstractmethod
    def emit_node(
        self,
        name: str,
        type_: NodeType,
        properties: Optional[NodeProperties] = None,
    ) -> None:
        """Create a new node. Nodes can be classes, packages, participants etc."""

    @abstractmethod
    def emit_edge(
        self,
        from_node: str,
        to_node: str,
        type_: EdgeType,
        label: Optional[str] = None,
    ) -> None:
        """Create an edge from one node to another to display relationships."""

    @staticmethod
    def _get_method_arguments(method: nodes.FunctionDef) -> List[str]:
        if method.args.args:
            arguments: List[nodes.AssignName] = [
                arg for arg in method.args.args if arg.name != "self"
            ]
        else:
            arguments = []

        annotations = dict(zip(arguments, method.args.annotations[1:]))
        for arg in arguments:
            annotation_label = ""
            ann = annotations.get(arg)
            if ann:
                annotation_label = get_annotation_label(ann)
            annotations[arg] = annotation_label

        return [
            f"{arg.name}: {ann}" if ann else f"{arg.name}"
            for arg, ann in annotations.items()
        ]

    def generate(self, outputfile: str) -> None:
        """Generate and save the final outputfile."""
        self._close_graph()
        with open(outputfile, "w", encoding="utf-8") as outfile:
            outfile.writelines(self.lines)

    @abstractmethod
    def _close_graph(self) -> None:
        """Emit the lines needed to properly close the graph."""
