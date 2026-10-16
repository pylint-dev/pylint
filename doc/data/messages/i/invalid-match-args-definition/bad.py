class Book:
    __match_args__ = ["title", "year"]  # [invalid-match-args-definition]

    def __init__(self, title, year):
        self.title = title
        self.year = year
