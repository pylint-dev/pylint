programs = {'do_something': lambda: print("Do something")}
program = input('Enter a program code to be used: ')
if programs.get(program):
    programs[program]()
