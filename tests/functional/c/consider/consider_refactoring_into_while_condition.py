"""Emit a message for breaking out of a while True loop immediately."""
# pylint: disable=missing-function-docstring,missing-class-docstring,unrecognized-inline-option,invalid-name

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
        a_list = []
        # Should recommend `while not a_list`
        while True:   # [consider-refactoring-into-while-condition]
            if a_list is not None:
                break
            a_list.append(1)

    def test_error_message_4(self):
        a_list = []
        # Should recommend `while not a_list`
        while True:   # [consider-refactoring-into-while-condition]
            if a_list is None:
                break
            a_list.append(1)

    def test_error_message_5(self):
        # while not a and b is not correct
        # Expeccted message should be while not (a and b)
        a = True
        b = False
        while True:   # [consider-refactoring-into-while-condition]
            if a and b:
                break
            a = 1
            b = 1

    def test_error_message_6(self):
        # while not a and not b is not correct
        # Expeccted message should be while not (a and not b)
        a = True
        b = False
        while True:   # [consider-refactoring-into-while-condition]
            if a and not b:
                break
            a = 1
            b = 1
