class MyContextManager:
    def __enter__(self):
        pass

    def __exit__(self, *exc):
        pass


with MyContextManager() as c:
    pass
