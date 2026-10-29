"""``exit``/``quit`` bound in an enclosing function scope are not the site builtins."""
# pylint: disable=missing-function-docstring,import-outside-toplevel,redefined-builtin


def imported_in_enclosing_function():
    from sys import exit

    def inner():
        exit(0)

    return inner


def assigned_in_enclosing_function():
    import sys

    quit = sys.exit

    def inner():
        quit(0)

    inner()
    quit(1)


def defined_in_enclosing_function():
    def exit(code):
        return code

    def inner():
        return exit(0)

    return inner


def builtin_from_nested_function():
    def inner():
        exit(0)  # [consider-using-sys-exit]

    return inner


def exit_imported_but_quit_called(code):
    from sys import exit

    if code:
        exit(code)
    quit()  # [consider-using-sys-exit]
