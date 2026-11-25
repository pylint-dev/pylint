# pylint: disable=missing-docstring,invalid-name,disallowed-name,unused-variable
# pylint: disable=missing-function-docstring,too-few-public-methods,unnecessary-pass

"""Regression test for https://github.com/pylint-dev/pylint/issues/7470."""


def function_a() -> None:
    pass


def function_b() -> None:
    pass


def in_different_cases(choice: str) -> None:
    match choice:
        case "a":
            function = function_a
        case "b":

            def function() -> None:
                pass

        case "c":
            function = function_b
    function()


def in_different_cases_reported_in_issue(choice: object) -> None:
    match choice:
        case None:

            def f():
                return 1

        case str():

            def f():
                return "1"

    f()


def classes_in_different_cases(choice: int) -> None:
    match choice:
        case 1:

            class C:
                pass

        case 2:

            class C:
                pass

    C()


def twice_in_the_same_case(choice: int) -> None:
    match choice:
        case 1:
            def f():
                return 1

            def f():  # [function-redefined]
                return 2

    f()


def nested_in_different_cases(choice: int, flag: bool) -> None:
    match choice:
        case 1:
            if flag:

                def f():
                    return 1

        case 2:

            def f():
                return 2

    f()


def assignment_outside_a_case(flag: int) -> None:
    name = 1

    match flag:
        case 1:
            def name():  # [function-redefined]
                return 2

    name()
