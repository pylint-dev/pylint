"""Tests for logging-format-interpolation with logging-format-style=new"""

import logging

logging.error("constant string")
logging.error("{}")
logging.error("{}", 1)
logging.error("{0}", 1)
logging.error("{named}", {"named": 1})
logging.error("{} {named}", 1, {"named": 1})
logging.error("{0} {named}", 1, {"named": 1})
