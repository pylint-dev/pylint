"""Tests for logging-too-many-args"""
import logging

logging.error("constant string", 1, 2)  # [logging-too-many-args]
logging.error("{}", 1, 2)  # [logging-too-many-args]
logging.error("{0}", 1, 2)  # [logging-too-many-args]
logging.error("{}, {named}", 1, 2, {"named": 1})  # [logging-too-many-args]
logging.error("{0}, {named}", 1, 2, {"named": 1})  # [logging-too-many-args]
