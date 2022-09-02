"""Logging warnings using a logger class."""
# pylint: disable=consider-using-f-string
from __future__ import absolute_import
import logging


LOG = logging.getLogger("domain")
LOG.debug("%s" % "junk")  # [logging-not-lazy]
LOG.log(logging.DEBUG, "%s" % "junk")  # [logging-not-lazy]
LOG2 = LOG.debug
LOG2("%s" % "junk")  # [logging-not-lazy]

logging.getLogger("domain").debug("%s" % "junk")  # [logging-not-lazy]
