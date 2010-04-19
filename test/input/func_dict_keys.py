"""Check multiple key definition"""
#pylint: disable=C0103
__revision__ = 5

correct_dict = {
    'tea': 'for two',
    'two': 'for tea',
}

wrong_dict = {
    'tea': 'for two',
    'two': 'for tea',
    'tea': 'time',

}
