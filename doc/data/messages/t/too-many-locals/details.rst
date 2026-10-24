Each local variable adds a name and a value that a reader needs to keep track of.
A function with many local variables may be doing several unrelated tasks, making
it harder to understand and test each task independently.

Look for groups of variables that serve different purposes. In the example above,
creating children, distributing sweets, and calculating the cost are separate
tasks. Extracting those tasks into helper functions reduces the number of names
needed in each function. A class or named tuple can also group closely related
values, as shown in the corrected example.

The limit is configurable with :ref:`--max-locals <max-locals-option>`.
Exceeding it is a prompt to review the function's responsibilities, rather than
proof that the function is incorrect. If the variables are needed for a single,
cohesive task, consider adjusting the limit or disabling this message locally.
