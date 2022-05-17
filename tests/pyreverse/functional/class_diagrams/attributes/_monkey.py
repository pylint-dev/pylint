# This is not a standalone test
# Monkey class is called from Tree class in delayed_external_monkey_patching.py


class Monkey:
    def __init__(self, name):
        # pylint: disable=import-outside-toplevel
        from delayed_external_monkey_patching import Tree

        self.name = name
        self.tree = Tree()
        self.tree.has_tasty_bananas = True  # This monkey patching will increase the number of items in instance_attrs for `Tree`
