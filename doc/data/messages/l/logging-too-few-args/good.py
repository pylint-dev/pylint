import logging

try:
    function()
except Exception as e:
    logging.error('%s error occured: %s', type(e), e)
    raise
