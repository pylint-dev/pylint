"""Example cases for dict-init-mutate"""
# pylint: disable=use-dict-literal, invalid-name, too-few-public-methods

base = {}

fruits = {}
for fruit in ["apple", "orange"]:
    fruits[fruit] = 1
    fruits[fruit] += 1

count = 10
fruits = {"apple": 1}
fruits["apple"] += count

config = {}  # [dict-init-mutate]
config['pwd'] = 'hello'

config = {}  # [dict-init-mutate]
config['dir'] = 'bin'
config['user'] = 'me'
config['workers'] = 5
print(config)

config = {}  # Not flagging calls to update for now
config.update({"dir": "bin"})

config = {}  # [dict-init-mutate]
config['options'] = {}  # Identifying nested assignment not supporting this yet.
config['options']['debug'] = False
config['options']['verbose'] = True


config = {}
def update_dict(di):
    """Update a dictionary"""
    di["one"] = 1

update_dict(config)

config = {}
globals()["config"]["dir"] = "bin"

# Test case from #7819: dict init with dict comprehension value
expectedrows = 100
axes = [("col1", "int"), ("col2", "str")]
d = {"name": "table", "expectedrows": expectedrows}  # [dict-init-mutate]
d["description"] = {a[0]: a[1] for a in axes}


# Test case from #7819 (attribute access form)
class Axis:
    """Stub for attribute access test."""
    def __init__(self, cname, typ):
        self.cname = cname
        self.typ = typ

self_axes = [Axis("col1", "int"), Axis("col2", "str")]
d = {"name": "table", "expectedrows": expectedrows}  # [dict-init-mutate]
d["description"] = {a.cname: a.typ for a in self_axes}
# Taken from a false positive in pytest
# https://github.com/pytest-dev/pytest/blob/728652641b378bb6ff31843698e562fc45536634/src/_pytest/junitxml.py#L74-L83
# pylint: disable-next=missing-function-docstring
def merge_family(left, right) -> None:
    result = {}
    for kl, vl in left.items():
        for kr, vr in right.items():  # pylint: disable=unused-variable
            if not isinstance(vl, list):
                raise TypeError(type(vl))
            result[kl] = vl + vr
    left.update(result)

families = {  # [dict-init-mutate]
    "_base": {"testcase": ["classname", "name"]},
    "_base_legacy": {"testcase": ["file", "line", "url"]},
}
families["xunit1"] = families["_base"].copy()
merge_family(families["xunit1"], families["_base_legacy"])
families["xunit2"] = families["_base"]

# Test case: many mutations should be truncated in the suggestion
settings = {}  # [dict-init-mutate]
settings["a"] = 1
settings["b"] = 2
settings["c"] = 3
settings["d"] = 4
settings["e"] = 5
settings["f"] = 6
settings["g"] = 7
