def second_favorite():
    fruits = ["kiwi", "pineapple"]
    try:
        return fruits[1]
    finally:
        # because of this `return` statement, this function will always return "kiwi"
        return fruits[0]  # [return-in-finally]
