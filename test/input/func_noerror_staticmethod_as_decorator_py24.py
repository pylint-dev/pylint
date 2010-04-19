# pylint: disable=R0903
"""test staticmethod and classmethod as decorator"""

__revision__ = None

class StaticMethod1(object):
    """staticmethod test"""
    def __init__(self):
        pass

    @staticmethod
    def do_work():
        "Working..."
        
    @staticmethod
    def do_work_with_arg(job):
        "Working on something"
        print "Working on %s..." % job


class ClassMethod2(object):
    """classmethod test"""
    def __init__(self):
        pass

    @classmethod
    def do_work(cls):
        "Working..."
        
    @classmethod
    def do_work_with_arg(cls, job):
        "Working on something"
        print "Working on %s..." % job


