# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Unittest for the main module."""

from __future__ import annotations

import os
import sys
from collections.abc import Iterator
from typing import Any
from unittest import mock

import pytest
from _pytest.capture import CaptureFixture
from _pytest.fixtures import SubRequest

from pylint.lint import augmented_sys_path, discover_package_path
from pylint.pyreverse import main

TEST_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
PROJECT_ROOT_DIR = os.path.abspath(os.path.join(TEST_DATA_DIR, ".."))


@pytest.fixture(name="mock_subprocess")
def mock_utils_subprocess() -> Iterator[mock.MagicMock]:
    with mock.patch("pylint.pyreverse.utils.subprocess") as mock_subprocess:
        yield mock_subprocess


@pytest.fixture
def mock_graphviz(mock_subprocess: mock.MagicMock) -> Iterator[None]:
    mock_subprocess.run.return_value = mock.Mock(
        stderr=(
            'Format: "XYZ" not recognized. Use one of: '
            "bmp canon cgimage cmap cmapx cmapx_np dot dot_json eps exr fig gd "
            "gd2 gif gv icns ico imap imap_np ismap jp2 jpe jpeg jpg json json0 "
            "mp pct pdf pic pict plain plain-ext png pov ps ps2 psd sgi svg svgz "
            "tga tif tiff tk vdx vml vmlz vrml wbmp webp xdot xdot1.2 xdot1.4 xdot_json"
        )
    )
    with mock.patch("pylint.pyreverse.utils.shutil") as mock_shutil:
        mock_shutil.which.return_value = "/usr/bin/dot"
        yield


@pytest.fixture(params=[PROJECT_ROOT_DIR, TEST_DATA_DIR])
def setup_path(request: SubRequest) -> Iterator[None]:
    current_sys_path = list(sys.path)
    sys.path[:] = []
    current_dir = os.getcwd()
    os.chdir(request.param)
    yield
    os.chdir(current_dir)
    sys.path[:] = current_sys_path


@pytest.mark.usefixtures("setup_path")
def test_project_root_in_sys_path() -> None:
    """Test the context manager adds the project root directory to sys.path.
    This should happen when pyreverse is run from any directory.
    """
    with augmented_sys_path([discover_package_path(TEST_DATA_DIR, [])]):
        assert sys.path == [PROJECT_ROOT_DIR]


@pytest.mark.parametrize(
    "py_mod_base_name",
    ("__init__", "impl"),
    ids=("explicit-namespace", "implicit-namespace"),
)
def test_discover_package_path_source_root_as_parent(
    py_mod_base_name: str,
    tmp_path: Any,
) -> None:
    """Test discover_package_path when source root is a parent of the module."""
    # Create this temporary structure:
    # /tmp_path/
    # └── project/
    #     └── my-package/
    #         └── __init__.py
    project_dir = tmp_path / "project"
    package_dir = project_dir / "mypackage"
    package_dir.mkdir(parents=True)
    (package_dir / f"{py_mod_base_name}.py").touch()

    # Test with project_dir as source root (parent of package)
    result = discover_package_path(str(package_dir), [str(project_dir)])
    assert result == str(project_dir)


@pytest.mark.parametrize(
    "py_mod_base_name",
    ("__init__", "impl"),
    ids=("explicit-namespace", "implicit-namespace"),
)
def test_discover_package_path_source_root_as_child(
    py_mod_base_name: str,
    tmp_path: Any,
) -> None:
    """Test discover_package_path when source root is a child of the module."""
    # Create this temporary structure:
    # /tmp_path/
    # └── project/
    #     └── src/
    #         └── my-package/
    #             └── __init__.py
    project_dir = tmp_path / "project"
    src_dir = project_dir / "src"
    package_dir = src_dir / "mypackage"
    package_dir.mkdir(parents=True)
    (package_dir / f"{py_mod_base_name}.py").touch()

    # Test with src_dir as source root (child of project)
    result = discover_package_path(str(project_dir), [str(src_dir)])
    assert result == str(src_dir)


@mock.patch("pylint.pyreverse.main.Linker", new=mock.MagicMock())
@mock.patch("pylint.pyreverse.main.DiadefsHandler", new=mock.MagicMock())
@mock.patch("pylint.pyreverse.main.writer")
@pytest.mark.usefixtures("mock_graphviz")
def test_graphviz_supported_image_format(
    mock_writer: mock.MagicMock, capsys: CaptureFixture[str]
) -> None:
    """Test that Graphviz is used if the image format is supported."""
    exit_code = main.Run(["-o", "png", TEST_DATA_DIR]).run()
    # Check that the right info message is shown to the user
    assert (
        "Format png is not supported natively. Pyreverse will try to generate it using Graphviz..."
        in capsys.readouterr().out
    )
    # Check that pyreverse actually made the call to create the diagram and we exit cleanly
    mock_writer.DiagramWriter().write.assert_called_once()
    assert exit_code == 0


@mock.patch("pylint.pyreverse.main.Linker", new=mock.MagicMock())
@mock.patch("pylint.pyreverse.main.DiadefsHandler", new=mock.MagicMock())
@mock.patch("pylint.pyreverse.main.writer")
@pytest.mark.usefixtures("mock_graphviz")
def test_graphviz_cant_determine_supported_formats(
    mock_writer: mock.MagicMock, mock_subprocess: mock.MagicMock, capsys: CaptureFixture
) -> None:
    """Test that Graphviz is used if the image format is supported."""
    mock_subprocess.run.return_value.stderr = "..."
    exit_code = main.Run(["-o", "png", TEST_DATA_DIR]).run()
    # Check that the right info message is shown to the user
    assert (
        "Unable to determine Graphviz supported output formats."
        in capsys.readouterr().out
    )
    # Check that pyreverse actually made the call to create the diagram and we exit cleanly
    mock_writer.DiagramWriter().write.assert_called_once()
    assert exit_code == 0


@mock.patch("pylint.pyreverse.main.Linker", new=mock.MagicMock())
@mock.patch("pylint.pyreverse.main.DiadefsHandler", new=mock.MagicMock())
@mock.patch("pylint.pyreverse.main.writer", new=mock.MagicMock())
@pytest.mark.usefixtures("mock_graphviz")
def test_graphviz_unsupported_image_format(capsys: CaptureFixture) -> None:
    """Test that Graphviz is used if the image format is supported."""
    with pytest.raises(SystemExit) as wrapped_sysexit:
        # we have to catch the SystemExit so the test execution does not stop
        main.Run(["-o", "somethingElse", TEST_DATA_DIR])
    # Check that the right info messages are shown to the user
    stdout = capsys.readouterr().out
    assert (
        "Format somethingElse is not supported natively. Pyreverse will try to generate it using Graphviz..."
        in stdout
    )
    assert "Format somethingElse is not supported by Graphviz. It supports:" in stdout
    # Check that we exited with the expected error code
    assert wrapped_sysexit.value.code == 32


@mock.patch("pylint.pyreverse.main.Linker", new=mock.MagicMock())
@mock.patch("pylint.pyreverse.main.DiadefsHandler", new=mock.MagicMock())
@mock.patch("pylint.pyreverse.main.writer")
@pytest.mark.usefixtures("mock_graphviz")
def test_verbose(_: mock.MagicMock, capsys: CaptureFixture[str]) -> None:
    """Test the --verbose flag."""
    main.Run(["--verbose", TEST_DATA_DIR]).run()
    assert "parsing" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("arg", "expected_default"),
    [
        ("mode", "PUB_ONLY"),
        ("classes", []),
        ("show_ancestors", None),
        ("all_ancestors", None),
        ("show_associated", None),
        ("all_associated", None),
        ("show_builtin", 0),
        ("show_stdlib", 0),
        ("module_names", None),
        ("output_format", "dot"),
        ("colorized", 0),
        ("max_color_depth", 2),
        ("ignore_list", ("CVS",)),
        ("project", ""),
        ("output_directory", ""),
    ],
)
@mock.patch("pylint.pyreverse.main.Run.run", new=mock.MagicMock())
@mock.patch("pylint.pyreverse.main.sys.exit", new=mock.MagicMock())
def test_command_line_arguments_defaults(arg: str, expected_default: Any) -> None:
    """Test that the default arguments of all options are correct."""
    run = main.Run([TEST_DATA_DIR])
    assert getattr(run.config, arg) == expected_default


@mock.patch("pylint.pyreverse.main.writer")
def test_command_line_arguments_yes_no(
    mock_writer: mock.MagicMock,  # pylint: disable=unused-argument
) -> None:
    """Regression test for the --module-names option.

    Make sure that we support --module-names=yes syntax instead
    of using it as a flag.
    """
    exit_code = main.Run(["--module-names=yes", TEST_DATA_DIR]).run()
    assert exit_code == 0


@mock.patch("pylint.pyreverse.main.writer")
@mock.patch("pylint.pyreverse.main.sys.exit", new=mock.MagicMock())
def test_class_command(
    mock_writer: mock.MagicMock,  # pylint: disable=unused-argument
) -> None:
    """Regression test for the --class option.

    Make sure that we append multiple --class arguments to one option destination.
    """
    runner = main.Run(
        [
            "--class",
            "data.clientmodule_test.Ancestor",
            "--class",
            "data.property_pattern.PropertyPatterns",
            TEST_DATA_DIR,
        ]
    )
    assert "data.clientmodule_test.Ancestor" in runner.config.classes
    assert "data.property_pattern.PropertyPatterns" in runner.config.classes


def test_version_info(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    """Test that it is possible to display the version information."""
    test_full_version = "1.2.3.4"
    monkeypatch.setattr(main.constants, "full_version", test_full_version)  # type: ignore[attr-defined]
    with pytest.raises(SystemExit):
        main.Run(["--version"])
    out, _ = capsys.readouterr()
    assert "pyreverse is included in pylint" in out
    assert test_full_version in out
