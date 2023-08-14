This is a message that isn't going to be raised for python > 3.3. It was raised
for code like::

    def interrogate_until_you_find_jack(pirates):
        for pirate in pirates:
            if pirate == "Captain Jack Sparrow":
                return "Arrr! We've found our captain!"
            yield pirate

Which is now valid and equivalent to the previously expected::

    def interrogate_until_you_find_jack(pirates):
        for pirate in pirates:
            if pirate == "Captain Jack Sparrow":
                raise StopIteration("Arrr! We've found our captain!")
            yield pirate
