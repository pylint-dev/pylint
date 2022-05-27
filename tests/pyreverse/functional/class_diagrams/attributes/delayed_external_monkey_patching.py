from _monkey import Monkey


class Tree:
    def __init__(self):
        self.number_of_bananas = 5
        self.inhabitant = Monkey(
            "Steve"
        )  # This will trigger the evaluation of `monkey.py`
