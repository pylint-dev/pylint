"""Unittest for the main module."""
import os
import sys
from typing import Iterator
from unittest import mock

import pytest

from pylint.lint import fix_import_path
from pylint.pyreverse import main

TEST_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
PROJECT_ROOT_DIR = os.path.abspath(os.path.join(TEST_DATA_DIR, ".."))


@pytest.fixture(name="mock_subprocess")
def mock_utils_subprocess():
    with mock.patch("pylint.pyreverse.utils.subprocess") as mock_subprocess:
        yield mock_subprocess


@pytest.fixture
def mock_graphviz(mock_subprocess):
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
def setup_path(request) -> Iterator:
    current_sys_path = list(sys.path)
    sys.path[:] = []
    current_dir = os.getcwd()
    os.chdir(request.param)
    yield
    os.chdir(current_dir)
    sys.path[:] = current_sys_path


@pytest.mark.usefixtures("setup_path")
def test_project_root_in_sys_path():
    """Test the context manager adds the project root directory to sys.path.
    This should happen when pyreverse is run from any directory
    """
    with fix_import_path([TEST_DATA_DIR]):
        assert sys.path == [PROJECT_ROOT_DIR]


@mock.patch("pylint.pyreverse.main.Linker", new=mock.MagicMock())
@mock.patch("pylint.pyreverse.main.DiadefsHandler", new=mock.MagicMock())
@mock.patch("pylint.pyreverse.main.writer")
@pytest.mark.usefixtures("mock_graphviz")
def test_graphviz_supported_image_format(mock_writer, capsys):
    """Test that Graphviz is used if the image format is supported."""
    with pytest.raises(SystemExit) as wrapped_sysexit:
        # we have to catch the SystemExit so the test execution does not stop
        main.Run(["-o", "png", TEST_DATA_DIR])
    # Check that the right info message is shown to the user
    assert (
        "Format png is not supported natively. Pyreverse will try to generate it using Graphviz..."
        in capsys.readouterr().out
    )
    # Check that pyreverse actually made the call to create the diagram and we exit cleanly
    mock_writer.DiagramWriter().write.assert_called_once()
    assert wrapped_sysexit.value.code == 0


@mock.patch("pylint.pyreverse.main.Linker", new=mock.MagicMock())
@mock.patch("pylint.pyreverse.main.DiadefsHandler", new=mock.MagicMock())
@mock.patch("pylint.pyreverse.main.writer")
@pytest.mark.usefixtures("mock_graphviz")
def test_graphviz_cant_determine_supported_formats(
    mock_writer, mock_subprocess, capsys
):
    """Test that Graphviz is used if the image format is supported."""
    mock_subprocess.run.return_value.stderr = "..."
    with pytest.raises(SystemExit) as wrapped_sysexit:
        # we have to catch the SystemExit so the test execution does not stop
        main.Run(["-o", "png", TEST_DATA_DIR])
    # Check that the right info message is shown to the user
    assert (
        "Unable to determine Graphviz supported output formats."
        in capsys.readouterr().out
    )
    # Check that pyreverse actually made the call to create the diagram and we exit cleanly
    mock_writer.DiagramWriter().write.assert_called_once()
    assert wrapped_sysexit.value.code == 0


@mock.patch("pylint.pyreverse.main.Linker", new=mock.MagicMock())
@mock.patch("pylint.pyreverse.main.DiadefsHandler", new=mock.MagicMock())
@mock.patch("pylint.pyreverse.main.writer", new=mock.MagicMock())
@pytest.mark.usefixtures("mock_graphviz")
def test_graphviz_unsupported_image_format(capsys):
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
