def f():
    raise OSError("error 1")


try:
    f()
except OSError as e:
    print("There were OSErrors")
except SystemError as e:
    print("There were SystemErrors")
