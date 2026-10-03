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
