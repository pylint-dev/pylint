from pathlib import Path

directories = Path(".").parents


class Cat:
    def meow(self):
        print("Meow")


Cat().meow()
