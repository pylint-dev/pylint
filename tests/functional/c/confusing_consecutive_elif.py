# pylint: disable=missing-module-docstring, missing-function-docstring

def check_config(machine, old_conf, new_conf):
    if old_conf:
        if not new_conf:
            machine.disable()
        elif old_conf.value != new_conf.value:
            machine.disable()
            machine.enable(new_conf.value)
    elif new_conf:  # [confusing-consecutive-elif]
        machine.enable(new_conf.value)
