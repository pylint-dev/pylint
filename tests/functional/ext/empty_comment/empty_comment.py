"""empty-comment test-case"""
# +1:[empty-comment]
a = 5  #
# +1:[empty-comment]
#
a = '#' + '1'
# +1:[empty-comment]
print(a)  #
print("A=", a)  # should not be an error#
# +1:[empty-comment]
a = "#pe\0ace#love#"  #
a = "peace#love"  # \0 peace'#'''' love#peace'''-'#love'-"peace#love"#
#######
