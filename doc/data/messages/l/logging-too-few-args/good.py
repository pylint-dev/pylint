import logging

try:
    function()
except Exception as e:
    logging.error("%s error occurred: %s", type(e), e)
    raise
