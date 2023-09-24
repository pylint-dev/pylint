def teacher_greeting(names):
    greetings = []
    for name in names:

        def greet():
            # do something
            print(f"Hello, {name}!")  # [cell-var-from-loop]

        if name.isalpha():
            greetings.append(greet)

    for greet in greetings:
        # the "name" variable is evaluated when the function is called here,
        # which is the last value it had in the loop - "Not-A-Name"
        greet()


teacher_greeting(["Graham", "John", "Terry", "Eric", "Terry", "Michael"])
# "Hello, Michael!"
# "Hello, Michael!"
# "Hello, Michael!"
# "Hello, Michael!"
# "Hello, Michael!"
