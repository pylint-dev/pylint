# pylint: disable=missing-docstring, no-member, no-self-use, bad-super-call
# pylint: disable=too-few-public-methods, unused-argument, invalid-name, too-many-public-methods
# pylint: disable=line-too-long, useless-object-inheritance


def not_a_method(param, param2):
    return super(None, None).not_a_method(param, param2)


class SuperBase(object):
    def with_default_arg(self, first, default_arg="only_in_super_base"):
        pass

    def with_default_arg_bis(self, first, default_arg="only_in_super_base"):
        pass

    def with_default_arg_ter(self, first, default_arg="will_be_changed"):
        pass

    def with_default_arg_quad(self, first, default_arg="will_be_changed"):
        pass


class Base(SuperBase):

    fake_method = not_a_method

    def something(self):
        pass

    def with_default_argument(self, first, default_arg="default"):
        pass

    def with_default_argument_bis(self, first, default_arg="default"):
        pass

    def without_default_argument(self, first, second):
        pass

    def with_default_argument_none(self, first, default_arg=None):
        pass

    def without_default_argument2(self, first, second):
        pass

    def with_default_argument_int(self, first, default_arg=42):
        pass

    def with_default_argument_tuple(self, first, default_arg=()):
        pass

    def with_default_arg_ter(self, first, default_arg="has_been_changed"):
        super(Base, self).with_default_arg_ter(first, default_arg)

    def with_default_arg_quad(self, first, default_arg="has_been_changed"):
        super(Base, self).with_default_arg_quad(first, default_arg)

class NotUselessSuper(Base):

    def multiple_statements(self):
        first = 42 * 24
        return super(NotUselessSuper, self).multiple_statements() + first

    def not_a_call(self):
        return 1 + 2

    def not_super_call(self):
        return type(self).__class__

    def not_super_attribute_access(self):
        return super(NotUselessSuper, self)

    def invalid_super_call(self):
        return super(NotUselessSuper, 1).invalid_super_call()

    def other_invalid_super_call(self):
        return super(2, 3, 4, 5).other_invalid_super_call()

    def different_name(self):
        return super(NotUselessSuper, self).something()

    def different_super_mro_pointer(self):
        return super(Base, self).different_super_mro_pointer()

    def different_super_type(self):
        return super(NotUselessSuper, NotUselessSuper).different_super_type()

    def other_different_super_type(self):
        return super(NotUselessSuper, 1).other_different_super_type()

    def not_passing_param(self, first):
        return super(NotUselessSuper, self).not_passing_param()

    def modifying_param(self, first):
        return super(NotUselessSuper, self).modifying_param(first + 1)

    def transforming_param(self, first):
        return super(NotUselessSuper, self).transforming_param(type(first))

    def modifying_variadic(self, *args):
        return super(NotUselessSuper, self).modifying_variadic(tuple(args))

    def not_passing_keyword_variadics(self, *args, **kwargs):
        return super(NotUselessSuper, self).not_passing_keyword_variadics(*args)

    def not_passing_default(self, first, second=None):
        return super(NotUselessSuper, self).not_passing_default(first)

    def passing_only_a_handful(self, first, second, third, fourth):
        return super(NotUselessSuper, self).passing_only_a_handful(
            first, second)

    def not_the_same_order(self, first, second, third):
        return super(NotUselessSuper, self).not_the_same_order(third, first, second)

    def no_kwargs_in_signature(self, key=None):
        values = {'key': 'something'}
        return super(NotUselessSuper, self).no_kwargs_in_signature(**values)

    def no_args_in_signature(self, first, second):
        values = (first + 1, second + 2)
        return super(NotUselessSuper, self).no_args_in_signature(*values)

    def variadics_with_multiple_keyword_arguments(self, **kwargs):
        return super(NotUselessSuper, self).variadics_with_multiple_keyword_arguments(
            first=None,
            second=None,
            **kwargs)

    def extraneous_keyword_params(self, none_ok=False):
        super(NotUselessSuper, self).extraneous_keyword_params(
            none_ok,
            valid_values=[23, 42])

    def extraneous_positional_args(self, **args):
        super(NotUselessSuper, self).extraneous_positional_args(
            1, 2, **args)

    def with_default_argument(self, first, default_arg="other"):
        # Not useless because the default_arg is different from the one in the base class
        super(NotUselessSuper, self).with_default_argument(first, default_arg)

    def without_default_argument(self, first, second=True):
        # Not useless because in the base class there is not default value for second argument
        super(NotUselessSuper, self).without_default_argument(first, second)

    def with_default_argument_none(self, first, default_arg='NotNone'):
        # Not useless because the default_arg is different from the one in the base class
        super(NotUselessSuper, self).with_default_argument_none(first, default_arg)

    def without_default_argument2(self, first, second=None):
        # Not useless because in the base class there is not default value for second argument
        super(NotUselessSuper, self).without_default_argument2(first, second)

    def with_default_argument_int(self, first, default_arg="42"):
        # Not useless because the default_arg is a string whereas in the base class it's an int
        super(NotUselessSuper, self).with_default_argument_int(first, default_arg)

    def with_default_argument_tuple(self, first, default_arg=("42", "a")):
        # Not useless because the default_arg is different from the one in the base class
        super(NotUselessSuper, self).with_default_argument_tuple(first, default_arg)

    def with_default_argument_bis(self, first, default_arg="default"):
        # Although the default_arg is the same as in the base class, the call signature
        # differs. Thus it is not useless.
        super(NotUselessSuper, self).with_default_argument_bis(default_arg + "_argument")

    def fake_method(self, param2="other"):
        super(NotUselessSuper, self).fake_method(param2)

    def with_default_arg(self, first, default_arg="only_in_super_base"):
        # Not useless because the call of this method is different from the function signature
        super(NotUselessSuper, self).with_default_arg(first, default_arg + "_and_here")

    def with_default_arg_bis(self, first, default_arg="default_changed"):
        # Not useless because the default value is different from the SuperBase one
        super(NotUselessSuper, self).with_default_arg_bis(first, default_arg)

    def with_default_arg_ter(self, first, default_arg="has_been_changed_again"):
        # Not useless because the default value is different from the Base one
        super(NotUselessSuper, self).with_default_arg_ter(first, default_arg)

    def with_default_arg_quad(self, first, default_arg="has_been_changed"):
        # Not useless because the default value is the same as in the base but the
        # call is different from the signature
        super(NotUselessSuper, self).with_default_arg_quad(first, default_arg + "_and_modified")


class UselessSuper(Base):

    def equivalent_params(self): # [useless-super-delegation]
        return super(UselessSuper, self).equivalent_params()

    def equivalent_params_1(self, first): # [useless-super-delegation]
        return super(UselessSuper, self).equivalent_params_1(first)

    def equivalent_params_2(self, *args): # [useless-super-delegation]
        return super(UselessSuper, self).equivalent_params_2(*args)

    def equivalent_params_3(self, *args, **kwargs): # [useless-super-delegation]
        return super(UselessSuper, self).equivalent_params_3(*args, **kwargs)

    def equivalent_params_4(self, first): # [useless-super-delegation]
        super(UselessSuper, self).equivalent_params_4(first)

    def equivalent_params_5(self, first, *args): # [useless-super-delegation]
        super(UselessSuper, self).equivalent_params_5(first, *args)

    def equivalent_params_6(self, first, *args, **kwargs): # [useless-super-delegation]
        return super(UselessSuper, self).equivalent_params_6(first, *args, **kwargs)

    def with_default_argument(self, first, default_arg="default"): # [useless-super-delegation]
        # useless because the default value here is the same as in the base class
        return super(UselessSuper, self).with_default_argument(first, default_arg)

    def without_default_argument(self, first, second): # [useless-super-delegation]
        return super(UselessSuper, self).without_default_argument(first, second)

    def with_default_argument_none(self, first, default_arg=None): # [useless-super-delegation]
        # useless because the default value here is the same as in the base class
        super(UselessSuper, self).with_default_argument_none(first, default_arg)

    def with_default_argument_int(self, first, default_arg=42): # [useless-super-delegation]
        super(UselessSuper, self).with_default_argument_int(first, default_arg)

    def with_default_argument_tuple(self, first, default_arg=()): # [useless-super-delegation]
        super(UselessSuper, self).with_default_argument_tuple(first, default_arg)

    def __init__(self): # [useless-super-delegation]
        super(UselessSuper, self).__init__()

    def with_default_arg(self, first, default_arg="only_in_super_base"): # [useless-super-delegation]
        super(UselessSuper, self).with_default_arg(first, default_arg)

    def with_default_arg_bis(self, first, default_arg="only_in_super_base"): # [useless-super-delegation]
        super(UselessSuper, self).with_default_arg_bis(first, default_arg)

    def with_default_arg_ter(self, first, default_arg="has_been_changed"): # [useless-super-delegation]
        super(UselessSuper, self).with_default_arg_ter(first, default_arg)

    def with_default_arg_quad(self, first, default_arg="has_been_changed"): # [useless-super-delegation]
        super(UselessSuper, self).with_default_arg_quad(first, default_arg)


def trigger_something(value_to_trigger):
    pass


class NotUselessSuperDecorators(Base):
    @trigger_something('value1')
    def method_decorated(self):
        super(NotUselessSuperDecorators, self).method_decorated()
