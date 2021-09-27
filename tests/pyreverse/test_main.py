import os
import sys

import pytest

from pylint.lint import fix_import_path

TEST_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
PROJECT_ROOT_DIR = os.path.abspath(os.path.join(TEST_DATA_DIR, ".."))


@pytest.fixture(name="setup_path", params=[PROJECT_ROOT_DIR, TEST_DATA_DIR])
def fixture_setup_path(request):
    current_sys_path = list(sys.path)
    sys.path[:] = []
    current_dir = os.getcwd()
    os.chdir(request.param)
    yield request.param
    os.chdir(current_dir)
    sys.path[:] = current_sys_path


def test_project_root_in_sys_path(setup_path):
    with fix_import_path([setup_path]):
        assert sys.path == [PROJECT_ROOT_DIR]
