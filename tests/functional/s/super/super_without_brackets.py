"""Tests for super-without-brackets"""

# pylint: disable=missing-function-docstring, missing-class-docstring, too-few-public-methods


class Soup:
    @staticmethod
    def temp():
        print("Soup is hot!")


class TomatoSoup(Soup):
    @staticmethod
    def temp():
        super.temp()  # [super-without-brackets]
        print("But tomato soup is even hotter!")


class VegetableSoup(Soup):
    @staticmethod
    def temp():
        super().temp()
        print("But vegetable soup is even hotter!")
