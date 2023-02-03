def fifty_percent_off(whole):
    return (float(whole)) * 50 / 100


def calculate_sum_and_display_price_of_fruits(*fruits_to_buy):  # [too-complex]
    # McCabe rating is 13 here (by default 10)
    shopping_list = []

    if "apple" in fruits_to_buy:
        v = fifty_percent_off(1.1)
        shopping_list.append(v)
    if "pear" in fruits_to_buy:
        shopping_list.append(0.8)
    if "banana" in fruits_to_buy:
        shopping_list.append(1.2)
    if "mango" in fruits_to_buy:
        shopping_list.append(3.5)
    if "peach" in fruits_to_buy:
        shopping_list.append(0.5)
    if "melon" in fruits_to_buy:
        shopping_list.append(4.9)
    if "orange" in fruits_to_buy:
        v = fifty_percent_off(2.0)
        shopping_list.append(v)
    if "strawberry" in fruits_to_buy:
        shopping_list.append(2.5)
    if "mandarin" in fruits_to_buy:
        shopping_list.append(2.3)
    if "plum" in fruits_to_buy:
        shopping_list.append(0.5)
    if "watermelon" in fruits_to_buy:
        shopping_list.append(6.4)

    combine = zip(fruits_to_buy, shopping_list)

    for i in combine:
        print(f"{i[0]} ${i[1]:.2f}")

    total = sum(shopping_list)
    print(f"Total price is ${total:.2f}")


fruits_to_buy = ["apple", "orange"]
calculate_sum_and_display_price_of_fruits(*fruits_to_buy)