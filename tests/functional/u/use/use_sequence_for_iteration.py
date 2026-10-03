# pylint: disable=missing-docstring,pointless-statement,unnecessary-comprehension

VAR = {1, 2, 3}

for x in VAR:
    pass
for x in {1, 2, 3}:  # [use-sequence-for-iteration]
    pass

(x for x in VAR)
(x for x in {1, 2, 3})  # [use-sequence-for-iteration]

[x for x in VAR]
[x for x in {1, 2, 3}]  # [use-sequence-for-iteration]

[x for x in {*VAR, 4}]

def deduplicate(list_in):
    for thing in {*list_in}:
        print(thing)

def deduplicate_two_lists(input1, input2):
    for thing in {*input1, *input2}:
        print(thing)

def deduplicate_nested_sets(input1, input2, input3, input4):
    for thing in {{*input1, *input2}, {*input3, *input4}}:
        print(thing)
