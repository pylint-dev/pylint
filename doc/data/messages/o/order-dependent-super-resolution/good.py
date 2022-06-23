class HarshParent:
    def scold():
        return "Don't do that!"


class KindParent:
    def scold():
        return "It would be better for you in the long run if you wouldn't do that."


class Child(HarshParent, KindParent):
    def scold():
        HarshParent.scold()
