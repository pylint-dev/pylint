"""Names assigned in an ``if __name__ == "__main__":`` block read like a script
body, so they may follow either the constant or the variable naming style."""
# pylint: disable=missing-function-docstring


def main() -> int:
    return 0


MODULE_CONST = 1
module_var = 2  # [invalid-name]


if __name__ == "__main__":
    exit_code = main()  # variable style is accepted
    EXIT_CODE = main()  # constant style is accepted
    BadMix = main()  # [invalid-name]
    raise SystemExit(exit_code or EXIT_CODE or BadMix)
