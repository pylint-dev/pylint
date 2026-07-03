def fruits_to_string(fruits):
    formatted_fruit = ""
    for fruit in fruits:
        formatted_fruit += fruit  # [consider-using-join]
    return formatted_fruit


print(fruits_to_string(["apple", "pear", "peach"]))
