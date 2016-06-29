# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING


import enum


_Stage = enum.Enum('Stage', 'CORE PEDANTIC REFACTORING STYLE ADDITIONAL')
# pylint: disable=no-member; github.com/pycqa/pylint/issues/690
CORE = _Stage.CORE
PEDANTIC = _Stage.PEDANTIC
REFACTORING = _Stage.REFACTORING
STYLE = _Stage.STYLE
ADDITIONAL = _Stage.ADDITIONAL
del _Stage


def next_stage(stage_step):
    """Get the next stage from the given one or None, if there is no next one."""
    stages = list(type(stage_step))
    try:
        index = stages.index(stage_step)
        return stages[index + 1]
    except (IndexError, ValueError):
        # We are at the end of the stages or th stage step was
        # too big.
        return None