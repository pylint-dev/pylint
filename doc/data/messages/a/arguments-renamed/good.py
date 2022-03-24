class Fruit:
    def brew(self, fruit_name: str):
        print(f"Brewing a fruit named {fruit_name}")


class Orange(Fruit):
    def brew(self, fruit_name: str):
        print(f"Brewing an orange named {fruit_name}")
