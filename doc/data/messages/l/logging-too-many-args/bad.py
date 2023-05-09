import logging

try:
    function()
except Exception as e:
    logging.error("Error occurred: %s", type(e), e)  # [logging-too-many-args]
    raise
