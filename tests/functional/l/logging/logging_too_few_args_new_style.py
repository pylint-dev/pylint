"""Tests for logging-too-few-args new style"""

import logging

logging.error("{}, {}", 1)  # [logging-too-few-args]
logging.error("{0}, {1}", 1)  # [logging-too-few-args]
logging.error("{}")  # [logging-too-few-args]
logging.error("{0}")  # [logging-too-few-args]
logging.error("{named}")  # [logging-too-few-args]
logging.error("{named1}, {named2}", {"named1": 1})  # [logging-too-few-args]
logging.error("{0}, {named}", 1)  # [logging-too-few-args]
logging.error("{}, {named}", {"named": 1})  # [logging-too-few-args]
logging.error("{0}, {named}", {"named": 1})  # [logging-too-few-args]
