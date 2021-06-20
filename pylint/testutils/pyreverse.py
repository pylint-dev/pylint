# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE


from typing import Optional

from pylint.pyreverse.inspector import Project, project_from_files


def get_project(module: str, name: Optional[str] = "No Name") -> Project:
    """return an astroid project representation"""

    def _astroid_wrapper(func, modname):
        return func(modname)

    return project_from_files([module], _astroid_wrapper, project_name=name)
