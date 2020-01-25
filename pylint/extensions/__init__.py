import importlib


class ExtensionStore:
    extension_names = [
        "bad_builtin",
        "broad_try_clause",
        "check_elif",
        "comparetozero",
        "docparams",
        "docstyle",
        "emptystring",
        "mccabe",
        "overlapping_exceptions",
        "redefined_variable_type",
    ]

    @staticmethod
    def get_extension_documentation(extension_name):
        indent = "  "
        base_path = "pylint.extensions."
        return indent + importlib.import_module(base_path + extension_name).__doc__
