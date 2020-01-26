import importlib

extension_names = [
    "bad_builtin",
    "broad_try_clause",
    "comparetozero",
    "docparams",
    "emptystring",
]


def get_extension_documentation(extension_name):
    indent = "  "
    base_path = "pylint.extensions."
    return indent + importlib.import_module(base_path + extension_name).__doc__
