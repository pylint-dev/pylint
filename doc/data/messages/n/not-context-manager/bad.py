class MyContextManager:
    def __enter__(self):
        pass


with MyContextManager() as c:  # [not-context-manager]
    pass
