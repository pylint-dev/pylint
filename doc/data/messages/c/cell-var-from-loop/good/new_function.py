def greet(name):
    print(f"Hello, {name}!")


def teacher_greeting(names):
    for name in names:
        greet(name)


teacher_greeting(["Graham", "John", "Terry", "Eric", "Terry", "Michael"])

