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
    """Just a very simple Faker as astroid crashes in a number of cases we want to lint

    So of course this lints won't work at the moment but still produce a
    negative result.
    But as the test can pass, we still don't rely on the behavior, in case it changes
    in the future.
    """

    file: Path

    def __init__(self, content: bytes):
        self.content = io.BytesIO(content)

    def stream(self):
        return self.content
