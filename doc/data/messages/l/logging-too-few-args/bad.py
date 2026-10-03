import logging

try:
    function()
except Exception as e:
    logging.error("%s error occurred: %s", e)  # [logging-too-few-args]
    raise
