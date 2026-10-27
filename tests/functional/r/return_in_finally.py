# pylint: disable=missing-docstring,too-few-public-methods,useless-return,lost-exception,inconsistent-return-statements

def second_favorite():
    fruits = ["apple"]
    try:
        return fruits[1]
    finally:
        return fruits[0]  # [return-in-finally]


def all_favorites():
    fruits = ["orange", "kiwi", "pineapple"]

    for fruit in fruits:
        try:
            return fruit
        finally:
            return  # [return-in-finally]


def more_favorites():
    fruits = ["orange", "kiwi", "pineapple"]

    for fruit in fruits:
        try:
            return fruit
        finally:
            if len(fruit) > 7:
                return "too many fruits"  # [return-in-finally]


def even_more_favorites():
    fruits = ["orange", "kiwi", "pineapple"]

    for fruit in fruits:
        try:
            return fruit
        finally:
            if len(fruit) > 7:
                for fruit_name in fruits:
                    return f"please remove {fruit_name}"  # [return-in-finally]


def callback_defined_in_finally():
    try:
        pass
    finally:
        def callback():
            return 1

        async def async_callback():
            return 2

        class Handler:
            def handle(self):
                return 3

        def callback_with_finally():
            try:
                pass
            finally:
                return 4  # [return-in-finally]

    return callback, async_callback, Handler, callback_with_finally


def nested_finally():
    try:
        pass
    finally:
        try:
            pass
        finally:
            return 1  # [return-in-finally]


def try_body_inside_finally():
    try:
        pass
    finally:
        try:
            return 1  # [return-in-finally]
        finally:
            pass
