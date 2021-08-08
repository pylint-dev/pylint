from dataclasses import dataclass, field
from typing import List, Optional

import pytest


@dataclass
class PyreverseConfig:  # pylint: disable=too-many-instance-attributes
    """Holds the configuration options for Pyreverse.
    The default values correspond to the defaults of the options parser."""

    mode: str = "PUB_ONLY"
    classes: List = field(default_factory=list)
    show_ancestors: Optional[int] = None
    all_ancestors: Optional[bool] = None
    show_associated: Optional[int] = None
    all_associated: Optional[bool] = None
    show_builtin: bool = False
    module_names: Optional[bool] = None
    only_classnames: bool = False
    output_format: str = "dot"
    ignore_list: List = field(default_factory=list)
    project: str = ""
    output_directory: str = ""


@pytest.fixture()
def default_config():
    return PyreverseConfig()


@pytest.fixture()
def vcg_config():
    return PyreverseConfig(
        output_format="vcg",
    )
