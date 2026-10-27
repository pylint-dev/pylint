# pylint: disable=disallowed-name,no-value-for-parameter,missing-docstring,undefined-variable

import subprocess


subprocess.run() # [subprocess-run-check]
subprocess.run(["ls"], check=True)

# ``check`` can be passed by unpacking a dict, as long as every possible dict defines it
RUN_KWARGS = {"check": True}
subprocess.run(["ls"], **RUN_KWARGS)
subprocess.run(["ls"], **{"check": False, "text": True})
subprocess.run(["ls"], **{"text": True}) # [subprocess-run-check]
subprocess.run(["ls"], **UNKNOWN_KWARGS) # [subprocess-run-check]


def run_conditionally(command, checked):
    if checked:
        run_kwargs = {"check": True}
    else:
        run_kwargs = {"capture_output": True}
    return subprocess.run(command, **run_kwargs) # [subprocess-run-check]


def run_with_options(command, options):
    return subprocess.run(command, **options) # [subprocess-run-check]
