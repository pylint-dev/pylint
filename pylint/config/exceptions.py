# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt


class UnrecognizedArgumentAction(Exception):
    """Raised if an ArgumentManager instance tries to add an argument for which the action
    is not recognized.
    """


class ArgumentPreprocessingError(Exception):
    """Raised if an error occurs during argument preprocessing."""
