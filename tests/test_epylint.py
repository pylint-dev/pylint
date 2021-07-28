"""Test for issue https://github.com/PyCQA/pylint/issues/4286"""
# pylint: disable=redefined-outer-name
import pytest

from pylint import epylint as lint


@pytest.fixture()
def example_path(tmp_path):
    content = """class IvrAudioApp:

    def run(self):
        self.hassan()
    """
    path = tmp_path / "my_app.py"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def test_epylint_good_command(example_path):
    out, err = lint.py_run(
        "%s -E --disable=E1111 --msg-template '{category} {module} {obj} {line} {column} {msg}'"
        % example_path,
        return_std=True,
    )
    msg = out.read()
    assert (
        msg
        == """\
************* Module my_app
 error my_app IvrAudioApp.run 4 8 Instance of 'IvrAudioApp' has no 'hassan' member
 """
    )
    assert err.read() == ""


def test_epylint_strange_command(example_path):
    out, err = lint.py_run(
        "%s -E --disable=E1111 --msg-template={category} {module} {obj} {line} {column} {msg}"
        % example_path,
        return_std=True,
    )
    assert (
        out.read()
        == """\
************* Module {module}
 fatal
 ************* Module {obj}
 fatal
 ************* Module {line}
 fatal
 ************* Module {column}
 fatal
 ************* Module {msg}
 fatal
 ************* Module my_app
 error
 """
    )
    assert err.read() == ""
