class Ctx:
    def __enter__(self):
        pass


with Ctx() as ctx:  # [not-context-manager]
    pass
