# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Test the primer commands. """

from pathlib import Path
from unittest.mock import patch

import pytest

from pylint.testutils._primer.primer import Primer

HERE = Path(__file__).parent
TEST_DIR_ROOT = HERE.parent.parent
PRIMER_DIRECTORY = TEST_DIR_ROOT / ".pylint_primer_tests/"
PACKAGES_TO_PRIME_PATH = TEST_DIR_ROOT / "primer/packages_to_prime.json"
FIXTURES_PATH = HERE / "fixtures"


@pytest.mark.parametrize(
    "directory,expected",
    [
        [
            FIXTURES_PATH / "both_empty",
            """🤖 According to the primer, this change has **no effect** on the checked open source code. 🤖🎉

*This comment was generated for commit v2.14.2*""",
        ],
        [
            FIXTURES_PATH / "message_changed",
            """🤖 **Effect of this PR on checked open source code:** 🤖



**Effect on [astroid](https://github.com/PyCQA/astroid):**
The following messages are now emitted:

<details>

1) locally-disabled:
*Locally disabling redefined-builtin [we added some text in the message] (W0622)*
https://github.com/PyCQA/astroid/blob/main/astroid/__init__.py#L91

</details>

The following messages are no longer emitted:

<details>

1) locally-disabled:
*Locally disabling redefined-builtin (W0622)*
https://github.com/PyCQA/astroid/blob/main/astroid/__init__.py#L91

</details>

*This comment was generated for commit v2.14.2*""",
        ],
        [
            FIXTURES_PATH / "no_change",
            """🤖 According to the primer, this change has **no effect** on the checked open source code. 🤖🎉

*This comment was generated for commit v2.14.2*""",
        ],
    ],
)
def test_compare(directory: Path, expected: str) -> None:
    main = directory / "main.json"
    pr = directory / "pr.json"
    new_argv = [
        "python tests/primer/__main__.py",
        "compare",
        "--commit=v2.14.2",
        f"--base-file={main}",
        f"--new-file={pr}",
    ]
    with patch("sys.argv", new_argv):
        Primer(PRIMER_DIRECTORY, PACKAGES_TO_PRIME_PATH).run()
    with open(PRIMER_DIRECTORY / "comment.txt", encoding="utf8") as f:
        content = f.read()
    assert content == expected
