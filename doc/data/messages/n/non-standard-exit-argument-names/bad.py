class Resource:
    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):  # [non-standard-exit-argument-names]
        pass
