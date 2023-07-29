class Cat:
    def meow(self, number_of_meow):
        print("Meow" * number_of_meow)
        return number_of_meow


CAT = Cat().meow(42)
