menu = ('eggs', 'spam')

order = "%s and %s" % menu # [consider-using-f-string]

new_order = "{1} and {0}".format(menu[0], menu[1]) # [consider-using-f-string]
