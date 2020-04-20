import unittest.mock

import pylint.lint


def test_can_read_toml(tmp_path):
    config_file = tmp_path / "pyproject.toml"
    config_file.write_text(
        "[tool.pylint.'messages control']\n"
        "disable='all'\n"
        "enable='missing-module-docstring'\n"
        "jobs=10\n"
    )
    linter = pylint.lint.PyLinter()
    linter.global_set_option = unittest.mock.MagicMock()
    linter.read_config_file(str(config_file))

    assert linter.global_set_option.called_with("disable", "all")
    assert linter.global_set_option.called_with("enable", "missing-module-docstring")
    assert linter.global_set_option.called_with("jobs", 10)


def test_can_read_setup_cfg(tmp_path):
    config_file = tmp_path / "setup.cfg"
    config_file.write_text(
        "[pylint.messages control]\n"
        "disable=all\n"
        "enable=missing-module-docstring\n"
        "jobs=10\n"
    )
    linter = pylint.lint.PyLinter()
    linter.global_set_option = unittest.mock.MagicMock()
    linter.read_config_file(str(config_file))

    assert linter.global_set_option.called_with("disable", "all")
    assert linter.global_set_option.called_with("enable", "missing-module-docstring")
    assert linter.global_set_option.called_with("jobs", 10)
