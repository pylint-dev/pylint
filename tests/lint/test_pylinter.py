from unittest.mock import patch

from astroid import AstroidBuildingError

from pylint.utils import FileState


def raise_exception(*args, **kwargs):
    raise AstroidBuildingError(modname="spam")


@patch.object(FileState, "iter_spurious_suppression_messages", raise_exception)
def test_crash_in_file(linter, capsys, tmpdir):
    args = linter.load_command_line_configuration([__file__])
    linter.crash_file_prefix = tmpdir / "pylint-crash-"
    linter.check(args)
    out, err = capsys.readouterr()
    assert not out
    assert not err
    files = tmpdir.listdir()
    assert len(files) == 1
    assert "pylint-crash" in str(files[0])
    with open(files[0], encoding="utf8") as f:
        content = f.read()
    assert "Failed to import module spam." in content
