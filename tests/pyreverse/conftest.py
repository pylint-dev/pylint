from typing import List

import pytest
from attr import dataclass


@dataclass
class PyreverseConfig:  # pylint: disable=too-many-instance-attributes
    mode: str = "PUB_ONLY"
    classes: List = []
    show_ancestors: int = None
    all_ancestors: bool = None
    show_associated: int = None
    all_associated: bool = None
    show_builtin: bool = False
    module_names: bool = None
    only_classnames: bool = False
    output_format: str = "dot"
    colorized: bool = False
    max_color_depth: int = 2
    ignore_list: List = []
    project: str = ""
    output_directory: str = ""


@pytest.fixture()
def default_config():
    return PyreverseConfig()


@pytest.fixture()
def colorized_dot_config():
    return PyreverseConfig(
        colorized=True,
    )


@pytest.fixture()
def black_and_white_vcg_config():
    return PyreverseConfig(
        output_format="vcg",
    )


@pytest.fixture()
def standard_puml_config():
    return PyreverseConfig(
        output_format="puml",
    )


@pytest.fixture()
def colorized_puml_config():
    return PyreverseConfig(output_format="puml", colorized=True)
