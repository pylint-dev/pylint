"""Tests for logging-too-few-args when static placeholders are present."""

import logging

logging.error("foo %s")  # [logging-too-few-args]
logging.info("Process %s started with ID %d")  # [logging-too-few-args]
logging.debug("Missing args: %s %s")  # [logging-too-few-args]
