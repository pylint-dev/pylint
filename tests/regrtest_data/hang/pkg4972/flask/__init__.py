import flask
import pkg4972.flask  # self-import necessary

class Fake(flask.Flask):
    pass

flask.Flask = Fake
