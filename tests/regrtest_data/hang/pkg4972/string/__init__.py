import string
import pkg4972.string  # self-import necessary

class Fake(string.Formatter):
    pass

string.Formatter = Fake
