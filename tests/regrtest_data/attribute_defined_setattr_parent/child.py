from parent import Parent


class Child(Parent):
    def set_fruit(self):
        setattr(self, "fruit", 2)
