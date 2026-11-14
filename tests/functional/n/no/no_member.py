# pylint: disable=missing-docstring, unused-argument, wrong-import-position, invalid-name
from pathlib import Path

# Regression test for https://github.com/pylint-dev/pylint/issues/400
class TestListener:
    def __init__(self):
        self._latest = None

    def wait(self, timeout):
        result = self._latest
        self._latest = None
        return result

    def peer_joined(self, peer):
        self._latest = peer


listener = TestListener()
broker = listener.wait(3).get_domain()  # No error here


# Regression test for https://github.com/pylint-dev/pylint/issues/4377
from urllib import parse

url = 'http://www.google.com'

parsed_url = parse.urlparse(url)
sorted_query = parse.urlencode(
    sorted(parse.parse_qsl(parsed_url.query), key=lambda param: param[0]))
new_parsed_url = parse.ParseResult._replace(parsed_url, query=sorted_query)
new_url = new_parsed_url.geturl()  # No error here


# Regression test for https://github.com/pylint-dev/pylint/issues/3803
# pylint: disable=too-few-public-methods
class Base:
    label: str


class Derived(Base):
    label = "I exist!"


print(Derived.label)


# Regression test for https://github.com/pylint-dev/pylint/issues/5832
starter_path = Path(__file__).parents[3].resolve()


# Regression test for https://github.com/pylint-dev/pylint/issues/9203
class FactoryBase:
    def __init__(self):
        self.name = "base"

    @classmethod
    def from_dict(cls, values):
        return cls()


class FactoryChild(FactoryBase):
    def __init__(self):
        super().__init__()
        self.extra = "child"

    @classmethod
    def from_dict(cls, values):
        return super().from_dict(values)


print(FactoryChild.from_dict({}).extra)  # No error here
