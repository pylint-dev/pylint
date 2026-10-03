"""https://github.com/pylint-dev/pylint/issues/4590"""
# pylint: disable=too-few-public-methods


def conditional_class_factory():
    """Define a nested class"""
    class ConditionalClass(ModuleClass):
        """Subclasses a name from the module scope"""
    return ConditionalClass


class ModuleClass:
    """Module-level class"""
