def teacher_greeting(names):
    greetings = (lambda: print(f"Hello, {name}!") for name in names)
    for greet in greetings:
        greet()


teacher_greeting(["First", "Second", "Third"])
