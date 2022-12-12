"""Tests for used-before-assignment with python 3.10's pattern matching"""

match ("example", "one"):
    case (x, y) if x == "example":
        print("x used to cause used-before-assignment!")
    case _:
        print("good thing it doesn't now!")
