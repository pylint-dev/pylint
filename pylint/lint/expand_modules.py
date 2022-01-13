import os
import sys
from typing import List, Pattern, Tuple

from astroid import modutils

from pylint.typing import ErrorDescriptionDict, ModuleDescriptionDict

PATH = sys.path.copy()


def _modpath_from_file(filename, is_namespace, path=None):
    def _is_package_cb(inner_path, parts):
        return modutils.check_modpath_has_init(inner_path, parts) or is_namespace

    return modutils.modpath_from_file_with_callback(
        filename, path=path, is_package_cb=_is_package_cb
    )


def get_python_path(filepath: str) -> str:
    """TODO This get the python path with the (bad) assumption that there is always
    an __init__.py. This is not true since python 3.3 and is causing problem.
    """
    dirname = os.path.realpath(os.path.expanduser(filepath))
    if not os.path.isdir(dirname):
        dirname = os.path.dirname(dirname)
    while True:
        if not os.path.exists(os.path.join(dirname, "__init__.py")):
            return dirname
        old_dirname = dirname
        dirname = os.path.dirname(dirname)
        if old_dirname == dirname:
            return os.getcwd()


def _is_in_ignore_list_re(element: str, ignore_list_re: List[Pattern]) -> bool:
    """determines if the element is matched in a regex ignore-list"""
    return any(file_pattern.match(element) for file_pattern in ignore_list_re)


def _get_additional_search_path(something):
    module_path = get_python_path(something)
    return [".", module_path] + PATH


def expand_modules(
    files_or_modules: List[str],
    ignore_list: List[str],
    ignore_list_re: List[Pattern],
    ignore_list_paths_re: List[Pattern[str]],
) -> Tuple[List[ModuleDescriptionDict], List[ErrorDescriptionDict]]:
    """take a list of files/modules/packages and return the list of tuple
    (file, module name) which have to be actually checked
    """
    result: List[ModuleDescriptionDict] = []
    errors: List[ErrorDescriptionDict] = []

    for something in files_or_modules:
        basename = os.path.basename(something)
        if _skip_file(something, ignore_list, ignore_list_re, ignore_list_paths_re):
            continue
        additional_search_path = _get_additional_search_path(something)
        if os.path.exists(something):
            # this is a file or a directory
            try:
                modname = ".".join(
                    modutils.modpath_from_file(something, path=additional_search_path)
                )
            except ImportError:
                modname = os.path.splitext(basename)[0]
            if os.path.isdir(something):
                filepath = os.path.join(something, "__init__.py")
            else:
                filepath = something
        else:
            # suppose it's a module or package
            modname = something
            try:
                filepath = modutils.file_from_modpath(
                    modname.split("."), path=additional_search_path
                )
                if filepath is None:
                    continue
            except (ImportError, SyntaxError) as ex:
                # The SyntaxError is a Python bug and should be
                # removed once we move away from imp.find_module: https://bugs.python.org/issue10588
                errors.append({"key": "fatal", "mod": modname, "ex": ex})
                continue
        filepath = os.path.normpath(filepath)
        modparts = (modname or something).split(".")
        try:
            spec = modutils.file_info_from_modpath(
                modparts, path=additional_search_path
            )
        except ImportError:
            # Might not be acceptable, don't crash.
            is_namespace = False
            is_directory = os.path.isdir(something)
        else:
            is_namespace = modutils.is_namespace(spec)
            is_directory = modutils.is_directory(spec)
        if not is_namespace:
            result.append(
                {
                    "path": filepath,
                    "name": modname,
                    "isarg": True,
                    "basepath": filepath,
                    "basename": modname,
                }
            )
        has_init = (
            not (modname.endswith(".__init__") or modname == "__init__")
            and os.path.basename(filepath) == "__init__.py"
        )
        if has_init or is_namespace or is_directory:
            for subfilepath in modutils.get_module_files(
                os.path.dirname(filepath), ignore_list, list_all=is_namespace
            ):
                if filepath == subfilepath:
                    continue
                if _is_in_ignore_list_re(
                    os.path.basename(subfilepath), ignore_list_re
                ) or _is_in_ignore_list_re(subfilepath, ignore_list_paths_re):
                    continue

                modpath = _modpath_from_file(
                    subfilepath, is_namespace, path=additional_search_path
                )
                submodname = ".".join(modpath)
                result.append(
                    {
                        "path": subfilepath,
                        "name": submodname,
                        "isarg": False,
                        "basepath": filepath,
                        "basename": modname,
                    }
                )
    return result, errors


def _skip_file(filepath, ignore_list, ignore_list_re, ignore_list_paths_re):
    return (
        os.path.basename(filepath) in ignore_list
        or _is_in_ignore_list_re(os.path.basename(filepath), ignore_list_re)
        or _is_in_ignore_list_re(filepath, ignore_list_paths_re)
    )


def _discover_module(filename):
    result = None
    error = None
    modname = ".".join(
        modutils.modpath_from_file(filename, path=_get_additional_search_path(filename))
    )
    try:
        filepath = modutils.file_from_modpath(
            modname.split("."), path=_get_additional_search_path(filename)
        )
    except (ImportError, SyntaxError) as ex:
        # The SyntaxError is a Python bug and should be
        # removed once we move away from imp.find_module: https://bugs.python.org/issue10588
        error = {"key": "fatal", "mod": modname, "ex": ex}
    else:
        result = {
            "path": os.path.normpath(filepath),
            "name": modname,
            "isarg": False,
            "basepath": os.path.normpath(filepath),
            "basename": modname,
        }
    return result, error


def discover_modules(
    files_or_modules: List[str],
    ignore_list: List[str],
    ignore_list_re: List[Pattern],
    ignore_list_paths_re: List[Pattern[str]],
) -> Tuple[List[ModuleDescriptionDict], List[ErrorDescriptionDict]]:
    result: List[ModuleDescriptionDict] = []
    errors: List[ErrorDescriptionDict] = []
    for something in files_or_modules:
        if _skip_file(something, ignore_list, ignore_list_re, ignore_list_paths_re):
            continue
        if os.path.isfile(something):
            moddesc, error = _discover_module(something)
            if error:
                errors.append(error)
                continue
            if moddesc:
                result.append(moddesc)
        else:
            for root, _, files in os.walk(top=something, topdown=True):
                for f in files:
                    filepath = os.path.join(root, f)
                    if _skip_file(
                        filepath,
                        ignore_list,
                        ignore_list_re,
                        ignore_list_paths_re,
                    ):
                        continue
                    if not f.endswith(".py"):
                        continue
                    moddesc, error = _discover_module(filepath)
                    if error:
                        errors.append(error)
                        continue
                    if moddesc:
                        result.append(moddesc)
    return result, errors
