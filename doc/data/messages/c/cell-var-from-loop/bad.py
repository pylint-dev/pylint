def teacher_greeting(names):
    for name in names:

        def greet():
            print(f"Hello, {name}!")  # [cell-var-from-loop]

        greet()


teacher_greeting(["Graham", "John", "Terry", "Eric", "Terry", "Michael"])
