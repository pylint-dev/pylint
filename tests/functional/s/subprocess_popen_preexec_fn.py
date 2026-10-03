# pylint: disable=disallowed-name,no-value-for-parameter,missing-docstring,consider-using-with

import subprocess

def foo():
    pass


subprocess.Popen(preexec_fn=foo) # [subprocess-popen-preexec-fn]

subprocess.Popen()
