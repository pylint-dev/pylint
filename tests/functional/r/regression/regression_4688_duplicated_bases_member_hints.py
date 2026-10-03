# pylint: disable=missing-docstring, pointless-statement, useless-object-inheritance
# pylint: disable=duplicate-bases, too-few-public-methods


class Klass(object, object):
    def get(self):
        self._non_existent_attribute # [no-member]
