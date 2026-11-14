# pylint: disable=missing-module-docstring
import logging

# Regression test for https://github.com/pylint-dev/pylint/issues/10813
# A bytes format string that is not valid UTF-8 used to crash the checker
# with a ``UnicodeDecodeError``.
logging.critical(b"\xc0\xc0")

# Valid bytes format strings should still have their arguments checked.
logging.error(b"%s", "arg")
logging.error(b"%s")  # [logging-too-few-args]
logging.error(b"%s", 1, 2)  # [logging-too-many-args]
logging.info(b"%s and 50%", "x")  # [logging-format-truncated]
