"""Calls built from ``unittest.mock.call`` describe expected calls on a mock. #7351"""
from unittest import mock
from unittest.mock import MagicMock, call

MOCK = MagicMock()
MOCK.assert_has_calls([call.HasDunder.__setitem__(1, 2)])
MOCK.assert_has_calls([call.__getitem__(1), mock.call.method().__enter__()])

# Dunder calls on the mock itself are still reported
MOCK.__enter__()  # [unnecessary-dunder-call]
