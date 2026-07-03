import subprocess


def foo():
    pass


subprocess.Popen(preexec_fn=foo)  # [subprocess-popen-preexec-fn]
