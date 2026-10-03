import random


class GenericAstrology:
    def __init__(self, signs, predictions):
        self.signs = signs
        self.predictions = predictions

    def __iter__(self):
        self.index = 0
        self.number_of_prediction = len(self.predictions)
        return self

    def __next__(self):
        if self.index == len(self.signs):
            raise StopIteration
        self.index += 1
        prediction_index = random.randint(0, self.number_of_prediction - 1)
        return self.signs[self.index - 1], self.predictions[prediction_index]


SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra"]
PREDICTIONS = ["good things", "bad thing", "existential dread"]
for sign, prediction in GenericAstrology(SIGNS, PREDICTIONS):
    print(f"{sign} : {prediction} today")
