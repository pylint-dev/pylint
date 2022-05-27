import logging

try:
    function()
except Exception as e:
    logging.error('Error occured: %s', e)
    raise
