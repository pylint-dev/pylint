fruit_prices = {
    "apple": 1.1,
    "pear": 0.8,
    "banana": 1.2,
    "mango": 3.5,
    "peach": 0.5,
    "melon": 4.9,
    "orange": 2.0,
    "strawberry": 2.5,
    "mandarin": 2.3,
    "plum": 0.5,
    "watermelon": 6.4,
}
discounted_fruits = ["apple", "watermelon"]


def fifty_percent_off(whole):
    return (float(whole)) * 50 / 100


def get_price(fruit):
    full_price = fruit_prices.get(fruit)
    if fruit in discounted_fruits:
        return fifty_percent_off(full_price)
    else:
        return full_price


def display_fruit_and_price(fruits):
    for fruit in fruits:
        price = get_price(fruit)
        print(f"{fruit} ${price :.2f}")


def get_total(fruits):
    return sum(get_price(f) for f in fruits)


fruits_to_buy = ["apple", "orange", "watermelon"]
display_fruit_and_price(fruits_to_buy)
print(f"Total price is ${get_total(fruits_to_buy):.2f}")
