"""Test case for typevar-name-missing-variance with non-default settings"""
from typing import TypeVar, ParamSpec
import typing_extensions as te

# Name set by regex pattern
TypeVarsShouldBeLikeThis = TypeVar("TypeVarsShouldBeLikeThis")
TypeVarsShouldBeLikeThis_contra = TypeVar(
    "TypeVarsShouldBeLikeThis_contra", contravariant=True
)
TypeVarsShouldBeLikeThis_co = TypeVar("TypeVarsShouldBeLikeThis_co", covariant=True)

# Name using the standard style
GoodNameT = TypeVar("GoodNameT")  # [invalid-name]
GoodNameT_co = TypeVar("GoodNameT_co", covariant=True)  # [invalid-name]
GoodNameT_contra = TypeVar("GoodNameT_contra", contravariant=True)  # [invalid-name]


# -- typing_extensions.TypeVar --
TypeVarsShouldBeLikeThis = te.TypeVar("TypeVarsShouldBeLikeThis")
GoodNameT = te.TypeVar("GoodNameT")  # [invalid-name]
GoodNameT_co = te.TypeVar("GoodNameT_co", covariant=True)  # [invalid-name]


# -- typing.ParamSpec --
ParamSpecShouldBeLikeThis = ParamSpec("ParamSpecShouldBeLikeThis")
GoodNameP = ParamSpec("GoodNameP")  # [invalid-name]

# -- typing_extensions.ParamSpec --
ParamSpecShouldBeLikeThis = te.ParamSpec("ParamSpecShouldBeLikeThis")
GoodNameP = te.ParamSpec("GoodNameP")  # [invalid-name]


# # -- typing.TypeVarTuple (TODO 3.11+) --
# TypeVarTupleShouldBeLikeThis = TypeVarTuple("TypeVarTupleShouldBeLikeThis")
# GoodNameTs = TypeVarTuple("GoodNameTs")  # invalid-name

# -- typing_extensions.TypeVarTuple --
# TODO Can't infer typing_extensions.TypeVarTuple for 3.10  # pylint:disable=fixme
TypeVarTupleShouldBeLikeThis = te.TypeVarTuple("TypeVarTupleShouldBeLikeThis")
GoodNameTs = te.TypeVarTuple("GoodNameTs")  # >=3.11:[invalid-name]
