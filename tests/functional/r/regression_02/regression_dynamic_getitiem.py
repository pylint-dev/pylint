# pylint: disable=missing-docstring,too-few-public-methods

class DynamicGetitem:
    def __getitem__(self, key):
        if key == 'attributes':
            return []
        return {'world': 123}


ex = DynamicGetitem()
a = ex['hello']['world']  # [invalid-sequence-index] known false-positive
