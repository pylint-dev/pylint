def teacher(names):
    for name in names:

        def greet():
            print(f"Hello, {name}!")  # [cell-var-from-loop]

        greet()
