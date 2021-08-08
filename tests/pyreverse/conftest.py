from typing import Optional, Tuple

import pytest


# This class could and should be replaced with a simple dataclass when support for Python < 3.7 is dropped.
# A NamedTuple is not possible as some tests need to modify attributes during the test.
class PyreverseConfig:  # pylint: disable=too-many-instance-attributes, too-many-arguments
    """Holds the configuration options for Pyreverse.
    The default values correspond to the defaults of the options parser."""

    def __init__(
        self,
        mode: str = "PUB_ONLY",
        classes: Tuple = tuple(),
        show_ancestors: Optional[int] = None,
        all_ancestors: Optional[bool] = None,
        show_associated: Optional[int] = None,
        all_associated: Optional[bool] = None,
        show_builtin: bool = False,
        module_names: Optional[bool] = None,
        only_classnames: bool = False,
        output_format: str = "dot",
        ignore_list: Tuple = tuple(),
        project: str = "",
        output_directory: str = "",
    ):
        self.mode = mode
        self.classes = classes
        self.show_ancestors = show_ancestors
        self.all_ancestors = all_ancestors
        self.show_associated = show_associated
        self.all_associated = all_associated
        self.show_builtin = show_builtin
        self.module_names = module_names
        self.only_classnames = only_classnames
        self.output_format = output_format
        self.ignore_list = ignore_list
        self.project = project
        self.output_directory = output_directory


@pytest.fixture()
def default_config():
    return PyreverseConfig()


@pytest.fixture()
def vcg_config():
    return PyreverseConfig(
        output_format="vcg",
    )
