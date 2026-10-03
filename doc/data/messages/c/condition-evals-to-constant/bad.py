def is_a_fruit(fruit):
    return bool(fruit in {"apple", "orange"} or True)  # [condition-evals-to-constant]
