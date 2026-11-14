class Engine:
    def __init__(self):
        self.power = 100

    def start(self):
        pass


class Car:
    def __init__(self):
        self.engine = Engine()
        self.wheels = 4

    def drive(self):
        pass


class BreakdownError(Exception):
    pass
