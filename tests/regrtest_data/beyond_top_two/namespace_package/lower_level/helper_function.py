from ..plugin_api import top_message


def plugin_message(msg):
    return "plugin_message: %s" % top_message(msg)
