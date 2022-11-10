# pylint: disable=missing-docstring, unreachable

class CustomBroadException(Exception):
    pass


class CustomNarrowException(CustomBroadException):
    pass


def exploding_apple(apple):
    print(f"{apple} is about to explode")
    raise Exception("{apple} exploded !")  # [broad-exception-raised]


def raise_and_catch():
    try:
        raise Exception("Oh No!!")  # [broad-exception-raised]
    except Exception as ex:  # [broad-exception-caught]
        print(ex)

raise Exception()  # [broad-exception-raised]
raise BaseException()  # [broad-exception-raised]
raise CustomBroadException()  # [broad-exception-raised]
raise IndexError from None
raise CustomNarrowException() from None
