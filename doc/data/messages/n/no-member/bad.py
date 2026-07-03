from pathlib import Path

directories = Path(".").mothers  # [no-member]


class Cat:
    def meow(self):
        print("Meow")


Cat().roar()  # [no-member]
