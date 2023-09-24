"""Emit a message for breaking out of a while True loop immediately."""
# pylint: disable=missing-function-docstring,missing-class-docstring,unrecognized-inline-option,invalid-name,literal-comparison, undefined-variable, too-many-public-methods, no-else-break

class Issue8015:
    def bad(self):
        k = 1
        while 1:  # [consider-refactoring-into-while-condition]
            if k == 10:
                break
            k += 1

    def another_bad(self):
        current_scope = None
        while 2:  # [consider-refactoring-into-while-condition]
            if current_scope is None:
                break
            current_scope = True

    def good(self):
        k = 1
        while True:
            k += 1
            if k == 10:
                break

    def another_good(self):
        k = 1
        while k < 10:
            k += 1

    def test_error_message_multiple_break(self, k: int) -> None:
        while True:  # [consider-refactoring-into-while-condition]
            if k <= 1:
                break
            if k > 10:
                break
            k -= 1

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

    def test_error_message_10(self):
        a = [1,2,3,4,5]
        while True:  # [consider-refactoring-into-while-condition]
            if 5 not in a:
                break
            a.pop()

    def test_error_message_11(self):
        a = []
        k = 1
        while True:  # [consider-refactoring-into-while-condition]
            if 5 in a:
                break
            a.append(k)
            k += 1

    def test_error_message_12(self):
        k = 1
        while True:  # [consider-refactoring-into-while-condition]
            if k > 10:
                break
            k += 1

    def test_error_message_13(self):
        k = 1
        while True:  # [consider-refactoring-into-while-condition]
            if k >= 10:
                break
            k += 1

    def test_error_message_14(self):
        k = 10
        while True:  # [consider-refactoring-into-while-condition]
            if k < 1:
                break
            k -= 1

    def test_error_message_15(self):
        k = 1
        while True:  # [consider-refactoring-into-while-condition]
            if k <= 1:
                break
            k -= 1

    def test_error_message_16(self):
        # Silly example but needed for coverage
        k = None
        while True:  # [consider-refactoring-into-while-condition]
            if (lambda x: x) == k:
                break
            break
        while True:  # [consider-refactoring-into-while-condition]
            if k == (lambda x: x):
                break
            break

    def test_error_message_17(self):
        a = True
        b = False
        c = True
        d = False
        while True:  # [consider-refactoring-into-while-condition]
            if (a or b) == (c and d):
                break
            a = not a if random.randint(0,1) == 1 else a
            b = not b if random.randint(0,1) == 1 else b
            c = not c if random.randint(0,1) == 1 else c
            d = not d if random.randint(0,1) == 1 else d

        while True:  # [consider-refactoring-into-while-condition]
            if (not a) == (not d):
                break
            a = not a if random.randint(0,1) == 1 else a
            d = not d if random.randint(0,1) == 1 else d

    def test_error_message_18(self):
        x = 0
        while True:  # [consider-refactoring-into-while-condition]
            if x ** 2:
                break
            x += 1

    def test_multi_break_condition_1(self):
        x = 0
        # This should chain conditions into
        # While (x == 0) and (x >= 0) and (x != 0):
        while True:  # [consider-refactoring-into-while-condition]
            if x != 0:
                break
            elif x > 0:
                x -= 1
            elif x < 0:
                break
            elif x == 0:
                break
            x -= 10

    def test_multi_break_condition_2(self):
        x = 0
        # This should chain both conditions
        while True:  # [consider-refactoring-into-while-condition]
            if x != 0:
                break
            if x == 0:
                break
            x -= 10

    def test_multi_break_condition_3(self):
        x = 0
        # This should chain all conditions
        while True:  # [consider-refactoring-into-while-condition]
            if x != 0:
                break
            elif x < 0:
                break
            elif x == 0:
                break
            if x != 100:
                break
            if x == 1000:
                break
            x -= 10

    def test_multi_break_condition_4(self):
        x = 0
        # This should chain all conditions except last 2.
        # The else clause taints the first if-elif-else block by introducing mutation
        while True:  # [consider-refactoring-into-while-condition]
            if x != 0:
                break
            elif x < 0:
                break
            elif x == 0:
                break
            else:
                x += 1
            if x != 100:
                break
            if x == 1000:
                break
            x -= 10

    def falsy_1(self):
        x = 0
        while []:
            if x > 10:
                break
            x += 1

    def falsy_2(self):
        x = 0
        while ():
            if x > 10:
                break
            x += 1

    def falsy_3(self):
        x = 0
        while {}:
            if x > 10:
                break
            x += 1

    def falsy_4(self):
        x = 0
        while set():
            if x > 10:
                break
            x += 1

    def falsy_5(self):
        x = 0
        while "":
            if x > 10:
                break
            x += 1

    def falsy_6(self):
        x = 0
        while range(0):
            if x > 10:
                break
            x += 1

    def falsy_7(self):
        x = 0
        while 0:
            if x > 10:
                break
            x += 1

    def falsy_8(self):
        x = 0
        while 0.0:
            if x > 10:
                break
            x += 1

    def falsy_9(self):
        x = 0
        while 0j:
            if x > 10:
                break
            x += 1

    def falsy_10(self):
        x = 0
        while None:
            if x > 10:
                break
            x += 1

    def falsy_11(self):
        x = 0
        while False:
            if x > 10:
                break
            x += 1
