def foo(numbers):
    for i in numbers:
        def bar():
            print(i)  # [cell-var-from-loop]
        bar()
