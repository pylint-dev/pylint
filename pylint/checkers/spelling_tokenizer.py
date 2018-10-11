import re

class Tokenizer:
    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def tokenize(self, text):
        self._text = text
        self._offset = 0
        return self

    # Override this
    def next(self):
        raise StopIteration()

class WordTokenizer(Tokenizer):
    """Tokenizer class that performs very basic word-finding.

    This tokenizer does the most basic thing that could work - it splits
    text into words based on whitespace boundaries, and removes basic
    punctuation symbols from the start and end of each word.
    """

    # Chars to remove from start/end of words
    strip_from_start = '"' + "'`([<{"
    strip_from_end = '"' + "'`]).!,?;:>}"

    def next(self):
        while self._offset < len(self._text):
            # Find start of next word
            while self._offset < len(self._text) and self._text[self._offset].isspace():
                self._offset += 1
            sPos = self._offset

            # Find end of word
            while self._offset < len(self._text) and not self._text[self._offset].isspace():
                self._offset += 1
            ePos = self._offset

            # Strip chars from font/end of word
            while sPos < len(self._text) and self._text[sPos] in self.strip_from_start:
                sPos += 1
            while 0 < ePos and self._text[ePos-1] in self.strip_from_end:
                ePos -= 1

            # Return if word isn't empty
            if sPos < ePos:
                return self._text[sPos:ePos]

        raise StopIteration()

class Filter(Tokenizer):
    def __init__(self, tokenizer):
        self._tokenizer = tokenizer

    def tokenize(self, text):
        self._tokenizer.tokenize(text)
        return self

    def next(self):
        token = next(self._tokenizer)
        while self._skip(token):
            token = next(self._tokenizer)
        return token

    def _skip(self, token):
        return False

class Chunker(Tokenizer):
    def __init__(self, tokenizer):
        self._tokenizer = tokenizer
        self._stack = []

    def tokenize(self, text):
        self._tokenizer.tokenize(text)
        return self

    def next(self):
        if len(self._stack) > 0:
            token = self._stack.pop()
        else:
            token = next(self._tokenizer)

        subtokens = self._split(token)
        if 1 == len(subtokens):
            return subtokens[0]

        self._stack.extend(subtokens)
        return self._stack.pop()

    def _split(self, token):
        return [token]

class ForwardSlashChunker(Chunker):
    """
    This chunker allows splitting words like 'before/after' into 'before' and 'after'
    """

    def _split(self, token):
        return token.split("/")

class EmailFilter(Filter):
    r"""Filter skipping over email addresses.
    This filter skips any words matching the following regular expression:

        ^.+@[^\.].*\.[a-z]{2,}$

    That is, any words that resemble email addresses.
    """
    _pattern = re.compile(r"^.+@[^\.].*\.[a-z]{2,}$")
    def _skip(self,word):
        return bool(self._pattern.match(word))

class URLFilter(Filter):
    r"""Filter skipping over URLs.
    This filter skips any words matching the following regular expression:

        ^[a-zA-Z]+:\/\/[^\s].*

    That is, any words that are URLs.
    """
    _pattern = re.compile(r"^[a-zA-Z]+:\/\/[^\s].*")
    def _skip(self,word):
        return bool(self._pattern.match(word))

class WordsWithDigitsFilter(Filter):
    """Skips words with digits.
    """

    _pattern = re.compile(r"\d")
    def _skip(self, word):
        return bool(self._pattern.search(word))

class WordsWithUnderscoresFilter(Filter):
    """Skips words with underscores.

    They are probably function parameter names.
    """

    def _skip(self, word):
        return "_" in word


class CamelCasedWordsFilter(Filter):
    r"""Filter skipping over camelCasedWords.
    This filter skips any words matching the following regular expression:

        ^([a-z]\w+[A-Z]+\w+)

    That is, any words that are camelCasedWords.
    """
    _pattern = re.compile(r"^([a-z]+([\d]|[A-Z])(?:\w+)?)")

    def _skip(self, word):
        return bool(self._pattern.match(word))


class SphinxDirectivesFilter(Filter):
    r"""Filter skipping over Sphinx Directives.
    This filter skips any words matching the following regular expression:

        ^:([a-z]+):`([^`]+)(`)?

    That is, for example, :class:`BaseQuery`
    """
    # The final ` in the patternnn is optional because enchant strips it out
    _pattern = re.compile(r"^:([a-z]+):`([^`]+)(`)?")

    def _skip(self, word):
        return bool(self._pattern.match(word))

class WikiWordFilter(Filter):
    r"""Filter skipping over WikiWords.
    This filter skips any words matching the following regular expression:

        ^([A-Z]\w+[A-Z]+\w+)

    That is, any words that are WikiWords.
    """
    _pattern = re.compile(r"^([A-Z]\w+[A-Z]+\w+)")
    def _skip(self,word):
        return bool(self._pattern.match(word))

def get_tokenizer(filters=[], chunkers=[]):
    tokenizer = WordTokenizer()
    for f in filters:
        tokenizer = f(tokenizer)

    for c in chunkers:
        tokenizer = c(tokenizer)

    return tokenizer
