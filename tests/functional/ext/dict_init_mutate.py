"""Example cases for dict-init-mutate"""
# pylint: disable=use-dict-literal, invalid-name

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
