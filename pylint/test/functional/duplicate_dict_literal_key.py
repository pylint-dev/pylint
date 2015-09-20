"""Check multiple key definition"""
# pylint: disable=C0103

correct_dict = {
    'tea': 'for two',
    'two': 'for tea',
}

wrong_dict = {
    'tea': 'for two',   # [duplicate-key]
    'two': 'for tea',
    'tea': 'time',

}
