"""some pylint test utilities
"""
from glob import glob
from os.path import join, abspath, dirname, basename
from cStringIO import StringIO

from pylint.interfaces import IReporter
from pylint.reporters import BaseReporter

PREFIX = abspath(dirname(__file__))

def fix_path():
    import sys
    sys.path.insert(0, PREFIX)
    
def get_tests_info(prefix=None, suffix=None):
    pattern = '*'
    if prefix:
        pattern = prefix + pattern
    if suffix:
        pattern = pattern + suffix
    result = []
    for file in glob(join(PREFIX, "input", pattern)):
        infile = basename(file)
        outfile = join(PREFIX, "messages", infile.replace(suffix, '.txt'))
        result.append((infile, outfile))
        
    return result


TITLE_UNDERLINES = ['', '=', '-', '.']

class TestReporter(BaseReporter):
    """ store plain text messages 
    """
    
    __implements____ = IReporter
    
    def __init__(self):
        self.message_ids = {}
        self.reset()
        
    def reset(self):
        self.out = StringIO()
        self.messages = []
        
    def add_message(self, msg_id, location, msg):
        """manage message of different type and in the context of path """
        fpath, module, object, line = location
        self.message_ids[msg_id] = 1
        if object:
            object = ':%s' % object
        sigle = msg_id[0]
        self.messages.append('%s:%3s%s: %s' % (sigle, line, object, msg))

    def finalize(self):
        self.messages.sort()
        for msg in self.messages:
            print >>self.out, msg
        result = self.out.getvalue()
        self.reset()
        return result
    
    def display_results(self, layout):
        """ignore layouts"""

