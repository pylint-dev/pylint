# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Test for the 'pylint-config' utils."""


import pytest
from pytest import CaptureFixture, MonkeyPatch

from pylint.config._pylint_config.utils import get_and_validate_format


def test_retrying_user_input_validation(
    monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]
) -> None:
    """Check that we retry after a wrong answer."""
    # Set the answers needed for the input() calls
    answers = iter(["A", "B", "EXIT", "EXIT()"])
    monkeypatch.setattr("builtins.input", lambda x: next(answers))

    with pytest.raises(SystemExit):
        get_and_validate_format()
    captured = capsys.readouterr()
    assert (
        captured.out
        == """Answer should be one of i, ini, t, toml.
Type 'exit()' if you want to exit the program.
Answer should be one of i, ini, t, toml.
Type 'exit()' if you want to exit the program.
Answer should be one of i, ini, t, toml.
Type 'exit()' if you want to exit the program.
Stopping 'pylint-config'.
"""
    )
