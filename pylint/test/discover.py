#!/usr/bin/python
import os
from contextlib import contextmanager
from cProfile import Profile
from unittest import TestProgram


@contextmanager
def profiling(profile):
    profile.enable()
    yield
    profile.disable()


if __name__ == '__main__':
    profile = Profile()
    start_directory = os.path.dirname(os.path.realpath(__file__))
    pattern = '*test_*.py'
    with profiling(profile):
        TestProgram(module=None, argv=[
            'python -m unittest', 'discover',
            '-s', start_directory, '-p', pattern],
            exit=False)
    fname = os.path.expanduser(
        os.environ.get('PYLINT_STATS', '~/pylint.stats'))
    profile.dump_stats(fname)
