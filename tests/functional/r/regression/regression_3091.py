# pylint: disable=too-few-public-methods,invalid-name,missing-docstring,unnecessary-lambda-assignment
class MyClass():
    fun = lambda self, x: x * 2
    def __init__(self):
        x = self.fun(1) # Crashes pylint 2.3.1
        print(x)
