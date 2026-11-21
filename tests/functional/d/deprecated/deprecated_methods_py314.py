"""Functional tests for methods deprecated in Python 3.14."""
import pathlib

pathlib.PurePath("/tmp").as_uri()  # [deprecated-method]
pathlib.PurePosixPath("/tmp").as_uri()  # [deprecated-method]
pathlib.Path("/tmp").as_uri()  # Path overrides as_uri and is not deprecated
