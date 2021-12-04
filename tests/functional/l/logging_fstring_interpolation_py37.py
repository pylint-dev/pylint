"""Tests for logging-fstring-interpolation with f-strings"""
import logging

VAR = "string"
logging.error(f"{VAR}")  # [logging-fstring-interpolation]
