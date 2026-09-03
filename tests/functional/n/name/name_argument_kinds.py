"""Every parameter kind is subject to the argument naming style."""
# pylint: disable=too-few-public-methods


def function(
    BadPosOnly,  # [invalid-name]
    /,
    BadPlain,  # [invalid-name]
    *BadStar,  # [invalid-name]
    BadKwOnly,  # [invalid-name]
    **BadKw,  # [invalid-name]
):
    """A function using all five parameter kinds."""
    return BadPosOnly, BadPlain, BadStar, BadKwOnly, BadKw


# visit_asyncfunctiondef is an alias of visit_functiondef.
async def coroutine(
    GoodEnough, /, *Args, KwOnly, **Kwargs  # [invalid-name,invalid-name,invalid-name,invalid-name]
):
    """An async function using four of the five parameter kinds."""
    return GoodEnough, Args, KwOnly, Kwargs


def well_named(pos_only, /, plain, *args, kw_only, **kwargs):
    """No message for any of these."""
    return pos_only, plain, args, kw_only, kwargs
