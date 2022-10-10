# pylint: disable=missing-docstring

import graphlib
from graphlib import TopologicalSorter

def example(
    sorter1: "graphlib.TopologicalSorter[int]",
    sorter2: "TopologicalSorter[str]",
) -> None:
    """unused-import shouldn't be emitted for graphlib or TopologicalSorter."""
    print(sorter1, sorter2)
