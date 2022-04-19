class Soup:
    @staticmethod
    def temp():
        print("Soup is hot!")


class TomatoSoup(Soup):
    @staticmethod
    def temp():
        super.temp()  # [super-without-brackets]
        print("But tomato soup is even hotter!")
