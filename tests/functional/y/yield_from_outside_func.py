"""This is grammatically correct, but it's still a SyntaxError"""
# pylint: disable=unnecessary-lambda-assignment

yield from [1, 2]  # [yield-outside-function]

LAMBDA_WITH_YIELD = lambda: (yield from [1, 2])
