def teacher_greeting(names):
    def greet(name):
        # do something
        print(f"Hello, {name}!")

    for name in names:
        if name.isalpha():
            # we're passing the value of "name" to the function here
            greet(name)


teacher_greeting(["Graham", "John", "Eric", "Terry", "Michael", "Not-A-Name"])
# "Hello, Graham!"
# "Hello, John!"
# "Hello, Eric!"
# "Hello, Terry!"
# "Hello, Michael!"
