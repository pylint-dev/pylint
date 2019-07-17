# pylint: disable=missing-docstring, too-few-public-methods


class Cls:
    @property
    def attribute(self, param, param1): # [property-with-parameters]
        return param + param1
