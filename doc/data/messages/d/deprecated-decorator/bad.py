import abc


class Animal:
    @abc.abstractclassmethod  # [deprecated-decorator]
    def breath(cls):
        pass
