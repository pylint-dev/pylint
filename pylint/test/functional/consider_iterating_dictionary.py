# pylint: disable=missing-docstring, expression-not-assigned, too-few-public-methods, no-member, import-error, no-self-use

from unknown import Unknown


class CustomClass(object):
    def keys(self):
        return []

for key in Unknown().keys():
    pass
for key in Unknown.keys():
    pass
for key in dict.keys():
    pass
for key in {}.values():
    pass
for key in {}.key():
    pass
for key in CustomClass().keys():
    pass

[key for key in {}.keys()] # [consider-iterating-dictionary]
(key for key in {}.keys()) # [consider-iterating-dictionary]
{key for key in {}.keys()} # [consider-iterating-dictionary]
{key: key for key in {}.keys()} # [consider-iterating-dictionary]
for key in {}.keys(): # [consider-iterating-dictionary]
    pass
