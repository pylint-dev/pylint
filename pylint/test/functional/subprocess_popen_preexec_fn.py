# pylint: disable=blacklisted-name,no-value-for-parameter,missing-docstring

import subprocess

def foo():
    pass


subprocess.Popen(preexec_fn=foo) # [subprocess-popen-preexec-fn]

subprocess.Popen()
