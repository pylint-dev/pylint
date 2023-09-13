"""Tests for logging-not-lazy and the logging-modules option."""
# pylint: disable=import-error, consider-using-f-string

from my import logging as blogging

blogging.warn("%s" % "%s")  # [logging-not-lazy]
