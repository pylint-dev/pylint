"""empty-comment test-case"""
# +1:[empty-comment]
A = 5  #
# +1:[empty-comment]
#
A = '#' + '1'
# +1:[empty-comment]
print(A)  #
print("A=", A)  # should not be an error#
# +1:[empty-comment]
A = "#pe\0ace#love#"  #
A = "peace#love"  # \0 peace'#'''' love#peace'''-'#love'-"peace#love"#
#######
