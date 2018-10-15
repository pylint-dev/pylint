import re

class Tokenizer:
    def __init__(self, filters, chunkers):
        self.filters = filters
        self.chunkers = chunkers
        self.sub_tokens = []

    def __iter__(self):
        return self

    def __next__(self):
        valid = False
        while not valid:
            valid = True
            
            if len(self.sub_tokens) > 0:
                base_token = self.sub_tokens.pop()
            else:
                base_token = self.next()

            for f in self.filters:
                if f.skip(base_token):
                    valid = False
                    break

        for c in self.chunkers:
            chunks = c.split(base_token)
            if len(chunks) > 1:
                self.sub_tokens.extend(chunks)
                return self.sub_tokens.pop()

        return base_token

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
    strip_from_start = set("\"'`([<{")
    strip_from_end = set("\"'`]).!,?;:>}")

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

            # Strip chars from front/end of word
            while sPos < len(self._text) and self._text[sPos] in self.strip_from_start:
                sPos += 1
            while 0 < ePos and self._text[ePos-1] in self.strip_from_end:
                ePos -= 1

            # Return if word isn't empty
            if sPos < ePos:
                return self._text[sPos:ePos]

        raise StopIteration()

class ForwardSlashChunker():
    """
    This chunker allows splitting words like 'before/after' into 'before' and 'after'
    """

    def split(self, token):
        return token.split("/")

class EnglishWordFilter():
    _pattern = re.compile(r"^[a-zA-Z'/\-]+$")

    def skip(self, token):
        return not bool(self._pattern.match(token))

class CamelCasedWordsFilter():
    r"""Filter skipping over camelCasedWords.
    This filter skips any words matching the following regular expression:

        ^([a-z]\w+[A-Z]+\w+)

    That is, any words that are camelCasedWords.
    """
    _pattern = re.compile(r"^([a-z]+([\d]|[A-Z])(?:\w+)?)")

    def skip(self, word):
        return bool(self._pattern.match(word))

class WikiWordFilter():
    r"""Filter skipping over WikiWords.
    This filter skips any words matching the following regular expression:

        ^([A-Z]\w+[A-Z]+\w+)

    That is, any words that are WikiWords.
    """
    _pattern = re.compile(r"^([A-Z]\w+[A-Z]+\w+)")
    def skip(self,word):
        return bool(self._pattern.match(word))

def get_tokenizer(filters=[], chunkers=[]):
    return WordTokenizer(filters, chunkers)
