class Book:
    __match_args__ = ("title", "year")

    def __init__(self, title, year):
        self.title = title
        self.year = year


def func(item: Book):
    match item:
        case Book(title=str() as title):
            ...
        case Book(year=int() as year):
            ...
