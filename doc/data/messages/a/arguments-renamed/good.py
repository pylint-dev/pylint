class Fruit:
    def brew(self, ingredient_name: str):
        print(f"Brewing a {type(self)} with {ingredient_name}")


class Apple(Fruit): ...


class Orange(Fruit):
    def brew(self, ingredient_name: str):
        print(f"Brewing an orange with {ingredient_name}")


for fruit, ingredient_name in [[Orange(), "thyme"], [Apple(), "cinnamon"]]:
    fruit.brew(ingredient_name=ingredient_name)
