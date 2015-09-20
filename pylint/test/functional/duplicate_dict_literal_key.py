"""Check multiple key definition"""
# pylint: disable=C0103

correct_dict = {
    'tea': 'for two',
    'two': 'for tea',
}

wrong_dict = {  # [duplicate-key]
    'tea': 'for two',
    'two': 'for tea',
    'tea': 'time',

}
