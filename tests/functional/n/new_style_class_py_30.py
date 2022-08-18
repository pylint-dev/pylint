"""check builtin data descriptors such as mode and name attributes on a file are correctly handled

bug notified by Pierre Rouleau on 2005-04-24
"""


class File(file):  # pylint: disable=undefined-variable
    """ Testing new-style class inheritance from file"""
    def __init__(self, name, mode="r", buffering=-1, verbose=False):
        """Constructor"""
        self.was_modified = False
        self.verbose = verbose
        super(File, self).__init__(name, mode, buffering)  # [super-with-arguments]
        if self.verbose:
            print(f"File {self.name} is opened.  The mode is: {self.mode}")

    def write(self, a_string):
        """ Write a string to the file."""
        super(File, self).write(a_string)  # [super-with-arguments]
        self.was_modified = True

    def writelines(self, sequence):
        """ Write a sequence of strings to the file. """
        super(File, self).writelines(sequence)  # [super-with-arguments]
        self.was_modified = True

    def close(self):
        """Close the file."""
        if self.verbose:
            print(f"Closing file {self.name}")
        super(File, self).close()  # [super-with-arguments]
        self.was_modified = False
