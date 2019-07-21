# pylint: disable=missing-docstring,no-member,deprecated-method,invalid-name

# Muck up the names in an effort to confuse...
import logging as renamed_logging
import os as logging

var = "123"
var_name = 'Var:'
# Statements that should be flagged:
renamed_logging.warn('%s, %s' % (4, 5))             # [logging-not-lazy]
renamed_logging.exception('%s' % 'Exceptional!')    # [logging-not-lazy]
renamed_logging.log(renamed_logging.INFO, 'msg: %s' % 'Run!')  # [logging-not-lazy]
renamed_logging.log(renamed_logging.INFO, "Var: " + var)  # [logging-not-lazy]
renamed_logging.warn('%s' + ' the rest of a single string') # [logging-not-lazy]
renamed_logging.log(renamed_logging.INFO, var_name + var) # [logging-not-lazy]

var_name = 'Var:'
# Statements that should not be flagged:
renamed_logging.warn('%s, %s', 4, 5)
renamed_logging.log(renamed_logging.INFO, 'msg: %s', 'Run!')
logging.warn('%s, %s' % (4, 5))
logging.log(logging.INFO, 'msg: %s' % 'Run!')
logging.log("Var: " + var)
