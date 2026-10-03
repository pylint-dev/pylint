# pylint: disable=disallowed-name,no-value-for-parameter,missing-docstring

import subprocess


subprocess.run() # [subprocess-run-check]
subprocess.run(["ls"], check=True)
subprocess.run(["ls"], **{"check": True})
subprocess.run(["ls"], **{"text": True})  # [subprocess-run-check]
subprocess.run(["ls"], **{})  # [subprocess-run-check]
subprocess.run(*["ls"])  # [subprocess-run-check]


def run_with_forwarded_kwargs(cmd, **kwargs):
    return subprocess.run(cmd, **kwargs)


def run_with_opaque_options(cmd, options):
    return subprocess.run(cmd, **options)


def run_with_extra_options(cmd, options):
    return subprocess.run(cmd, **{"text": True, **options})


def run_with_variable_key(cmd, key):
    return subprocess.run(cmd, **{key: True})
