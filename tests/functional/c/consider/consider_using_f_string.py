"""Test to see if an f-string would be possible and consider-using-f-string should be raised"""
# pylint: disable=unused-variable, invalid-name, missing-function-docstring, pointless-statement
# pylint: disable=expression-not-assigned, repeated-keyword, too-many-locals

PARAM_1 = PARAM_2 = PARAM_3 = 1
PARAM_LIST = [PARAM_1, PARAM_2, PARAM_3]
PARAM_LIST_SINGLE = [PARAM_1]
PARAM_DICT = {"Param_1": PARAM_1, "Param_2": PARAM_2, "Param_3": PARAM_3}
PARAM_DICT_SINGLE = {"Param_1": PARAM_1}


def return_parameter():
    return PARAM_1


def return_list():
    return PARAM_LIST


def return_dict():
    return PARAM_DICT


def print_good():
    print("String {}, {} or {}".format(*PARAM_LIST))
    print("String {}, {}, {} or {}".format(*PARAM_LIST_SINGLE, *PARAM_LIST))
    print("String {Param}, {}, {} or {}".format(Param=PARAM_1, *PARAM_LIST))
    print("String {Param} {Param}".format(Param=PARAM_1))
    print("{Param_1} {Param_2}".format(**PARAM_DICT))
    print("{Param_1} {Param_2} {Param_3}".format(**PARAM_DICT_SINGLE, **PARAM_DICT))
    print("{Param_1} {Param_2} {Param_3}".format(Param_1=PARAM_1, **PARAM_DICT))
    print("{Param_1} {Param_2}".format(**PARAM_DICT))
    print("{Param_1} {Param_2}".format(**return_dict()))
    print("%(Param_1)s %(Param_2)s" % PARAM_LIST)
    print("%(Param_1)s %(Param_2)s" % PARAM_DICT)
    print("%(Param_1)s %(Param_2)s" % return_dict())
    print("{a[Param_1]}{a[Param_2]}".format(a=PARAM_DICT))
    print("{}".format("\n"))
    print("{}".format("\n".join(i for i in "string")))
    print("%s" % "\n")
    print("%s" % "\n".join(i for i in "string"))
    print("{%s}%s" % (PARAM_1, PARAM_2))


def print_bad():
    print("String %f" % PARAM_1)  # [consider-using-f-string]
    print("String {}".format(PARAM_1))  # [consider-using-f-string]
    print("String {Param_1}".format(Param_1=PARAM_1))  # [consider-using-f-string]
    print("{} {}".format(PARAM_1, PARAM_2))  # [consider-using-f-string]
    print("{Par_1}{Par_2}".format(Par_1=PARAM_1, Par_2=PARAM_2))  # [consider-using-f-string]
    print("{Param_1}".format(*PARAM_LIST_SINGLE))  # [consider-using-f-string]
    print("{Param_1}".format(**PARAM_DICT_SINGLE))  # [consider-using-f-string]
    print("String %s" % (PARAM_1))  # [consider-using-f-string]
    print("String %s %s" % (PARAM_1, PARAM_2))  # [consider-using-f-string]
    print("String %s" % (PARAM_LIST_SINGLE))  # [consider-using-f-string]


def statement_good():
    "String {}, {} or {}".format(*PARAM_LIST)
    "String {}, {}, {} or {}".format(*PARAM_LIST_SINGLE, *PARAM_LIST)
    "String {Param}, {}, {} or {}".format(Param=PARAM_1, *PARAM_LIST)
    "String {Param} {Param}".format(Param=PARAM_1)
    "{Param_1} {Param_2}".format(**PARAM_DICT)
    "{Param_1} {Param_2} {Param_3}".format(**PARAM_DICT_SINGLE, **PARAM_DICT)
    "{Param_1} {Param_2} {Param_3}".format(Param_1=PARAM_1, **PARAM_DICT)
    "{Param_1} {Param_2}".format(**PARAM_DICT)
    "{Param_1} {Param_2}".format(**return_dict())
    "%(Param_1)s %(Param_2)s" % PARAM_LIST
    "%(Param_1)s %(Param_2)s" % PARAM_DICT
    "%(Param_1)s %(Param_2)s" % return_dict()
    "{a[Param_1]}{a[Param_2]}".format(a=PARAM_DICT)
    "{}".format("\n")
    "{}".format("\n".join(i for i in "string"))
    "%s" % "\n"
    "%s" % "\n".join(i for i in "string")
    1 % "str"
    (1, 2) % 'garbage'


def statement_bad():
    "String %f" % PARAM_1  # [consider-using-f-string]
    "String {}".format(PARAM_1)  # [consider-using-f-string]
    "String {Param_1}".format(Param_1=PARAM_1)  # [consider-using-f-string]
    "{} {}".format(PARAM_1, PARAM_2)  # [consider-using-f-string]
    "{Par_1}{Par_2}".format(Par_1=PARAM_1, Par_2=PARAM_2)  # [consider-using-f-string]
    "{Param_1}".format(*PARAM_LIST_SINGLE)  # [consider-using-f-string]
    "{Param_1}".format(**PARAM_DICT_SINGLE)  # [consider-using-f-string]
    "String %s" % (PARAM_1)  # [consider-using-f-string]
    "String %s %s" % (PARAM_1, PARAM_2)  # [consider-using-f-string]
    "String %s" % (PARAM_LIST_SINGLE)  # [consider-using-f-string]


def assignment_good():
    A = "String {}, {} or {}".format(*PARAM_LIST)
    B = "String {}, {}, {} or {}".format(*PARAM_LIST_SINGLE, *PARAM_LIST)
    C = "String {Param}, {}, {} or {}".format(Param=PARAM_1, *PARAM_LIST)
    D = "String {Param} {Param}".format(Param=PARAM_1)
    E = "{Param_1} {Param_2}".format(**PARAM_DICT)
    F = "{Param_1} {Param_2} {Param_3}".format(**PARAM_DICT_SINGLE, **PARAM_DICT)
    G = "{Param_1} {Param_2} {Param_3}".format(Param_1=PARAM_1, **PARAM_DICT)
    H = "{Param_1} {Param_2}".format(**PARAM_DICT)
    I = "{Param_1} {Param_2}".format(**return_dict())
    J = "%(Param_1)s %(Param_2)s" % PARAM_LIST
    K = "%(Param_1)s %(Param_2)s" % PARAM_DICT
    L = "%(Param_1)s %(Param_2)s" % return_dict()
    M = "{a[Param_1]}{a[Param_2]}".format(a=PARAM_DICT)
    N = "{Param}".format
    O = "%s" % "\n"
    P = "%s" % "\n".join(i for i in "string")


def assignment_bad():
    a = "String %f" % PARAM_1  # [consider-using-f-string]
    b = "String {}".format(PARAM_1)  # [consider-using-f-string]
    c = "String {Param_1}".format(Param_1=PARAM_1)  # [consider-using-f-string]
    d = "{} {}".format(PARAM_1, PARAM_2)  # [consider-using-f-string]
    e = "{Par_1}{Par_2}".format(Par_1=PARAM_1, Par_2=PARAM_2)  # [consider-using-f-string]
    f = "{Param_1}".format(*PARAM_LIST_SINGLE)  # [consider-using-f-string]
    g = "{Param_1}".format(**PARAM_DICT_SINGLE)  # [consider-using-f-string]
    h = "String %s" % (PARAM_1)  # [consider-using-f-string]
    i = "String %s %s" % (PARAM_1, PARAM_2)  # [consider-using-f-string]
    j = "String %s" % (PARAM_LIST_SINGLE)  # [consider-using-f-string]


def regression_tests():
    # Referencing .format in a kwarg should not be warned
    def wrap_print(value):
        print(value)

    wrap_print(value="{}".format)
