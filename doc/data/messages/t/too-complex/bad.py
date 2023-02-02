def fifty_percent_off(whole):
    return (float(whole)) * 50 / 100


def calculate_sum_and_display_price_of_fruits(*fruits):  # [too-complex]
    # McCabe rating is 13 here (by default 10)
    shopping_list = []

    if "apple" in fruits:
        shopping_list.append(1.1)
    if "pear" in fruits:
        shopping_list.append(0.8)
    if "banana" in fruits:
        v = fifty_percent_off(1.2)
        shopping_list.append(v)
    if "mango" in fruits:
        v = fifty_percent_off(3.5)
        shopping_list.append(v)
    if "peach" in fruits:
        shopping_list.append(0.5)
    if "melon" in fruits:
        shopping_list.append(4.9)
    if "orange" in fruits:
        v = fifty_percent_off(2.0)
        shopping_list.append(v)
    if "strawberry" in fruits:
        shopping_list.append(2.5)
    if "mandarin" in fruits:
        shopping_list.append(2.3)
    if "plum" in fruits:
        shopping_list.append(0.5)
    if "watermelon" in fruits:
        v = fifty_percent_off(6.4)
        shopping_list.append(v)

    combine = zip(fruits, shopping_list)

    for i in combine:
        print(f"{i[0]} ${i[1]:.2f}")

    total = sum(shopping_list)
    print(f"Total: ${total:.2f}")


calculate_sum_and_display_price_of_fruits(
    "apple",
    "pear",
    "banana",
    "mango",
    "peach",
    "melon",
    "orange",
    "strawberry",
    "mandarin",
    "plum",
    "watermelon",
)