# pylint: disable=missing-docstring, no-member, unused-argument, invalid-name,unused-variable
# pylint: disable=too-few-public-methods

class NotUselessSuper(object):

    def not_passing_keyword_only(self, first, *, second):
        return super(NotUselessSuper, self).not_passing_keyword_only(first)

    def passing_keyword_only_with_modifications(self, first, *, second):
        return super(NotUselessSuper, self).passing_keyword_only_with_modifications(
            first, second + 1)

class UselessSuper(object):

    def useless(self, *, first): # [useless-super-delegation]
        super(UselessSuper, self).useless(first=first)


class Egg():
    def __init__(self, thing: object) -> None:
        pass

class Spam(Egg):
    def __init__(self, thing: int) -> None:
        super().__init__(thing)

class Ham(Egg):
    def __init__(self, thing: object) -> None: # [useless-super-delegation]
        super().__init__(thing)
