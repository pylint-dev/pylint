class Shape:
    def __init__(self):
        self.shape = True

class Rectangle(Shape):
    def __init__(self):
        super().__init__()
        self.rectangle = True

class Square(Rectangle):
    def __init__(self):
        super().__init__()
        self.square = True
