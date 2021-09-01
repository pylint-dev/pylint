from typing import Any
from unittest.mock import patch

from _pytest.capture import CaptureFixture
from astroid import AstroidBuildingError
from mypy_extensions import NoReturn
from py._path.local import LocalPath  # type: ignore

from pylint.lint.pylinter import PyLinter
from pylint.utils import FileState


def raise_exception(*args: Any, **kwargs: Any) -> NoReturn:
    raise AstroidBuildingError(modname="spam")


@patch.object(FileState, "iter_spurious_suppression_messages", raise_exception)
def test_crash_in_file(
    linter: PyLinter, capsys: CaptureFixture, tmpdir: LocalPath
) -> None:
    args = linter.load_command_line_configuration([__file__])
    linter.crash_file_path = str(tmpdir / "pylint-crash-%Y")
    linter.check(args)
    out, err = capsys.readouterr()
    assert not out
    assert not err
    files = tmpdir.listdir()
    assert len(files) == 1
    assert "pylint-crash-20" in str(files[0])
    with open(files[0], encoding="utf8") as f:
        content = f.read()
    assert "Failed to import module spam." in content
