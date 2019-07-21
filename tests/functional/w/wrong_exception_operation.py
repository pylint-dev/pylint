# pylint: disable=missing-docstring, superfluous-parens


try:
    1/0
except (ValueError | TypeError): # [wrong-exception-operation]
    pass

try:
    1/0
except (ValueError + TypeError): # [wrong-exception-operation]
    pass


try:
    1/0
except (ValueError < TypeError): # [wrong-exception-operation]
    pass
