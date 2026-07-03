class Fruit:
    COLORS = []

    def __init__(self, color):
        self.color = color

    def pick_colors(cls, *args):
        """classmethod to pick fruit colors"""
        cls.COLORS = args

    pick_colors = classmethod(pick_colors)  # [no-classmethod-decorator]
