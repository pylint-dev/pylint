# split up to smaller functions

fruit = {
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


def fifty_percent_off(whole):
    return (float(whole)) * 50 / 100


discounted_fruit = ("banana", "mango", "orange", "watermelon")
shopping_list = []

for f, v in fruit.items():
    if f in discounted_fruit:
        PRICE = fifty_percent_off(v)
    else:
        PRICE = v
    shopping_list.append(PRICE)
    print(f"{f} ${PRICE:.2f}")

print(f"Total price is ${sum(shopping_list):.2f}")