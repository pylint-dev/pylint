from argparse import _SubParsersAction, _AttributeHolder  # [import-private-name]

attr_holder = _AttributeHolder()

def add_sub_parser(sub_parsers: _SubParsersAction):
    sub_parsers.add_parser('my_subparser')
    # ... 
