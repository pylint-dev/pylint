from string import Template

menu = ("eggs", "spam", 42.4)

old_order = "%s and %s: %.2f ¤" % menu  # [consider-using-f-string]
beginner_order = menu[0] + " and " + menu[1] + ": " + str(menu[2]) + " ¤"
joined_order = " and ".join(menu[:2])
# +1: [consider-using-f-string]
format_order = "{} and {}: {:0.2f} ¤".format(menu[0], menu[1], menu[2])
# +1: [consider-using-f-string]
named_format_order = "{eggs} and {spam}: {price:0.2f} ¤".format(
    eggs=menu[0], spam=menu[1], price=menu[2]
)
template_order = Template("$eggs and $spam: $price ¤").substitute(
    eggs=menu[0], spam=menu[1], price=menu[2]
)
