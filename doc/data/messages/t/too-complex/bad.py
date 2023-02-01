fruit = {'apple': 1.1,
         'pear': 0.8,
         'banana': 1.2,
         'mango': 3.5,
         'peach': 0.5,
         'melon': 4.9,
         'orange': 2.0,
         'strawberry': 2.5,
         'mandarin': 2.3,
         'plum': 0.5,
         'watermelon': 6.4
         }

discounted_fruit = ('banana', 'mango', 'orange', 'watermelon')
shopping_list = []


def fifty_percent_off(whole):
    return (float(whole)) * 50 / 100


for f, v in fruit.items():  # [too-complex]
    # McCabe rating is 13 here (by default 10)
    if f == 'apple':
        shopping_list.append(v)
    if f == 'pear':
        shopping_list.append(v)
    if f == 'banana':
        v = fifty_percent_off(v)
        shopping_list.append(v)
    if f == 'mango':
        v = fifty_percent_off(v)
        shopping_list.append(v)
    if f == 'peach':
        shopping_list.append(v)
    if f == 'melon':
        shopping_list.append(v)
    if f == 'orange':
        v = fifty_percent_off(v)
        shopping_list.append(v)
    if f == 'strawberry':
        shopping_list.append(v)
    if f == 'mandarin':
        shopping_list.append(v)
    if f == 'plum':
        shopping_list.append(v)
    if f == 'watermelon':
        v = fifty_percent_off(v)
        shopping_list.append(v)

    print(f'{f} ${v:.2f}')

total = sum(shopping_list)
print(f'Total: ${total:.2f}')