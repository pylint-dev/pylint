class InstanceAttributes:
    def __init__(self):
        self.my_int_without_type_hint = 1
        self.my_int_with_type_hint: int = 2
        self.my_optional_int: int = None
