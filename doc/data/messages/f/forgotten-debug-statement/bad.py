import pdb


def find_the_treasure(clues):
    for clue in clues:
        pdb.set_trace() # [forgotten-debug-statement]
        if "treasure" in clue:
            return True
    return False

treasure_hunt = ["Dead Man's Chest", "X marks the spot", "The treasure is buried near the palm tree"]
find_the_treasure(treasure_hunt)
