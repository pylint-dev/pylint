# pylint: disable=missing-docstring
from argparse import ArgumentParser # [unused-import]
from argparse import Namespace  # [unused-import]
from typing import Literal as Lit
import typing as t

# str inside Literal shouldn't be treated as names
example: t.Literal["ArgumentParser", Lit["Namespace", "ArgumentParser"]]
