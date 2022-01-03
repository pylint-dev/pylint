"""Check for use of for loops that only check for a condition."""
import optparse  # pylint: disable=deprecated-module
from typing import TYPE_CHECKING, List, Optional

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages, is_node_in_typing_guarded_import_block
from pylint.interfaces import IAstroidChecker
from pylint.utils import IsortDriver

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
        self.config = optparse.Values(
            defaults={"known_standard_library": (), "known_third_party": ()}
        )
        self.isort_driver = IsortDriver(self.config)

    @check_messages("import-private-name")
    def visit_import(self, node: nodes.Import) -> None:
        self._check_import_private_name(
            node, [name[0] for name in node.names], checking_objects=False
        )

    @check_messages("import-private-name")
    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        private_module = self._check_import_private_name(
            node, [node.modname], checking_objects=False
        )
        if not private_module:
            self._check_import_private_name(
                node, [name[0] for name in node.names], checking_objects=True
            )

    def _check_import_private_name(
        self, node: nodes.Import, names: List[str], checking_objects: bool
    ) -> bool:
        """Checks if the import is private. Checking an object if checking_objects is True else a module
        Returns True if a message was emitted
        """
        if is_node_in_typing_guarded_import_block(node):
            return True
        if not checking_objects:
            # Check only external modules; internal private imports are allowed
            names = [
                name
                for name in names
                if self.isort_driver.place_module(name) in {"THIRDPARTY", "STDLIB"}
            ]
            if len(names) == 0:
                return True

        private_names = [name for name in names if self._name_is_private(name)]
        if len(private_names) > 0:
            private_imports = ", ".join(private_names)
            self.add_message(
                "import-private-name",
                node=node,
                args=("object" if checking_objects else "module", private_imports),
            )
            return True
        return False

    @staticmethod
    def _name_is_private(name):
        """Returns true if the name exists, starts with `_`, and if len(name) > 4
        it is not a dunder, i.e. it does not begin and end with two underscores
        """
        return (
            name
            and name[0] == "_"
            and (len(name) <= 4 or (name[1] != "_" and name[-2:] != "__"))
        )

    # def load_configuration(linter: "PyLinter"):
    #     imports_checker = get_checker(linter, ImportsChecker)


def register(linter: "PyLinter") -> None:
    linter.register_checker(PrivateImportChecker(linter))
