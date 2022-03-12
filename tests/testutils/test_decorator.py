# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors


import pytest

from pylint.testutils.decorator import set_config_directly


def test_deprecation_of_set_config_directly() -> None:
    """Test that the deprecation of set_config_directly works as expected."""

    with pytest.warns(DeprecationWarning) as records:
        set_config_directly()
        assert len(records) == 1
