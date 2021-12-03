from typing import Callable, Optional

import pytest
from astroid.nodes.scoped_nodes import Module

from pylint.lint import fix_import_path
from pylint.pyreverse.inspector import Project, project_from_files
from pylint.testutils.pyreverse import PyreverseConfig


@pytest.fixture()
def default_config() -> PyreverseConfig:
    return PyreverseConfig()


@pytest.fixture()
def colorized_dot_config() -> PyreverseConfig:
    return PyreverseConfig(
        output_format="dot",
        colorized=True,
    )


@pytest.fixture()
def vcg_config() -> PyreverseConfig:
    return PyreverseConfig(
        output_format="vcg",
    )


@pytest.fixture()
def puml_config() -> PyreverseConfig:
    return PyreverseConfig(
        output_format="puml",
    )


@pytest.fixture()
def colorized_puml_config() -> PyreverseConfig:
    return PyreverseConfig(
        output_format="puml",
        colorized=True,
    )


@pytest.fixture()
def mmd_config() -> PyreverseConfig:
    return PyreverseConfig(
        output_format="mmd",
        colorized=False,
    )


@pytest.fixture()
def html_config() -> PyreverseConfig:
    return PyreverseConfig(
        output_format="html",
        colorized=False,
    )


@pytest.fixture(scope="session")
def get_project() -> Callable:
    def _get_project(module: str, name: Optional[str] = "No Name") -> Project:
        """return an astroid project representation"""

        def _astroid_wrapper(func: Callable, modname: str) -> Module:
            return func(modname)

        with fix_import_path([module]):
            project = project_from_files([module], _astroid_wrapper, project_name=name)
        return project

    return _get_project
