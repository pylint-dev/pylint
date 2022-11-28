"""Tests for logging-fstring-interpolation with f-strings"""
import logging

VAR = "string"
logging.error(f"{VAR}")  # [logging-fstring-interpolation]

WORLD = "world"
logging.error(f'Hello {WORLD}')  # [logging-fstring-interpolation]

logging.error(f'Hello %s', 'World!')  # [f-string-without-interpolation]
logging.error(f'Hello %d', 1)  # [f-string-without-interpolation]
