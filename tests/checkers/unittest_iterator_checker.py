
import astroid
from astroid import nodes
from pylint import interfaces # Assuming interfaces is needed by MessageTest or similar
from pylint.testutils import CheckerTestCase, MessageTest
from pylint.checkers.looping_iterator_checker import RepeatedIteratorLoopChecker


class TestRepeatedIteratorLoopChecker(CheckerTestCase):
    """Tests for RepeatedIteratorLoopChecker."""

    CHECKER_CLASS = RepeatedIteratorLoopChecker
    checker:RepeatedIteratorLoopChecker

    # checker: RepeatedIteratorLoopChecker # This will be automatically set up

    def test_warns_for_generator_expression_global_scope(self):
        # Use astroid.parse() to get the Module node
        module_node = astroid.parse(
            """
            gen_ex = (x for x in range(3)) # Module level: module_node.body[0]
            for _i in range(2):            # Outer loop: module_node.body[1]
                for item in gen_ex:        # Inner loop: module_node.body[1].body[0]
                    print(item)
            """
        )
        outer_for_loop_node = module_node.body[1]
        if not isinstance(outer_for_loop_node, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected a For node, got {type(outer_for_loop_node)}")

        inner_for_loop_node = outer_for_loop_node.body[0]
        if not isinstance(inner_for_loop_node, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected an inner For node, got {type(inner_for_loop_node)}")

        expected_message_node = inner_for_loop_node.iter
        print("expected_message_node ", id(expected_message_node))

        with self.assertAddsMessages(
                MessageTest(
                    msg_id="looping-through-iterator",
                    node=expected_message_node,
                    args=("gen_ex",),
                    line=4,
                    col_offset=16,
                    end_line=4,  # Can be None
                    end_col_offset=22,  # Can be None
                    confidence=interfaces.HIGH,
                )
        ):
            #self.checker.visit_module(module_node) # Clears state
            self.walk(module_node)

    def test_warns_for_map_object_global_scope(self):

        module_node = astroid.parse(
                """
                map_obj = map(str, range(3))
                for _i in range(2):
                    for item in map_obj: # <-- Warning here
                        print(item)
                """
            )
        print("module node ", module_node.body[0])
        outer_for_loop_node = module_node.body[1]
        if not isinstance(outer_for_loop_node, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected a For node, got {type(outer_for_loop_node)}")

        inner_for_loop_node = outer_for_loop_node.body[0]
        if not isinstance(inner_for_loop_node, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected an inner For node, got {type(inner_for_loop_node)}")

        expected_message_node = inner_for_loop_node.iter
        with self.assertAddsMessages(
                MessageTest(msg_id="looping-through-iterator", node=expected_message_node, args=("map_obj",),
                            confidence=interfaces.HIGH), ignore_position=True
        ):
            self.walk(module_node)

    def test_warns_for_filter_object_function_scope(self):

        module_node = astroid.parse(
                    """
                    filter_obj = filter(None, range(3))
                    for _i in range(2):
                        for item in filter_obj: # <-- Warning here
                            print(item)
                    """)
        print("module node ", module_node.body[0])
        outer_for_loop_node = module_node.body[1]
        if not isinstance(outer_for_loop_node, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected a For node, got {type(outer_for_loop_node)}")

        inner_for_loop_node = outer_for_loop_node.body[0]
        if not isinstance(inner_for_loop_node, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected an inner For node, got {type(inner_for_loop_node)}")

        expected_message_node = inner_for_loop_node.iter
        with self.assertAddsMessages(
            MessageTest(msg_id="looping-through-iterator", node=expected_message_node, args=("filter_obj",), confidence=interfaces.HIGH), ignore_position=True
        ):
            self.walk(module_node)

    def test_warns_for_zip_object(self):

        module_node = astroid.parse(
                    """
                    zip_obj = zip(range(3), "abc")
                    for _i in range(2):
                        for item in zip_obj: # <-- Warning here
                            print(item)
                    """
                )
        print("module node ", module_node.body[0])
        outer_for_loop_node = module_node.body[1]
        if not isinstance(outer_for_loop_node, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected a For node, got {type(outer_for_loop_node)}")

        inner_for_loop_node = outer_for_loop_node.body[0]
        if not isinstance(inner_for_loop_node, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected an inner For node, got {type(inner_for_loop_node)}")

        expected_message_node = inner_for_loop_node.iter
        with self.assertAddsMessages(
                MessageTest(msg_id="looping-through-iterator", node=expected_message_node, args=("zip_obj",),
                            confidence=interfaces.HIGH), ignore_position=True
        ):
            self.walk(module_node)

    def test_warns_for_iter_object(self):
        module_node = astroid.parse(
                    """
                    my_list = [1, 2, 3]
                    iter_obj = iter(my_list)
                    for _i in range(2):
                        for item in iter_obj: # <-- Warning here
                            print(item)
                    """
                )
        print("module node ", module_node.body)
        outer_for_loop_node = module_node.body[2]
        if not isinstance(outer_for_loop_node, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected a For node, got {type(outer_for_loop_node)}")

        inner_for_loop_node = outer_for_loop_node.body[0]
        if not isinstance(inner_for_loop_node, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected an inner For node, got {type(inner_for_loop_node)}")

        expected_message_node = inner_for_loop_node.iter
        with self.assertAddsMessages(
                MessageTest(msg_id="looping-through-iterator", node=expected_message_node, args=("iter_obj",),
                            confidence=interfaces.HIGH), ignore_position=True
        ):
            self.walk(module_node)
    def test_warns_for_iter_callable_sentinel(self):

        module_node_1 = astroid.parse(
                    """
                    from itertools import count # line 1
                    counter = count(0) # line 2
                    def get_next(): return next(counter) # line 3
                    iter_call_obj = iter(get_next, 3) # line 4
                    for _i in range(2): # line 5
                        for item in iter_call_obj: # <-- Warning here on line 6 of this snippet, but MessageTest line is relative to `iter_call_obj` use
                            print(item)
                    """
                )
        print("module node 1", module_node_1.body[4])
        outer_for_loop_node_1 = module_node_1.body[4]
        if not isinstance(outer_for_loop_node_1, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected a For node, got {type(outer_for_loop_node_1)}")

        inner_for_loop_node_1 = outer_for_loop_node_1.body[0]
        if not isinstance(inner_for_loop_node_1, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected an inner For node, got {type(inner_for_loop_node_1)}")

        expected_message_node_1 = inner_for_loop_node_1.iter
        with self.assertAddsMessages(MessageTest(msg_id="looping-through-iterator", args=("iter_call_obj",),node=expected_message_node_1,
                                                 confidence=interfaces.HIGH), ignore_position=True):  # Line numbers start from 1 for the string content
            self.walk(module_node_1)

            # Correction for the line number above:
            # The MessageTest line is relative to the start of the *entire code snippet* passed to extract_node.
            # Snippet:
            # 1: from itertools import count
            # 2: counter = count(0)
            # 3: def get_next(): return next(counter)
            # 4: iter_call_obj = iter(get_next, 3)
            # 5: for _i in range(2):
            # 6:     for item in iter_call_obj: # <-- This is line 6
            # So MessageTest should be line=6 for the node `iter_call_obj`
        # Re-evaluating line for iter_callable_sentinel

    def test_warns_for_nested_consuming_producing_calls(self):
        # The code to be linted
        module_node = astroid.parse(
            """
            import string
            iter1 = map(lambda x: x, string.printable)
            iter2 = set(map(lambda x: x, string.printable))
            for i in range(5):
                for i1, i2 in list(zip(iter1, iter2)):
                    print(i1, i2)
            """
        )

        # To find the correct node, we must inspect the AST.
        # inner_for_loop_node -> For(iter=<Call...>)
        inner_for_loop_node = module_node.body[3].body[0]

        # The .iter attribute is the `list(zip(iter1, iter2))` call
        # Call(func=<Name.list...>, args=[<Call...>])
        list_call_node = inner_for_loop_node.iter

        # The argument to list() is the `zip(iter1, iter2)` call
        # Call(func=<Name.zip...>, args=[<Name.iter1>, <Name.iter2>])
        zip_call_node = list_call_node.args[0]

        # The first argument to zip() is the 'iter1' Name node we want to flag
        expected_message_node = zip_call_node.args[0]

        # Assert that ONE message is added on the 'iter1' node with the correct argument
        with self.assertAddsMessages(
                MessageTest(
                    msg_id="looping-through-iterator",
                    node=expected_message_node,
                    args=("iter1",),  # The name of the misused iterator
                    confidence=interfaces.HIGH,
                ),
                ignore_position=True,
        ):
            self.walk(module_node)


    def test_warns_for_reversed_object(self):
        module_node = astroid.parse(
                    """
                    my_tuple = (1, 2, 3)
                    rev_obj = reversed(my_tuple)
                    for _i in range(2):
                        for item in rev_obj: # <-- Warning here
                            print(item)
                    """
                )

        print("module node ", module_node.body)
        outer_for_loop_node = module_node.body[2]
        if not isinstance(outer_for_loop_node, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected a For node, got {type(outer_for_loop_node)}")

        inner_for_loop_node = outer_for_loop_node.body[0]
        if not isinstance(inner_for_loop_node, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected an inner For node, got {type(inner_for_loop_node)}")

        expected_message_node = inner_for_loop_node.iter
        with self.assertAddsMessages(
                MessageTest(msg_id="looping-through-iterator", node=expected_message_node, args=("rev_obj",),
                            confidence=interfaces.HIGH), ignore_position=True
        ):
            self.walk(module_node)


    def test_warns_iterator_defined_in_func_before_outer_loop(self):
        module_node =  astroid.parse(
                    """
                    def func():
                        gen_ex = (x for x in range(3))
                        for _i in range(2): # Outer loop
                            for item in gen_ex: # Inner loop <-- Warning here
                                print(item)
                    """
                )
        print("module node ", module_node.body[0].body[1].body[0])
        outer_for_loop_node = module_node.body[0].body[1]
        if not isinstance(outer_for_loop_node, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected a For node, got {type(outer_for_loop_node)}")

        inner_for_loop_node = outer_for_loop_node.body[0]
        if not isinstance(inner_for_loop_node, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected an inner For node, got {type(inner_for_loop_node)}")

        expected_message_node = inner_for_loop_node.iter
        with self.assertAddsMessages(
                MessageTest(msg_id="looping-through-iterator", node=expected_message_node, args=("gen_ex",),
                            confidence=interfaces.HIGH), ignore_position=True
        ):
            self.walk(module_node)


    def test_warns_multiple_levels_of_nesting(self):
        module_node = astroid.parse(
                    """
                    gen_ex = (x for x in range(3))
                    for _i in range(2):
                        for _j in range(2):
                            for item in gen_ex: # <-- Warning here
                                print(item)
                    """
                )
        print("module node ", module_node.body[1].body[0].body[0])
        outer_for_loop_node = module_node.body[1]
        if not isinstance(outer_for_loop_node, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected a For node, got {type(outer_for_loop_node)}")
        inner_for_loop_node = outer_for_loop_node.body[0].body[0]
        if not isinstance(inner_for_loop_node, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected an inner For node, got {type(inner_for_loop_node)}")

        expected_message_node = inner_for_loop_node.iter
        with self.assertAddsMessages(
                MessageTest(msg_id="looping-through-iterator", node=expected_message_node, args=("gen_ex",),
                            confidence=interfaces.HIGH), ignore_position=True
        ):
            self.walk(module_node)

    def test_nested_consumer_producer_calls(self):
        module_node = astroid.parse(
                    """
                    iter1 = map(lambda x: x, range(5))
                    for i in filter(lambda x: x % 2 == 0, map(lambda x: x, range(5))):
                        for j, k in zip(iter1, iter(range(5))):
                            print("i ", i, "j ", j, "k ", k)
                    """
                )
        print("module node ", module_node.body[1])
        outer_for_loop_node = module_node.body[1]
        if not isinstance(outer_for_loop_node, (nodes.For, nodes.AsyncFor)):
            raise AssertionError(f"Expected a For node, got {type(outer_for_loop_node)}")
        print("outer_for_loop_node ", outer_for_loop_node)
        print("outer_for_loop_node.body ", outer_for_loop_node.body[0])
        inner_for_loop_node = outer_for_loop_node.body[0]
        if not isinstance(inner_for_loop_node, (nodes.For, nodes.AsyncFor)):  # Check if it's a For node
            raise AssertionError(f"Expected an inner For node, got {type(inner_for_loop_node)}")

        expected_message_node = inner_for_loop_node.iter.args[0]
        with self.assertAddsMessages(
                MessageTest(msg_id="looping-through-iterator", node=expected_message_node, args=("iter1",),
                            confidence=interfaces.HIGH), ignore_position=True
        ):
            self.walk(module_node)

    def test_warns_for_iterator_stolen_by_nested_while_loop(self):
        """
        Tests for a true positive where an iterator is advanced by both an
        outer loop and a nested while loop, causing items to be skipped.
        """
        module_node = astroid.parse("""
        data_iterator = iter(range(20)) # Defined once, outside all loops
        for i in range(5):
            item = next(data_iterator)
            print(f"Outer loop got: {item}")
            while item < 10: # This nested while loop "steals" from the same iterator
                item = next(data_iterator) # <-- WARNING on 'data_iterator'
                print(f"  Inner loop got: {item}")
                if item % 3 == 0:
                    break
        """)
        print("module node ", module_node.body[1])
        outer_for_loop_node = module_node.body[1]
        if not isinstance(outer_for_loop_node, (nodes.For, nodes.AsyncFor)):
            raise AssertionError(f"Expected a For node, got {type(outer_for_loop_node)}")
        print("outer_for_loop_node ", outer_for_loop_node)
        print("outer_for_loop_node.body ", outer_for_loop_node.body[0])
        while_loop_node = outer_for_loop_node.body[2]
        if not isinstance(while_loop_node, nodes.While):  # Check if it's a For node
            raise AssertionError(f"Expected an inner For node, got {type(while_loop_node)}")
        assignment_node = while_loop_node.body[0]
        # 4. Get the right-hand side of the assignment (the 'next(...)' call)
        call_node = assignment_node.value
        # 5. Get the FIRST ARGUMENT to that call, which is 'data_iterator'
        expected_message_node = call_node.args[0]
        # The usage of `data_iterator` on line 8 is a violation.
        with self.assertAddsMessages(
                MessageTest(
                    msg_id="looping-through-iterator",
                    node = expected_message_node,
                    args=("data_iterator",),
                    confidence=interfaces.HIGH), ignore_position=True

                ):
            self.walk(module_node)

    # --- Negative Cases ---

    def test_no_warning_if_iterator_defined_inside_outer_loop(self):
        with self.assertNoMessages():
            self.walk( # CHANGED HERE
                astroid.parse(
                    """
                    def my_func():
                        for _i in range(2):
                            gen_ex_inner = (x for x in range(3)) # Defined inside outer loop
                            for item in gen_ex_inner:
                                print(item)
                    """
                )
            )

    def test_no_warning_for_list_comprehension_or_list_literal(self):
        with self.assertNoMessages():
            self.walk( # CHANGED HERE
                astroid.parse(
                    """
                    my_list_comp = [x for x in range(3)]
                    my_list_lit = [1, 2, 3]
                    for _i in range(2):
                        for item in my_list_comp:
                            print(item)
                        for item_lit in my_list_lit:
                            print(item_lit)
                    """
                )
            )

    def test_no_warning_if_iterator_converted_to_set(self):
        with self.assertNoMessages():
            self.walk( # CHANGED HERE
                astroid.parse(
                    """
                    gen_ex = (x for x in range(3))
                    list_from_gen = set(map(list(gen_ex))) # Converted to set after nested calls
                    for _i in range(2):
                        for item in list_from_gen:
                            print(item)
                    """
                )
            )

    def test_no_warning_for_single_loop(self):
        with self.assertNoMessages():
            self.walk( # CHANGED HERE
                astroid.parse(
                    """
                    gen_ex = (x for x in range(3))
                    for item in gen_ex:
                        print(item)
                    """
                )
            )

    def test_no_warning_for_range_object(self):
        with self.assertNoMessages():
            self.walk( # CHANGED HERE
                astroid.parse(
                    """
                    range_obj = range(3)
                    for _i in range(2):
                        for item in range_obj:
                            print(item)
                    """
                )
            )

    def test_no_warning_if_iterator_shadowed_in_outer_loop(self):
        with self.assertNoMessages():
            self.walk( # CHANGED HERE
                astroid.parse(
                    """
                    it = (x for x in range(3)) # Outer definition
                    for i in range(2):
                        it = [10, 20, 30] # Shadowed by a list
                        for item in it: # Uses the inner 'it' (list)
                            print(i, item)
                    """
                )
            )
            self.walk( # CHANGED HERE
                astroid.parse(
                    """
                    it = (x for x in range(3)) # Outer definition
                    for i in range(2):
                        it = (i + y for y in range(1)) # Shadowed by new generator
                        for item in it: # Uses the inner 'it'
                            print(i, item)
                    """
                )
            ) # Each call to self.walk should be in its own assertNoMessages/assertAddsMessages context
              # if they are meant to be independent assertions.
              # For multiple negative cases that are related, one might keep them in one self.walk if the AST setup is complex,
              # but generally, it's cleaner to have one `walk` per distinct test condition within its own context manager.
              # Let's separate them for clarity:

        with self.assertNoMessages():
             self.walk(
                astroid.parse(
                    """
                    it = (x for x in range(3)) # Outer definition
                    for i in range(2):
                        it = (i + y for y in range(1)) # Shadowed by new generator
                        for item in it: # Uses the inner 'it'
                            print(i, item)
                    """
                )
            )


    def test_no_warning_when_assign_target_is_not_simple_name(self):
        with self.assertNoMessages():
            self.walk( # CHANGED HERE
                astroid.parse(
                    """
                    class MyClass:
                        def __init__(self):
                            self.my_iter = (x for x in range(3))
                        def run(self):
                            for i in range(2):
                                for item in self.my_iter: # Accesses self.my_iter
                                    print(i, item)
                    """
                )
            )

    def test_no_warning_for_comprehension_directly_in_for_loop(self):
        with self.assertNoMessages():
            self.walk( # CHANGED HERE
                astroid.parse(
                    """
                    my_data = [1,2,3]
                    for i in range(2):
                        for item in (x*i for x in my_data): # New gen exp each time
                            print(item)
                    """
                )
            )

    def test_re_initialized_iterator_in_outer_loop_no_warn(self):
        code = """
        def test_re_initialized_iterator_in_outer_loop():
            for _i in range(2):
                my_iter = (x for x in range(3)) # Re-initialized here
                for item in my_iter:
                    print(item)
        """
        module_node = astroid.parse(code)
        # We expect NO messages here.
        with self.assertNoMessages():
            self.walk(module_node)

    def test_iterator_consumed_once_per_outer_loop_no_warn(self):
        code = """
        def test_iterator_consumed_once_per_outer_loop():
            outer_data = range(2)
            for outer_item in outer_data:
                my_gen = (x for x in range(outer_item, outer_item + 2)) # Generator created here
                for item in my_gen:
                    print(item)
        """
        module_node = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module_node)

    def test_iterator_name_reassigned_to_non_iterator_no_warn(self):
        code = """
        def test_iterator_name_reassigned_to_non_iterator():
            my_iter = map(str, range(3)) # Initial assignment of a tracked iterator
            my_iter = [1, 2, 3] # Reassigned to a list (non-iterator)
            for _i in range(2):
                for item in my_iter: # This is now a list, not a problematic iterator
                    print(item)
        """
        module_node = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module_node)

    def test_non_iterator_overwrites_iter_name_no_warn(self):
        code = """
        my_iter = map(str, range(3)) # Initial assignment of a tracked iterator
        my_iter = [1, 2, 3] # Reassigned to a list (non-iterator)
        for _i in range(2):
            for item in my_iter: # This is now a list, not a problematic iterator
                print(item)
        """
        module_node = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module_node)

    def test_iterator_used_inner_loop_called_outer_loop(self):
        code = """
            def get_numbers_iterator(start):
                return (x for x in range(start, start + 3))
            def test_iterator_from_function_in_outer_loop():
                for i in range(2):
                    numbers_iter = get_numbers_iterator(i) # New iterator each time
                    for num in numbers_iter:
                        print(num)
        """
        module_node = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module_node)

    # test_iterator_consumed_once_per_outer_loop.py
    def test_iterator_consumed_once_per_outer_loop(self):
        code = """
        outer_data = range(2)
        for outer_item in outer_data:
            my_gen = (x for x in range(outer_item, outer_item + 2))  # Generator created here
            # The inner loop consumes 'my_gen' once per iteration of the outer loop.
            # This is a valid pattern if a fresh generator is intended for each outer_item.
            for item in my_gen:
                print(item) """
        module_node = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module_node)

    # def test_iter_on_list(self):
    #     code = """
    #     data = [1, 2, 3]
    #     my_iter = iter(data) # 'iter' is in KNOWN_ITERATOR_PRODUCING_FUNCTIONS
    #     for _i in range(2):
    #         for item in my_iter: # This *will* be exhausted. Checker should flag.
    #             print(item)
    #     """
    #     module_node = astroid.parse(code)
    #     with self.assertNoMessages():
    #         self.walk(module_node)

    def test_iter_on_list_inner_loop(self):
        code = """
        data = [1, 2, 3]
        # 'iter' is in KNOWN_ITERATOR_PRODUCING_FUNCTIONS
        for _i in range(2):
            my_iter = iter(data)
            for item in my_iter: # This *will* be exhausted. Checker should flag.
                print(item)
        """
        module_node = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module_node)

    def test_list_call_in_loop(self):
        code = """
            for i in range(5):
                iterator1 = (i for i in [1, 2, 3])
                for j in list(iterator1):
                    print("i ", i, "j ", j)
        """
        module_node = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module_node)

    def test_nested_call_in_loop(self):
        code = """
            iter1 = map(lambda x: x, list(i for i in [1,2,3,4,5]))
            iter2 = set(map(lambda x: x, list(i for i in [1,2,3,4,5])))
            for i1, i2 in zip(iter1, iter2):
                for i in range(5):
                    print(i1, i2, i)
        """
        module_node = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module_node)

    def test_reassign_in_inner_loop(self):
        code = """
            iter1 = map(lambda x: x, range(5))
            for i in filter(lambda x: x % 2 == 0, map(lambda x: x, range(5))):
                iter1 = map(lambda x: x, range(5))
                for j, k in zip(iter1, iter(range(5))):
                    print("i ", i, "j ", j, "k ", k)
        """
        module_node = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module_node)

    # A test case for a valid pattern that was previously a false positive.
    # The iterator `my_iter` is safely re-initialized on every pass of the
    # outer loop, so its use in the nested loop is correct.

    def test_iterator_reinitialized_in_outer_loop_is_safe(self):
        code = """
        for i in range(2):
            data = [10, 20, 30, 40]
            my_iter = iter(data)  # Re-initialized on every outer loop pass
            for j in range(2):
                # This is a valid use, not a re-use of a stale iterator
                print(i, j, next(my_iter))
        """
        # This test MUST assert that no messages are added.
        with self.assertNoMessages():
            self.walk(astroid.parse(code))

    # A test case for a valid pattern with deep nesting that was previously a false positive.
    # The iterator `my_iter` is safely re-initialized on every pass of the
    # outer loop, so its use in the deeply nested loop is correct.

    def test_iterator_in_deeply_nested_loop_is_safe(self):
        code = """
        for i in range(2):  # Outer loop
            my_iter = iter([10, 20])  # Iterator defined inside the outer loop
            for j in range(2):         # First level of nesting
                print(f"j={j}")
                # The usage is in a second level of nesting
                for item in my_iter:
                    print(f"  i={i}, item={item}")
                # Crucially, my_iter is now exhausted for this pass of the outer loop.
        """
        # The old, buggy checker would incorrectly flag the usage of `my_iter`
        # on line 6. The new, correct checker should not.
        with self.assertNoMessages():
            self.walk(astroid.parse(code))

    def test_no_warning_for_iterator_reinitialized_in_loop(self):
        """
        Tests that no warning is raised for the valid pattern where an
        iterator is re-initialized on each pass of the outer loop.
        """
        code = """
        responses = {"a": [1, 2], "b": [3, 4]}
        for source, results in responses.items():
            # The iterator is created FRESH on each outer loop pass. This is safe.
            results_iter = iter(results)
            for i in range(2):
                item = next(results_iter)
                print(source, i, item)
        """
        with self.assertNoMessages():
            self.walk(astroid.parse(code))

    def test_no_warning_gen_producer_call_directly_in_loop(self):
        code = """
                my_list = [1, 2, 3]
                for _i in range(4):
                    for item in map(lambda x:x, my_list): # <-- Warning here
                        print(item)
                """
        with self.assertNoMessages():
            self.walk(astroid.parse(code))
