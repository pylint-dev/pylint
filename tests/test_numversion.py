# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

import pytest

from pylint.__pkginfo__ import get_numversion_from_version


@pytest.mark.parametrize(
    "version,expected_numversion",
    [
        ["2.8.1", (2, 8, 1)],
        ["2.8.2+", (2, 8, 2)],
        ["3.0.0a0", (3, 0, 0)],
        ["3..0", (3, 0, 0)],
        ["1.a", (1, 0, 0)],
        ["", (0, 0, 0)],
        ["3.0.0b1", (3, 0, 0)],
        ["3.0.0rc1", (3, 0, 0)],
        ["3.0.0dev-234324234234f23abc4", (3, 0, 0)],
        ["pylint-2.4.7", (2, 4, 7)],
        ["2.8.3.dev3+g28c093c2.d20210428", (2, 8, 3)],
    ],
)
def test_numversion(version, expected_numversion):
    assert get_numversion_from_version(version) == expected_numversion
