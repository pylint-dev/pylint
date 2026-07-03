var = 1


def foo():
    global var  # [global-statement]
    var = 10
    print(var)


foo()
print(var)
