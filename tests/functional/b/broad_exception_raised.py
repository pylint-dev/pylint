# pylint: disable=missing-module-docstring, missing-function-docstring, unreachable

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
raise IndexError from None
