class Soup:
    @staticmethod
    def temp():
        print("Soup is hot!")


class TomatoSoup(Soup):
    @staticmethod
    def temp():
        super().temp()
        print("But tomato soup is even hotter!")
