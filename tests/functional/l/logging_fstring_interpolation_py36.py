"""Test logging-fstring-interpolation for Python 3.6"""
# pylint: disable=invalid-name

from datetime import datetime

import logging as renamed_logging


local_var_1 = 4
local_var_2 = "run!"

pi = 3.14159265

may_14 = datetime(year=2018, month=5, day=14)

# Statements that should be flagged:
renamed_logging.debug(f'{local_var_1} {local_var_2}') # [logging-fstring-interpolation]
renamed_logging.log(renamed_logging.DEBUG, f'msg: {local_var_2}') # [logging-fstring-interpolation]
renamed_logging.log(renamed_logging.DEBUG, f'pi: {pi:.3f}') # [logging-fstring-interpolation]
renamed_logging.info(f"{local_var_2.upper()}") # [logging-fstring-interpolation]
renamed_logging.info(f"{may_14:'%b %d: %Y'}") # [logging-fstring-interpolation]
