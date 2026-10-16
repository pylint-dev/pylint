"""Tests for logging-unsupported-format (issue #10752)

According to Python logging documentation, no formatting is performed
when no arguments are supplied. This test verifies that unsupported
format characters are only reported when arguments are provided.
"""

import logging

# These should NOT trigger warnings (no args = no formatting)
logging.error("%test")
logging.warning("%badformat")
logging.info("%z - invalid specifier")
logging.debug("%q %k %z - multiple invalid")

# These SHOULD trigger warnings (args provided = formatting attempted)
logging.error("%test", 123)  # [logging-unsupported-format]
logging.warning("%bad", "arg")  # [logging-unsupported-format]
logging.info("Value: %s, Invalid: %z", "test", "val")  # [logging-unsupported-format]

# Valid format strings should work fine
logging.info("User %s logged in", "john")
logging.debug("Count: %d", 42)
