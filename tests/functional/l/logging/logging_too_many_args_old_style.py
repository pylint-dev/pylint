"""Tests for logging-too-many-args using logging-format-style=old
for both new style and old style."""
import logging

logging.error("constant string", 1, 2)  # [logging-too-many-args]
logging.error("{}", 1, 2)  # [logging-too-many-args]
logging.error("{0}", 1, 2)  # [logging-too-many-args]
logging.error("{}, {named}", 1, 2, {"named": 1})  # [logging-too-many-args]
logging.error("{0}, {named}", 1, 2, {"named": 1})  # [logging-too-many-args]
# Regression test for https://github.com/pylint-dev/pylint/issues/9118
# This is a false positive currently
logging.warning( "The frequency is: {:.2f} MHz", 2.3 )  # [logging-too-many-args]

logging.error("constant string", 1, 2)  # [logging-too-many-args]
logging.error("%s", 1, 2)  # [logging-too-many-args]
logging.error("%s", 1, 2)  # [logging-too-many-args]
logging.error("%s, {named}", 1, 2, {"named": 1})  # [logging-too-many-args]
logging.error("%s, {named}", 1, 2, {"named": 1})  # [logging-too-many-args]
# Regression test for https://github.com/pylint-dev/pylint/issues/9118
logging.warning( "The frequency is: %f MHz", 2.3 )
