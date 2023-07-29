class cat:  # [invalid-name]
    def Meow(self, NUMBER_OF_MEOW):  # [invalid-name, invalid-name]
        print("Meow" * NUMBER_OF_MEOW)
        return NUMBER_OF_MEOW


Cat = cat().Meow(42)  # [invalid-name]
