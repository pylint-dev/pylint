class Fruit:
    def brew(self, ingredient_name: str):
        print(f"Brewing a {type(self)} with {ingredient_name}")


class Apple(Fruit): ...


class Orange(Fruit):
    def brew(self, flavor: str):  # [arguments-renamed]
        print(f"Brewing an orange with {flavor}")


for fruit, ingredient_name in [[Orange(), "thyme"], [Apple(), "cinnamon"]]:
    fruit.brew(ingredient_name=ingredient_name)
