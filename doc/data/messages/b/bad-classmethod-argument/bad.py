class Klass:
    @classmethod
    def get_instance(self):  # [bad-classmethod-argument]
        return self()
