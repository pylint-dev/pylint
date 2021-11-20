# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
import copy

class MyData:
    '''
    class docstring
    '''
    def __init__(self):
        self.data = {}

    def process(self):
        '''
        another method is responsible for putting "static_key"
        '''
        copy.copy(self.data['static_key'])
