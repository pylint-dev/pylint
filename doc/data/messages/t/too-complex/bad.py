def fifty_percent_off(whole):
    return (float(whole)) * 50 / 100


def calculate_sum_and_display_price_of_fruits(*fruits):  # [too-complex]
    # McCabe rating is 13 here (by default 10)
    shopping_list = []

    if "apple" in fruits:
        v = fifty_percent_off(1.1)
        shopping_list.append(v)
    if "pear" in fruits:
        shopping_list.append(0.8)
    if "banana" in fruits:
        shopping_list.append(1.2)
    if "mango" in fruits:
        shopping_list.append(3.5)
    if "peach" in fruits:
        shopping_list.append(0.5)
    if "melon" in fruits:
        shopping_list.append(4.9)
    if "orange" in fruits:
        shopping_list.append(2.0)
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
    print(f"Total price is ${total:.2f}")


fruits_to_buy = ["apple", "orange", "watermelon"]
calculate_sum_and_display_price_of_fruits(*fruits_to_buy)
