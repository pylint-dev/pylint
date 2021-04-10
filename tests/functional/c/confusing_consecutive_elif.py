# pylint: disable=missing-module-docstring, missing-function-docstring

def check_config(machine, old_conf, new_conf):
    """Example code that will trigger the message"""
    if old_conf:
        if not new_conf:
            machine.disable()
        elif old_conf.value != new_conf.value:
            machine.disable()
            machine.enable(new_conf.value)
    elif new_conf:  # [confusing-consecutive-elif]
        machine.enable(new_conf.value)


def check_config_2(machine, old_conf, new_conf):
    """Example code must not trigger the message, because the inner block ends with else."""
    if old_conf:
        if not new_conf:
            machine.disable()
        elif old_conf.value != new_conf.value:
            machine.disable()
            machine.enable(new_conf.value)
        else:
            pass
    elif new_conf:
        machine.enable(new_conf.value)

def check_config_3(machine, old_conf, new_conf):
    """
    Example code must not trigger the message,
    because the inner if is not the final node of the body.
    """
    if old_conf:
        if not new_conf:
            machine.disable()
        elif old_conf.value != new_conf.value:
            machine.disable()
            machine.enable(new_conf.value)
        print("Processed old configuration...")
    elif new_conf:
        machine.enable(new_conf.value)
