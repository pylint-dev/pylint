"""used-before-assignment cases in matching"""

match 4:
    case a if a in {2, 4, 6}:   # [used-before-assignment]
        pass


match ("example", "one"):
    case (x, y) if x == "example":  # [used-before-assignment]
        pass
