import logging

try:
    function()
except Exception as e:
    logging.error('Error occurred: %s', e)
    raise
