"""Check arguments for exception classes that raise instantiates."""

# pylint: disable=missing-docstring


class RequiredError(Exception):
    def __init__(self, reason):
        super().__init__(reason)


class InheritedError(RequiredError):
    pass


class NoArgumentError(Exception):
    def __init__(self):
        super().__init__("fixed message")


class DefaultedError(Exception):
    def __init__(self, reason="default"):
        super().__init__(reason)


class KeywordOnlyError(Exception):
    def __init__(self, *, reason):
        super().__init__(reason)


class NewError(Exception):
    def __new__(cls, reason, /):
        return super().__new__(cls, reason)


class NotAnException:
    def __init__(self, reason):
        self.reason = reason


def implicit():
    raise RequiredError  # [no-value-for-parameter]


def explicit():
    raise RequiredError()  # [no-value-for-parameter]


def supplied_argument():
    raise RequiredError("explicit")


def no_argument():
    raise NoArgumentError


def defaulted_argument():
    raise DefaultedError


def builtin_exception():
    raise ValueError


def inherited_constructor():
    raise InheritedError  # [no-value-for-parameter]


def keyword_only_constructor():
    raise KeywordOnlyError  # [missing-kwoa]


def explicit_keyword_only_constructor():
    raise KeywordOnlyError()  # [missing-kwoa]


def custom_new():
    raise NewError  # [no-value-for-parameter]


def explicit_custom_new():
    raise NewError("explicit")


def exception_instance():
    error = RequiredError("instance")
    raise error


def bare_reraise():
    try:
        raise RequiredError("reraised")
    except RequiredError:
        print("reraising")
        raise


def unresolved_exception(error):
    raise error


def ambiguous_exception(condition):
    raise RequiredError if condition else DefaultedError


def non_exception_class():
    raise NotAnException  # [raising-non-exception]



RequiredAlias = RequiredError


def raise_alias():
    raise RequiredAlias  # [no-value-for-parameter]


class FreeError(Exception):
    pass


class RequiredMetaclass(type):
    def __call__(cls, reason):
        return super().__call__(reason)


class MetaclassError(Exception, metaclass=RequiredMetaclass):
    pass


def required_metaclass_argument():
    raise MetaclassError  # [no-value-for-parameter]


class DefaultedMetaclass(RequiredMetaclass):
    def __call__(cls, reason="provided"):
        return super().__call__(reason)


class MetaclassMixin(metaclass=DefaultedMetaclass):  # pylint: disable=too-few-public-methods
    pass


class MostDerivedMetaclassError(MetaclassError, MetaclassMixin):
    pass


def inherited_most_derived_metaclass():
    raise MostDerivedMetaclassError


def ambiguous_new(condition):
    raise NewError if condition else FreeError


def ambiguous_metaclass(condition):
    raise MetaclassError if condition else FreeError


class SuppliesArgument:  # pylint: disable=too-few-public-methods
    def __init__(self):
        super().__init__("provided")


class SuppliesArgumentMeta(type):
    def __call__(cls):
        return super().__call__("provided")


def unresolved_base(mixin):
    class MixedError(mixin, RequiredError):
        pass

    raise MixedError


def ambiguous_base(condition):
    class MixedError(RequiredError if condition else FreeError):
        pass

    raise MixedError


def unresolved_metaclass(meta):
    class DynamicError(RequiredError, metaclass=meta):
        pass

    raise DynamicError


def inherited_unresolved_metaclass(meta):
    class DynamicError(RequiredError, metaclass=meta):
        pass

    class DerivedError(DynamicError):
        pass

    raise DerivedError


def ambiguous_metaclass_declaration(condition):
    class DynamicError(
        RequiredError, metaclass=RequiredMetaclass if condition else SuppliesArgumentMeta
    ):
        pass

    raise DynamicError


def unpacked_metaclass(options):
    class DynamicError(RequiredError, **options):
        pass

    raise DynamicError


class StaticInitError(Exception):
    @staticmethod
    def __init__():
        pass


def static_initializer():
    raise StaticInitError


def factory(_reason):
    return RequiredError


def invalid_factory_call():
    raise factory()  # [no-value-for-parameter]


def invalid_factory_branch(condition):
    raise factory() if condition else RequiredError  # [no-value-for-parameter]


def unresolved_metaclass_base(base):
    class DynamicMeta(base, type):
        pass

    class DynamicError(RequiredError, metaclass=DynamicMeta):
        pass

    raise DynamicError


def implicit_cause():
    raise ValueError from RequiredError



class DeadInitializerError(Exception):
    if False:  # pylint: disable=using-constant-test
        def __init__(self, reason):
            super().__init__(reason)


def dead_initializer():
    raise DeadInitializerError


def conditional_initializer(defaulted):
    class ConditionalInitializerError(Exception):
        if defaulted:
            def __init__(self):
                super().__init__("provided")
        else:
            def __init__(self, reason):
                super().__init__(reason)

    class DerivedError(ConditionalInitializerError):
        pass

    raise DerivedError


def conditional_metaclass_call(defaulted):
    class ConditionalMeta(type):
        if defaulted:
            def __call__(cls):
                return super().__call__("provided")
        else:
            def __call__(cls, reason):
                return super().__call__(reason)

    class DerivedMeta(ConditionalMeta):
        pass

    class ConditionalMetaclassError(Exception, metaclass=DerivedMeta):
        pass

    raise ConditionalMetaclassError


class DeadNewError(Exception):
    if False:  # pylint: disable=using-constant-test
        def __new__(cls, reason, /):
            return super().__new__(cls, reason)


class InheritedDeadNewError(DeadNewError):
    pass


def inherited_dead_new():
    raise InheritedDeadNewError


def same_class_twice(condition):
    raise RequiredError if condition else RequiredAlias  # [no-value-for-parameter]
