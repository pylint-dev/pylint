"""Minimal code to reproduce PyLint bug around infered, ignored, no-member."""
import logging
import os


class MyVeryOwnError(ValueError):
    """My Exception class."""
    node = True


def main():
    """Have main code in here so that PyLint does not pick on global vars."""
    # Use the environment to create a var (owner) that can be one of two types.
    if os.getenv('CAT') == 'dead':
        owner = ValueError('dead')
    else:
        owner = MyVeryOwnError('alive')
    if os.getenv('CAT') != 'dead':
        # In here although owner can only be of type MyVeryOwnError, PyLint
        # won't detect it and will infer it to be either a ValueError or a
        # MyVeryOwnError instance.
        logging.info(owner.node)
