# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from collections.abc import Callable

import pytest
from astroid.nodes.scoped_nodes import Module

from pylint.lint import augmented_sys_path, discover_package_path
from pylint.pyreverse.inspector import Project, project_from_files
from pylint.testutils.pyreverse import PyreverseConfig
from pylint.typing import GetProjectCallable


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
def get_project() -> GetProjectCallable:
    def _get_project(module: str, name: str | None = "No Name") -> Project:
        """Return an astroid project representation."""

        def _astroid_wrapper(func: Callable[[str], Module], modname: str) -> Module:
            return func(modname)

        with augmented_sys_path([discover_package_path(module, [])]):
            project = project_from_files([module], _astroid_wrapper, project_name=name)
        return project

    return _get_project
