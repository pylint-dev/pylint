import random


class GenericAstrology:
    def __init__(self, signs, predictions):
        self.signs = signs
        self.predictions = predictions

    def __iter__(self):  # [non-iterator-returned]
        self.index = 0
        self.number_of_prediction = len(self.predictions)
        return self


SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra"]
PREDICTIONS = ["good things", "bad thing", "existential dread"]
for sign, prediction in GenericAstrology(SIGNS, PREDICTIONS):
    print(f"{sign} : {prediction} today")
