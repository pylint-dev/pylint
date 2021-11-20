"""Unittest for the main module"""
import os
import sys
from typing import Iterator

import pytest

from pylint.lint import fix_import_path

TEST_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
PROJECT_ROOT_DIR = os.path.abspath(os.path.join(TEST_DATA_DIR, ".."))


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
