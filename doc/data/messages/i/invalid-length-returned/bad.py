class Foo:
    def __len__(self):  # [invalid-length-returned]
        return -1
