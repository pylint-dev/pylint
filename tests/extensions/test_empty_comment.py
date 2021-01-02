from pathlib import Path

import pytest

import pylint.extensions.empty_comment as empty_comment


@pytest.fixture(scope="module")
def checker():
    return empty_comment.CommentChecker


@pytest.fixture(scope="module")
def enable():
    return ["empty-comment"]


@pytest.fixture(scope="module")
def disable():
    return ["all"]


def test_comment_base_case(linter):
    comment_test = str(Path(__file__).parent.joinpath("data", "empty_comment.py"))
    linter.check([comment_test])
    msgs = linter.reporter.messages
    assert len(msgs) == 4
    for msg in msgs:
        assert msg.symbol == "empty-comment"
        assert msg.msg == "Line with empty comment"
    assert msgs[0].line == 2
    assert msgs[1].line == 3
    assert msgs[2].line == 5
    assert msgs[3].line == 7
