# pylint: disable=missing-docstring, unreachable

ExceptionAlias = Exception

class CustomBroadException(Exception):
    pass


class CustomNarrowException(CustomBroadException):
    pass


def exploding_apple(apple):
    print(f"{apple} is about to explode")
    raise Exception("{apple} exploded !")  # [broad-exception-raised]


def raise_and_catch_star():
    try:
        raise Exception("Oh No!!")  # [broad-exception-raised]
    except* Exception as ex:  # [broad-exception-caught]
        print(ex)


def raise_catch_reraise_star():
    try:
        exploding_apple("apple")
    except* Exception as ex:
        print(ex)
        raise ex


def raise_catch_raise_star():
    try:
        exploding_apple("apple")
    except* Exception as ex:
        print(ex)
        raise Exception() from None  # [broad-exception-raised]


def raise_catch_raise_using_alias_star():
    try:
        exploding_apple("apple")
    except* Exception as ex:
        print(ex)
        raise ExceptionAlias() from None  # [broad-exception-raised]

raise Exception()  # [broad-exception-raised]
raise BaseException()  # [broad-exception-raised]
raise CustomBroadException()  # [broad-exception-raised]
raise IndexError from None
raise CustomNarrowException() from None
