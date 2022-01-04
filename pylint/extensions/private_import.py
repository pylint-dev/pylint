"""Check for use of for loops that only check for a condition."""
import os
from typing import TYPE_CHECKING, List, Optional, Set, Union

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages, is_node_in_typing_guarded_import_block
from pylint.interfaces import IAstroidChecker

if TYPE_CHECKING:
    from pylint.lint.pylinter import PyLinter


class PrivateImportChecker(BaseChecker):

    __implements__ = (IAstroidChecker,)
    name = "import-private-name"
    msgs = {
        "C0416": (
            "Imported private %s (%s)",
            "import-private-name",
            "Used when a private module or object prefixed with _ is imported",
        ),
    }

    def __init__(self, linter: Optional["PyLinter"] = None):
        BaseChecker.__init__(self, linter)
        self.all_used_type_annotations = None

    @check_messages("import-private-name")
    def visit_import(self, node: nodes.Import) -> None:
        if is_node_in_typing_guarded_import_block(node):
            return
        self._check_import_private_name(
            node, [name[0] for name in node.names], checking_objects=False
        )

    @check_messages("import-private-name")
    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        if is_node_in_typing_guarded_import_block(node):
            return
        check_imported_names = self._check_import_private_name(
            node, [node.modname], checking_objects=False
        )
        if check_imported_names:
            if self.all_used_type_annotations is None:
                module_node = node
                while module_node.parent:
                    module_node = module_node.parent
                self.all_used_type_annotations = self._populate_type_annotations(
                    module_node, set()
                )
            self._check_import_private_name(
                node,
                [
                    name[0]
                    for name in node.names
                    if name[0] not in self.all_used_type_annotations
                ],
                checking_objects=True,
            )

    def _check_import_private_name(
        self, node: nodes.Import, names: List[str], checking_objects: bool
    ) -> bool:
        """Checks if the import is private. Checking an object if checking_objects is True else a module
        Returns True if the module is external and public because we want to check a module's imported names
        """
        if not checking_objects:
            # Check only external modules
            names = [name for name in names if not self.same_root_dir(node, name)]
            if not names:
                return (
                    False  # The module is internal, do not have to check imported names
                )

        private_names = [name for name in names if self._name_is_private(name)]
        if not private_names:
            return True  # The module name is not private, so check imported names
        private_imports = ", ".join(private_names)
        type_ = "object" if checking_objects else "module"
        self.add_message(
            "import-private-name", node=node, args=(type_, private_imports)
        )
        return False  # The module name is private and external; short-circuit checking imported names

    @staticmethod
    def _populate_type_annotations(
        node: Union[nodes.Module, nodes.ClassDef], all_used_type_annotations: Set
    ) -> Set[str]:
        """Adds into the set all_used_type_annotations the names of all names ever used as a type annotation
        in the scope and class definition scopes of node
        """
        for name in node.locals:
            for usage_node in node.locals[name]:
                if isinstance(usage_node, nodes.AssignName) and isinstance(
                    usage_node.parent, nodes.AnnAssign
                ):
                    all_used_type_annotations.add(usage_node.parent.annotation.name)
                elif isinstance(usage_node, nodes.ClassDef):
                    PrivateImportChecker._populate_type_annotations(
                        usage_node, all_used_type_annotations
                    )
                elif isinstance(usage_node, nodes.FunctionDef):
                    all_used_type_annotations = (
                        PrivateImportChecker._populate_type_annotations_function(
                            usage_node, all_used_type_annotations
                        )
                    )
        return all_used_type_annotations

    @staticmethod
    def _populate_type_annotations_function(
        node: nodes.FunctionDef, all_used_type_annotations: Set
    ) -> Set[str]:
        """Adds into the set all_used_type_annotations the names of all names used as a type annotation
        in the arguments and return type of the function node
        """
        if node.args:  # pylint: disable=too-many-nested-blocks
            for arg in node.args.args:
                if arg.parent.annotations:
                    for annotation in arg.parent.annotations:
                        if isinstance(
                            annotation, nodes.Subscript
                        ):  # e.g. Optional[type]
                            while isinstance(
                                annotation, nodes.Subscript
                            ):  # In the case of Optional[List[type]]
                                all_used_type_annotations.add(
                                    annotation.value.name
                                )  # Add the names of slices
                                annotation = annotation.slice
                        if isinstance(annotation, nodes.Name):
                            all_used_type_annotations.add(annotation.name)
        if node.returns:
            all_used_type_annotations.add(node.returns.name)
        return all_used_type_annotations

    @staticmethod
    def same_root_dir(node: nodes.Import, import_mod_name: str) -> bool:
        """Returns if the path of the file of node has a directory with same name as the base name of import_mod_name"""
        if not import_mod_name:  # from . import ...
            return True

        base_import_package = import_mod_name.split(".")[0]
        while node.parent:
            node = node.parent

        return base_import_package in os.path.dirname(node.file).split(os.sep)

    @staticmethod
    def _name_is_private(name: str) -> bool:
        """Returns true if the name exists, starts with `_`, and if len(name) > 4
        it is not a dunder, i.e. it does not begin and end with two underscores
        """
        return (
            bool(name)
            and name[0] == "_"
            and (len(name) <= 4 or (name[1] != "_" and name[-2:] != "__"))
        )


def register(linter: "PyLinter") -> None:
    linter.register_checker(PrivateImportChecker(linter))
