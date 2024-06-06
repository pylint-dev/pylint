"""Test pylint.extension.typing - deprecated-typing-alias

'py-version' needs to be set to >= '3.13'.
"""
# pylint: disable=missing-docstring,invalid-name,unused-argument,line-too-long,unsubscriptable-object,unnecessary-direct-lambda-call
import typing
import typing_extensions

var1: typing.AsyncContextManager[int]  # [deprecated-typing-alias]
var2: typing.ContextManager[str]  # [deprecated-typing-alias]
var3: typing.AsyncGenerator[int]  # [deprecated-typing-alias]
var4: typing.Generator[str]  # [deprecated-typing-alias]

var5: typing_extensions.AsyncContextManager[int]  # [deprecated-typing-alias]
var6: typing_extensions.ContextManager[str]  # [deprecated-typing-alias]
var7: typing_extensions.AsyncGenerator[int]  # [deprecated-typing-alias]
var8: typing_extensions.Generator[str]  # [deprecated-typing-alias]
