# pylint: disable=missing-docstring, no-member, unused-argument, invalid-name,unused-variable


class NotUselessSuper(object):

    def not_passing_keyword_only(self, first, *, second):
        return super(NotUselessSuper, self).not_passing_keyword_only(first)

    def passing_keyword_only_with_modifications(self, first, *, second):
        return super(NotUselessSuper, self).passing_keyword_only_with_modifications(
            first, second + 1)

    def not_passing_all_params(self, first, *args, second=None, **kwargs):
        return super(NotUselessSuper, self).not_passing_all_params(*args, second, **kwargs)


class UselessSuper(object):

    def useless(self, first, *, second=None, **kwargs): # [useless-super-delegation]
        return super(UselessSuper, self).useless(first, second=second, **kwargs)

    def useless_1(self, *, first): # [useless-super-delegation]
        super(UselessSuper, self).useless_1(first=first)
