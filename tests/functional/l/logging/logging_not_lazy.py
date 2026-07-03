"""Tests for logging-not-lazy"""
# pylint: disable=missing-docstring,no-member,deprecated-method,invalid-name, consider-using-f-string

# Muck up the names in an effort to confuse...
import logging as renamed_logging
import os as logging

var = "123"
var_name = "Var:"
# Statements that should be flagged:
renamed_logging.warn("%s, %s" % (4, 5))  # [logging-not-lazy]
renamed_logging.warn("Var: " + var)  # [logging-not-lazy]
renamed_logging.exception("%s" % "Exceptional!")  # [logging-not-lazy]
renamed_logging.log(renamed_logging.INFO, "msg: %s" % "Run!")  # [logging-not-lazy]
renamed_logging.log(renamed_logging.INFO, "Var: " + var)  # [logging-not-lazy]
renamed_logging.log(renamed_logging.INFO, var_name + var)  # [logging-not-lazy]

# Statements that should not be flagged:
renamed_logging.warn("%s, %s", 4, 5)
renamed_logging.log(renamed_logging.INFO, "msg: %s", "Run!")
logging.warn("%s, %s" % (4, 5))
logging.log(logging.INFO, "msg: %s" % "Run!")
logging.log("Var: " + var)
# Explicit string concatenations are fine:
renamed_logging.warn("%s" + " the rest of a single string")
renamed_logging.warn("Msg: " + "%s", "first piece " + "second piece")
renamed_logging.warn("first" + "second" + "third %s", "parameter")
renamed_logging.warn(("first" + "second" + "third %s"))

# Regression crash test for incorrect format call
renamed_logging.error(
    "0} - {1}".format(1, 2)  # [bad-format-string, logging-format-interpolation]
)
