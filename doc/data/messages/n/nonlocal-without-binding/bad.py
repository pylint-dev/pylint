class Fruit:
    def get_color(self):
        nonlocal colors  # [nonlocal-without-binding]
