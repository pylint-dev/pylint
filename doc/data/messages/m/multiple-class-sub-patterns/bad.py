class Book:
    __match_args__ = ("title", "year")

    def __init__(self, title, year):
        self.title = title
        self.year = year


def func(item: Book):
    match item:
        case Book("abc", title="abc"):  # [multiple-class-sub-patterns]
            ...
        case Book(year=2000, year=2001):  # [multiple-class-sub-patterns]
            ...
