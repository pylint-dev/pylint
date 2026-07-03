# pylint: disable=unused-argument, missing-docstring, line-too-long, too-few-public-methods
import enum


class Condiment(enum.Enum):
    CINAMON = 1
    SUGAR = 2

class Fruit:
    def brew(self, fruit_name: str):
        print(f"Brewing a fruit named {fruit_name}")

    def eat_with_condiment(self, fruit_name:str, condiment: Condiment):
        print(f"Eating a fruit named {fruit_name} with {condiment}")

class Orange(Fruit):
    def brew(self, orange_name: str): # [arguments-renamed]
        print(f"Brewing an orange named {orange_name}")

    def eat_with_condiment(self, orange_name: str, condiment: Condiment): #[arguments-renamed]
        print(f"Eating a fruit named {orange_name} with {condiment}")

class Banana(Fruit):
    def brew(self, fruit_name: bool): # No warning here
        print(f"Brewing a banana named {fruit_name}")

    def eat_with_condiment(self, fruit_name: str, condiment: Condiment, error: str): # [arguments-differ]
        print(f"Eating a fruit named {fruit_name} with {condiment}")

class Parent:

    def test(self, arg):
        return arg + 1

    def kwargs_test(self, arg, *, var1, var2):
        print(f"keyword parameters are {var1} and {var2}.")

class Child(Parent):

    def test(self, arg1): # [arguments-renamed]
        return arg1 + 1

    def kwargs_test(self, arg, *, value1, var2): #[arguments-differ]
        print(f"keyword parameters are {value1} and {var2}.")

class Child2(Parent):

    def test(self, var): # [arguments-renamed]
        return var + 1

    def kwargs_test(self, *, var1, kw2): #[arguments-differ]
        print(f"keyword parameters are {var1} and {kw2}.")

class ParentDefaults:

    def test1(self, arg, barg):
        print(f"Argument values are {arg} and {barg}")

    def test2(self, arg, barg):
        print(f"Argument values are {arg} and {barg}!")

    def test3(self, arg1, arg2):
        print(f"arguments: {arg1} {arg2}")

class ChildDefaults(ParentDefaults):

    def test1(self, arg, param2): # [arguments-renamed]
        print(f"Argument values are {arg} and {param2}")

    def test2(self, _arg, ignored_barg): # no error here
        print(f"Argument value is {_arg}")

    def test3(self, dummy_param, arg2): # no error here
        print(f"arguments: {arg2}")

# Check for crash on method definitions not at top level of class
# https://github.com/pylint-dev/pylint/issues/5648
class FruitConditional:

    define_eat = True

    def brew(self, fruit_name: str):
        print(f"Brewing a fruit named {fruit_name}")

    if define_eat:
        def eat_with_condiment(self, fruit_name:str, condiment: Condiment):
            print(f"Eating a fruit named {fruit_name} with {condiment}")

class FruitOverrideConditional(FruitConditional):

    fruit = "orange"
    override_condiment = True

    if fruit == "orange":
        def brew(self, orange_name: str): # [arguments-renamed]
            print(f"Brewing an orange named {orange_name}")

        if override_condiment:
            def eat_with_condiment(self, fruit_name: str, condiment: Condiment, error: str): # [arguments-differ]
                print(f"Eating a fruit named {fruit_name} with {condiment}")
