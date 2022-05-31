"""If a function is not using any class attribute it can be a @staticmethod, or a function outside the class."""

def developer_greeting():
    print("Greetings developer!")


class Person:
    name = "Paris"

    def greeting_1(self):
        print(f"Hello from {self.name} !")

    @staticmethod
    def greeting_2():
        print("Hi!")
