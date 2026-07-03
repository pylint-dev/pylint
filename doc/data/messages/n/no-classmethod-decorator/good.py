class Fruit:
    COLORS = []

    def __init__(self, color):
        self.color = color

    @classmethod
    def pick_colors(cls, *args):
        """classmethod to pick fruit colors"""
        cls.COLORS = args
