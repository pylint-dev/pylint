"""Test logging-format-interpolation for Python 3.6"""
import logging as renamed_logging


renamed_logging.info(f'Read {renamed_logging} from globals')  # [logging-fstring-interpolation]
