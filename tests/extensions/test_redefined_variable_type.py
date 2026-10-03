# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import astroid
import pytest

from pylint.extensions.redefined_variable_type import MultipleTypesChecker
from pylint.testutils import CheckerTestCase, MessageTest


class TestMultipleTypesChecker(CheckerTestCase):
    CHECKER_CLASS = MultipleTypesChecker

    @pytest.mark.parametrize(
        "source",
        [
            "_ = []\n_ = object()\n",
            "def example():\n    _ = []\n    _ = object()\n",
        ],
    )
    def test_discard_variable_can_change_type(self, source: str) -> None:
        with self.assertNoMessages():
            self.walk(astroid.parse(source))

    def test_underscore_attribute_still_checks_type(self) -> None:
        module = astroid.parse("""
            class Example:
                def __init__(self):
                    self._ = []
                    self._ = object()
            """)
        assignment = module.body[0].body[0].body[-1]
        with self.assertAddsMessages(
            MessageTest(
                "redefined-variable-type",
                node=assignment,
                args=("self._", "list", "object"),
            ),
            ignore_position=True,
        ):
            self.walk(module)
