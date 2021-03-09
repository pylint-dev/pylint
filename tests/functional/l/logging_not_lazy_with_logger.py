"""Logging warnings using a logger class."""
from __future__ import absolute_import
import logging

__revision__ = ''

LOG = logging.getLogger("domain")
LOG.debug("%s" % "junk")  # [logging-not-lazy]
LOG.log(logging.DEBUG, "%s" % "junk")  # [logging-not-lazy]
LOG2 = LOG.debug
LOG2("%s" % "junk")  # [logging-not-lazy]

logging.getLogger("domain").debug("%s" % "junk")  # [logging-not-lazy]
