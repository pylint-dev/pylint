class Book:
    __match_args__ = ("title", "year")

    def __init__(self, title, year, author):
        self.title = title
        self.year = year
        self.author = author


def func(item: Book):
    match item:
        case Book("title", 2000, "author"):  # [too-many-positional-sub-patterns]
            ...
