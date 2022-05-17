def fruits_to_string():
    fruits = {"apple", "pear", "peach"}
    formatted_fruit = ""
    for fruit in fruits:
        formatted_fruit += fruit  # [consider-using-join]
    return formatted_fruit
