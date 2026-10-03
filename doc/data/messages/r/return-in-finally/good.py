def second_favorite():
    fruits = ["kiwi", "pineapple"]
    try:
        return fruits[1]
    except KeyError:
        ...

    return fruits[0]
