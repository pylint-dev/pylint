# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import io
from pathlib import Path

import pylint.interfaces
import pylint.testutils

CODEC_AND_MSG = [
    ("utf-8", tuple()),
    (
        "utf-16",
        (
            pylint.testutils.MessageTest(
                msg_id="invalid-unicode-codec",
                confidence=pylint.interfaces.HIGH,
                # node=module,
                line=1,
                end_line=1,
                col_offset=None,
                end_col_offset=None,
            ),
        ),
    ),
    (
        "utf-32",
        (
            pylint.testutils.MessageTest(
                msg_id="invalid-unicode-codec",
                confidence=pylint.interfaces.HIGH,
                # node=module,
                line=1,
                end_line=1,
                col_offset=None,
                end_col_offset=None,
            ),
        ),
    ),
    (
        "iso-8859-1",
        (
            pylint.testutils.MessageTest(
                msg_id="bad-file-encoding",
                confidence=pylint.interfaces.HIGH,
                # node=module,
                line=1,
                end_line=1,
                col_offset=None,
                end_col_offset=None,
            ),
        ),
    ),
    (
        "ascii",
        (
            pylint.testutils.MessageTest(
                msg_id="bad-file-encoding",
                confidence=pylint.interfaces.HIGH,
                # node=module,
                line=1,
                end_line=1,
                col_offset=None,
                end_col_offset=None,
            ),
        ),
    ),
]


class FakeNode:
    """Simple Faker representing a Module node.

    Astroid crashes in a number of cases if we want to lint unsupported encodings.
    So, this is used to test the behaviour of the encoding checker.
    This shall ensure that our checks keep working once Python supports UTF16/32.
    """

    file: Path

    def __init__(self, content: bytes):
        self.content = io.BytesIO(content)

    def stream(self) -> io.BytesIO:
        return self.content
