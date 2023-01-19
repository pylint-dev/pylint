"""This should emit warnings when heuristic-exception-detection is enabled
"""
class NotClearlyAProblem(Exception):
    """ an exception class that isn't clearly named like one """
    purpose = "testing"

def ambiguous_method():
    """ instantiates NotClearlyAProblem, for unknown reasons """
    NotClearlyAProblem()
