class HarshParent:
    @staticmethod
    def scold():
        return "Don't do that!"


class KindParent:
    @staticmethod
    def scold():
        return "It would be better for you in the long run if you wouldn't do that."


class Child(HarshParent, KindParent):
    @staticmethod
    def scold():
        return HarshParent.scold()
