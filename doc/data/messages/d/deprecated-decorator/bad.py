import abc


class FishClass:
    @abc.abstractclassmethod  # [deprecated-decorator]
    def my_method(cls):
        pass
