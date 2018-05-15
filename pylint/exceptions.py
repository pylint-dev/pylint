# -*- coding: utf-8 -*-
# Copyright (c) 2016-2017 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016 Glenn Matthews <glenn@e-dad.net>
# Copyright (c) 2017 Łukasz Rogalski <rogalski.91@gmail.com>
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Exception classes raised by various operations within pylint."""


class InvalidMessageError(Exception):
    """raised when a message creation, registration or addition is rejected"""

class UnknownMessageError(Exception):
    """raised when a unregistered message id is encountered"""

class EmptyReportError(Exception):
    """raised when a report is empty and so should not be displayed"""

class InvalidReporterError(Exception):
    """raised when selected reporter is invalid (e.g. not found)"""
