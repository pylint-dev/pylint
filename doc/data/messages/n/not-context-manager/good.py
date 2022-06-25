class Ctx:
    def __enter__(self):
        pass

    def __exit__(self, *exc):
        pass


with Ctx() as ctx:
    pass
