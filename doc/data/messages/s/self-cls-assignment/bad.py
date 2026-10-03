class Fruit:
    @classmethod
    def list_fruits(cls):
        cls = "apple"  # [self-cls-assignment]

    def print_color(self, *colors):
        self = "red"  # [self-cls-assignment]
        color = colors[1]
        print(color)
