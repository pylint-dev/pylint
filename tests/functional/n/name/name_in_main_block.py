"""Names assigned in an ``if __name__ == "__main__":`` block read like a script
body, so they may follow either the constant or the variable naming style."""
# pylint: disable=missing-function-docstring
import sys


def main() -> int:
    return 0


MODULE_CONST = 1
module_var = 2  # [invalid-name]


if __name__ == "__main__":
    exit_code = main()  # variable style is accepted
    EXIT_CODE = main()  # constant style is accepted
    BadMix = main()  # [invalid-name]
    unused_returnCode = main()  # [invalid-name]
    if sys.argv[1:]:
        exclusively_assigned = main()  # exclusive assignments read as a constant
    else:
        exclusively_assigned = 0
    sys.exit(exit_code or EXIT_CODE or BadMix or exclusively_assigned)
else:
    # The ``else`` branch runs on import, so it keeps the constant naming style.
    imported_flag = main()  # [invalid-name]
