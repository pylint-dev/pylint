# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Generic classes/functions for pyreverse core/extensions."""
import os
import re
import shutil
import subprocess
import sys
from typing import Optional, Union

import astroid
from astroid import nodes

RCFILE = ".pyreverserc"


def get_default_options():
    """Read config file and return list of options."""
    options = []
    home = os.environ.get("HOME", "")
    if home:
        rcfile = os.path.join(home, RCFILE)
        try:
            with open(rcfile, encoding="utf-8") as file_handle:
                options = file_handle.read().split()
        except OSError:
            pass  # ignore if no config file found
    return options


def insert_default_options():
    """Insert default options to sys.argv."""
    options = get_default_options()
    options.reverse()
    for arg in options:
        sys.argv.insert(1, arg)


# astroid utilities ###########################################################
SPECIAL = re.compile(r"^__([^\W_]_*)+__$")
PRIVATE = re.compile(r"^__(_*[^\W_])+_?$")
PROTECTED = re.compile(r"^_\w*$")


def get_visibility(name):
    """Return the visibility from a name: public, protected, private or special."""
    if SPECIAL.match(name):
        visibility = "special"
    elif PRIVATE.match(name):
        visibility = "private"
    elif PROTECTED.match(name):
        visibility = "protected"

    else:
        visibility = "public"
    return visibility


ABSTRACT = re.compile(r"^.*Abstract.*")
FINAL = re.compile(r"^[^\W\da-z]*$")


def is_abstract(node):
    """Return true if the given class node correspond to an abstract class
    definition
    """
    return ABSTRACT.match(node.name)


def is_final(node):
    """Return true if the given class/function node correspond to final
    definition
    """
    return FINAL.match(node.name)


def is_interface(node):
    # bw compat
    return node.type == "interface"


def is_exception(node):
    # bw compat
    return node.type == "exception"


# Helpers #####################################################################

_CONSTRUCTOR = 1
_SPECIAL = 2
_PROTECTED = 4
_PRIVATE = 8
MODES = {
    "ALL": 0,
    "PUB_ONLY": _SPECIAL + _PROTECTED + _PRIVATE,
    "SPECIAL": _SPECIAL,
    "OTHER": _PROTECTED + _PRIVATE,
}
VIS_MOD = {
    "special": _SPECIAL,
    "protected": _PROTECTED,
    "private": _PRIVATE,
    "public": 0,
}


class FilterMixIn:
    """Filter nodes according to a mode and nodes' visibility."""

    def __init__(self, mode):
        """Init filter modes."""
        __mode = 0
        for nummod in mode.split("+"):
            try:
                __mode += MODES[nummod]
            except KeyError as ex:
                print(f"Unknown filter mode {ex}", file=sys.stderr)
        self.__mode = __mode

    def show_attr(self, node):
        """Return true if the node should be treated."""
        visibility = get_visibility(getattr(node, "name", node))
        return not self.__mode & VIS_MOD[visibility]


class ASTWalker:
    """A walker visiting a tree in preorder, calling on the handler:.

    * visit_<class name> on entering a node, where class name is the class of
    the node in lower case

    * leave_<class name> on leaving a node, where class name is the class of
    the node in lower case
    """

    def __init__(self, handler):
        self.handler = handler
        self._cache = {}

    def walk(self, node, _done=None):
        """Walk on the tree from <node>, getting callbacks from handler."""
        if _done is None:
            _done = set()
        if node in _done:
            raise AssertionError((id(node), node, node.parent))
        _done.add(node)
        self.visit(node)
        for child_node in node.get_children():
            assert child_node is not node
            self.walk(child_node, _done)
        self.leave(node)
        assert node.parent is not node

    def get_callbacks(self, node):
        """Get callbacks from handler for the visited node."""
        klass = node.__class__
        methods = self._cache.get(klass)
        if methods is None:
            handler = self.handler
            kid = klass.__name__.lower()
            e_method = getattr(
                handler, f"visit_{kid}", getattr(handler, "visit_default", None)
            )
            l_method = getattr(
                handler, f"leave_{kid}", getattr(handler, "leave_default", None)
            )
            self._cache[klass] = (e_method, l_method)
        else:
            e_method, l_method = methods
        return e_method, l_method

    def visit(self, node):
        """Walk on the tree from <node>, getting callbacks from handler."""
        method = self.get_callbacks(node)[0]
        if method is not None:
            method(node)

    def leave(self, node):
        """Walk on the tree from <node>, getting callbacks from handler."""
        method = self.get_callbacks(node)[1]
        if method is not None:
            method(node)


class LocalsVisitor(ASTWalker):
    """Visit a project by traversing the locals dictionary."""

    def __init__(self):
        super().__init__(self)
        self._visited = set()

    def visit(self, node):
        """Launch the visit starting from the given node."""
        if node in self._visited:
            return None

        self._visited.add(node)
        methods = self.get_callbacks(node)
        if methods[0] is not None:
            methods[0](node)
        if hasattr(node, "locals"):  # skip Instance and other proxy
            for local_node in node.values():
                self.visit(local_node)
        if methods[1] is not None:
            return methods[1](node)
        return None


def get_annotation_label(ann: Union[nodes.Name, nodes.NodeNG]) -> str:
    if isinstance(ann, nodes.Name) and ann.name is not None:
        return ann.name
    if isinstance(ann, nodes.NodeNG):
        return ann.as_string()
    return ""


def get_annotation(
    node: Union[nodes.AssignAttr, nodes.AssignName]
) -> Optional[Union[nodes.Name, nodes.Subscript]]:
    """Return the annotation for `node`."""
    ann = None
    if isinstance(node.parent, nodes.AnnAssign):
        ann = node.parent.annotation
    elif isinstance(node, nodes.AssignAttr):
        init_method = node.parent.parent
        try:
            annotations = dict(zip(init_method.locals, init_method.args.annotations))
            ann = annotations.get(node.parent.value.name)
        except AttributeError:
            pass
    else:
        return ann

    try:
        default, *_ = node.infer()
    except astroid.InferenceError:
        default = ""

    label = get_annotation_label(ann)
    if ann:
        label = (
            rf"Optional[{label}]"
            if getattr(default, "value", "value") is None
            and not label.startswith("Optional")
            else label
        )
    if label:
        ann.name = label
    return ann


def infer_node(node: Union[nodes.AssignAttr, nodes.AssignName]) -> set:
    """Return a set containing the node annotation if it exists
    otherwise return a set of the inferred types using the NodeNG.infer method
    """

    ann = get_annotation(node)
    try:
        if ann:
            if isinstance(ann, nodes.Subscript):
                return {ann}
            return set(ann.infer())
        return set(node.infer())
    except astroid.InferenceError:
        return {ann} if ann else set()


def check_graphviz_availability():
    """Check if the ``dot`` command is available on the machine.

    This is needed if image output is desired and ``dot`` is used to convert
    from *.dot or *.gv into the final output format.
    """
    if shutil.which("dot") is None:
        print("'Graphviz' needs to be installed for your chosen output format.")
        sys.exit(32)


def check_if_graphviz_supports_format(output_format: str) -> None:
    """Check if the ``dot`` command supports the requested output format.

    This is needed if image output is desired and ``dot`` is used to convert
    from *.gv into the final output format.
    """
    dot_output = subprocess.run(
        ["dot", "-T?"], capture_output=True, check=False, encoding="utf-8"
    )
    match = re.match(
        pattern=r".*Use one of: (?P<formats>(\S*\s?)+)",
        string=dot_output.stderr.strip(),
    )
    if not match:
        print(
            "Unable to determine Graphviz supported output formats. "
            "Pyreverse will continue, but subsequent error messages "
            "regarding the output format may come from Graphviz directly."
        )
        return
    supported_formats = match.group("formats")
    if output_format not in supported_formats.split():
        print(
            f"Format {output_format} is not supported by Graphviz. It supports: {supported_formats}"
        )
        sys.exit(32)
