# pylint: disable=missing-docstring,consider-using-with,redefined-outer-name

import pytest


@pytest.fixture
def qm_file():
    qm_file = open("src/test/resources/example_qm_file.csv", encoding="utf-8").read()
    return qm_file
