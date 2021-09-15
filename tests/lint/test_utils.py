from pathlib import Path, PosixPath

from pylint.lint.utils import get_fatal_error_message, prepare_crash_report


def test_prepare_crash_report(tmp_path: PosixPath) -> None:
    exception_content = "Exmessage"
    python_file = tmp_path / "myfile.py"
    python_content = "from shadok import MagicFaucet"
    with open(python_file, "w", encoding="utf8") as f:
        f.write(python_content)
    try:
        raise Exception(exception_content)
    except Exception as ex:  # pylint: disable=broad-except
        template_path = prepare_crash_report(
            ex, str(python_file), str(tmp_path / "pylint-crash-%Y.txt")
        )
    assert str(tmp_path) in str(template_path)
    with open(template_path, encoding="utf8") as f:
        template_content = f.read()
    assert python_content in template_content
    assert exception_content in template_content
    assert "in test_prepare_crash_report" in template_content
    assert "raise Exception(exception_content)" in template_content


def test_get_fatal_error_message() -> None:
    python_path = "mypath.py"
    crash_path = "crash.txt"
    msg = get_fatal_error_message(python_path, Path(crash_path))
    assert python_path in msg
    assert crash_path in msg
    assert "open an issue" in msg
