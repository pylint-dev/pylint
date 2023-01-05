"""Emit a message for breaking out of a while True loop immediately."""
# pylint: disable=missing-function-docstring,missing-class-docstring,unrecognized-inline-option,invalid-name,literal-comparison

class Issue8015:
    def bad(self):
        k = 1
        while True:  # [consider-refactoring-into-while-condition]
            if k == 10:
                break
            k += 1

    def another_bad(self):
        current_scope = None
        while True:  # [consider-refactoring-into-while-condition]
            if current_scope is None:
                break
            current_scope = True

    def good(self):
        k = 1
        while True:
            k += 1
            if k == 10:
                break

    def test_error_message(self):
        a_list = [1,2,3,4,5]
        # Should recommend `while a_list`
        while True:   # [consider-refactoring-into-while-condition]
            if not a_list:
                break
            a_list.pop()

    def test_error_message_2(self):
        a_list = []
        # Should recommend `while not a_list`
        while True:   # [consider-refactoring-into-while-condition]
            if a_list:
                break
            a_list.append(1)

    def test_error_message_3(self):
        a_var = "defined"
        # Should recommend `while not a_var`
        while True:   # [consider-refactoring-into-while-condition]
            if a_var is not None:
                break
            a_var = None

    def test_error_message_4(self):
        a_list = []
        # Should recommend `while a_list is []`
        while True:   # [consider-refactoring-into-while-condition]
            if a_list is not []:
                break
            a_list.append(1)

    def test_error_message_5(self):
        a_dict = {}
        a_var = a_dict.get("undefined_key")
        # Should recommend `while a_var`
        while True:   # [consider-refactoring-into-while-condition]
            if a_var is None:
                break
            a_var = "defined"

    def test_error_message_6(self):
        a_list = []
        # Should recommend `while a_list is not []`
        while True:   # [consider-refactoring-into-while-condition]
            if a_list is []:
                break
            a_list.append(1)


    def test_error_message_7(self):
        # while not a and b is not correct
        # Expeccted message should be `while not (a and b)``
        a = True
        b = False
        while True:   # [consider-refactoring-into-while-condition]
            if a and b:
                break
            a = 1
            b = 1

    def test_error_message_8(self):
        # while not a and not b is not correct
        # Expeccted message should be `while not (a and not b)``
        a = True
        b = False
        while True:   # [consider-refactoring-into-while-condition]
            if a and not b:
                break
            a = 1
            b = 1

    def test_error_message_9(self):
        k = 1
        while True:  # [consider-refactoring-into-while-condition]
            if k != 1:
                break
            k += 1