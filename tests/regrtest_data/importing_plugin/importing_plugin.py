from importlib import import_module

from pylint.checkers import BaseChecker
from pylint.lint.pylinter import PyLinter


class ImportingChecker(BaseChecker):
    options = (
        (
            "settings-module",
            {
                "default": "settings",
                "type": "string",
                "metavar": "<settings module>"
            },
        ),
    )

    msgs = {
        "E9999": (
            "Importing checker error message",
            "importing-checker-error",
            "Importing checker error message",
        ),
    }

    def open(self) -> None:
        import_module(self.linter.config.settings_module)


def register(linter: "PyLinter") -> None:
    linter.register_checker(ImportingChecker(linter))
