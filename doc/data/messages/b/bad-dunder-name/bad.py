class Apples:
    def _init_(self):  # [bad-dunder-name]
        pass

    def __hello__(self):  # [bad-dunder-name]
        print("hello")
