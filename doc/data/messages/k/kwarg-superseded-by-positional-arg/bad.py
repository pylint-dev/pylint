def print_name(name="Sarah", /, **kwds):
    print(name)


print_name(name="Jacob")  # [kwarg-superseded-by-positional-arg]
# Will print "Sarah"
