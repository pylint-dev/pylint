"""Emit a message for breaking out of a while True loop immediately."""
# pylint: disable=line-too-long,missing-docstring,unsubscriptable-object,too-few-public-methods,redefined-outer-name,use-dict-literal,modified-iterating-dict

class Issue8015:
    def bad(self):
        k = 1
        while True:  # [consider-using-while-not]
            if k == 10:
                break
            k += 1


    def good(self):
        k = 1
        while True:
            k += 1
            if k == 10:
                break

    def complicated_bad(self):
        a_var = 1
        b_var = 1
        while True:  # [consider-using-while-not]
            if (a_var == 10) is (b_var == 10):
                break
            a_var += 1
            b_var += 1
