"""this module produces a SyntaxError at execution time"""
# pylint: disable=using-constant-test
__revision__ = None

def run():
    """simple function"""
    if True:
        continue
    else:
        break

if __name__ == '__main__':
    run()

