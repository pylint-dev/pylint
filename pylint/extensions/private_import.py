"""Check for imports on private external modules and names"""
from pathlib import Path
from typing import TYPE_CHECKING, List, Set, Union

from astroid import nodes

from pylint.checkers import BaseChecker, utils
from pylint.interfaces import HIGH, IAstroidChecker

if TYPE_CHECKING:
    from pylint.lint.pylinter import PyLinter


class PrivateImportChecker(BaseChecker):

    __implements__ = (IAstroidChecker,)
    name = "import-private-name"
    msgs = {
        "C2601": (
            "Imported private %s (%s)",
            "import-private-name",
            "Used when a private module or object prefixed with _ is imported. "
            "PEP8 guidance on Naming Conventions states that public attributes with"
            "leading underscores should be considered private.",
        ),
    }

    def __init__(self, linter: "PyLinter") -> None:
        BaseChecker.__init__(self, linter)
        self.all_used_type_annotations: Set[str] = set()
        self.populated_annotations = False

    @utils.check_messages("import-private-name")
    def visit_import(self, node: nodes.Import) -> None:
        if utils.is_node_in_typing_guarded_import_block(node):
            return
        names = [name[0] for name in node.names]
        private_names = self._get_private_imports(names)
        if private_names:
            imported_identifier = "modules" if len(private_names) > 1 else "module"
            private_name_string = ", ".join(private_names)
            self.add_message(
                "import-private-name",
                node=node,
                args=(imported_identifier, private_name_string),
            )

    @utils.check_messages("import-private-name")
    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        if utils.is_node_in_typing_guarded_import_block(node):
            return
        private_module_imports = self._get_private_imports([node.modname])
        if private_module_imports:  # If module is private, do not check imported names
            self.add_message(
                "import-private-name",
                node=node,
                args=("module", private_module_imports[0]),
            )
        elif not self.same_root_dir(
            node, node.modname
        ):  # Only check imported names if the module is external

            # Only check names not used as type annotations
            if not self.populated_annotations:
                self._populate_type_annotations(
                    node.root(), self.all_used_type_annotations
                )
                self.populated_annotations = True
            names = [
                n[0] for n in node.names if n[0] not in self.all_used_type_annotations
            ]

            private_names = self._get_private_imports(names)
            if private_names:
                imported_identifier = "objects" if len(private_names) > 1 else "object"
                private_name_string = ", ".join(private_names)
                self.add_message(
                    "import-private-name",
                    node=node,
                    args=(imported_identifier, private_name_string),
                    confidence=HIGH,
                )

    def _get_private_imports(
        self,
        names: List[str],
    ) -> List[str]:
        """Returns the private names from input names by a simple string check"""
        private_names = [name for name in names if self._name_is_private(name)]
        return private_names

    @staticmethod
    def _name_is_private(name: str) -> bool:
        """Returns true if the name exists, starts with `_`, and if len(name) > 4
        it is not a dunder, i.e. it does not begin and end with two underscores
        """
        return (
            bool(name)
            and name[0] == "_"
            and (len(name) <= 4 or name[1] != "_" or name[-2:] != "__")
        )

    @staticmethod
    def _populate_type_annotations(
        node: nodes.LocalsDictNodeNG,
        all_used_type_annotations: Set[str],
    ) -> None:
        """Adds into the set all_used_type_annotations the names of all names ever used as a type annotation
        in the scope and class definition scopes of node
        """
        for name in node.locals:
            for usage_node in node.locals[name]:
                if isinstance(usage_node, nodes.AssignName) and isinstance(
                    usage_node.parent, nodes.AnnAssign
                ):
                    PrivateImportChecker._populate_type_annotations_annotation(
                        usage_node.parent.annotation, all_used_type_annotations
                    )
                if isinstance(usage_node, nodes.FunctionDef):
                    PrivateImportChecker._populate_type_annotations_function(
                        usage_node, all_used_type_annotations
                    )
                if isinstance(usage_node, nodes.LocalsDictNodeNG):
                    PrivateImportChecker._populate_type_annotations(
                        usage_node, all_used_type_annotations
                    )

    @staticmethod
    def _populate_type_annotations_function(
        node: nodes.FunctionDef, all_used_type_annotations: Set[str]
    ) -> None:
        """Adds into the set all_used_type_annotations the names of all names used as a type annotation
        in the arguments and return type of the function node
        """
        if node.args.annotations:
            for annotation in node.args.annotations:
                PrivateImportChecker._populate_type_annotations_annotation(
                    annotation, all_used_type_annotations
                )
        if node.returns:
            PrivateImportChecker._populate_type_annotations_annotation(
                node.returns, all_used_type_annotations
            )

    @staticmethod
    def _populate_type_annotations_annotation(
        node: Union[nodes.Attribute, nodes.Subscript, nodes.Name],
        all_used_type_annotations: Set,
    ) -> None:
        """Handles the possiblity of an annotation either being a Name, i.e. just type,
        or a Subscript e.g. Optional[type] or an Attribute, e.g. pylint.lint.linter
        """
        if isinstance(node, nodes.Name):
            all_used_type_annotations.add(node.name)
        elif isinstance(node, nodes.Subscript):  # e.g. Optional[List[str]]
            # value is the current type name: could be a Name or Attribute
            PrivateImportChecker._populate_type_annotations_annotation(
                node.value, all_used_type_annotations
            )
            # slice is the next nested type
            PrivateImportChecker._populate_type_annotations_annotation(
                node.slice, all_used_type_annotations
            )
        elif isinstance(node, nodes.Attribute):
            # An attribute is a type like `pylint.lint.pylinter`. node.expr is the next level up, could be another attribute
            PrivateImportChecker._populate_type_annotations_annotation(
                node.expr, all_used_type_annotations
            )

    @staticmethod
    def same_root_dir(node: nodes.Import, import_mod_name: str) -> bool:
        """Does the node's file's path contain the base name of 'import_mod_name'?"""
        if not import_mod_name:  # from . import ...
            return True

        base_import_package = import_mod_name.split(".")[0]

        return base_import_package in Path(node.root().file).parent.parts


def register(linter: "PyLinter") -> None:
    linter.register_checker(PrivateImportChecker(linter))
