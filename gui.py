"""Tkinker gui for pylint"""

from Tkinter import Tk, Frame, Listbox, Entry, Label, Button, Scrollbar
from Tkinter import TOP, LEFT, RIGHT, BOTTOM, END, X, Y, BOTH
import os
import sys

if sys.platform.startswith('win'):
    PYLINT = 'pylint.bat'
else:
    PYLINT = 'pylint'

class LintGui:
    """Build and control a window to interact with pylint"""
    
    def __init__(self, root=None):
        self.root = root or Tk()
        self.root.title('Pylint')
        top_frame = Frame(self.root)
        res_frame = Frame(self.root)
        btn_frame = Frame(self.root)
        top_frame.pack(side=TOP, fill=X)
        res_frame.pack(side=TOP, fill=BOTH, expand=True)
        btn_frame.pack(side=TOP, fill=X)
        
        Label(top_frame, text='Module or package').pack(side=LEFT)
        self.txtModule = Entry(top_frame, background='white')
        self.txtModule.bind('<Return>', self.run_lint)
        self.txtModule.pack(side=LEFT, expand=True, fill=X)
        Button(top_frame, text='Run', command=self.run_lint).pack(side=LEFT)

        scrl = Scrollbar(res_frame)
        self.results = Listbox(res_frame,
                               background='white',
                               font='fixedsys',
                               selectmode='browse',
                               yscrollcommand=scrl.set)
        scrl.configure(command=self.results.yview)
        self.results.pack(side=LEFT, expand=True, fill=BOTH)
        scrl.pack(side=RIGHT, fill=Y)
        
        Button(btn_frame, text='Quit', command=self.quit).pack(side=BOTTOM)
        #self.root.bind('<ctrl-q>', self.quit)
        self.txtModule.focus_set()
        
    def mainloop(self):
        """launch the mainloop of the application"""
        self.root.mainloop()

    def quit(self, _=None):
        """quit the application"""
        self.root.quit()

    def run_lint(self, _=None):
        """launches pylint"""
        colors = {'W:':'red1', 'E:': 'red4',
                  'W:': 'red3', '**': 'navy'}
        
        self.root.configure(cursor='watch')
        self.results.focus_set()
        self.results.delete(0, END)
        self.results.update()
        module = self.txtModule.get()
        pout = os.popen('%s %s' % (PYLINT, module), 'r')
        for line in  pout.xreadlines():
            line = line.rstrip()
            self.results.insert(END, line)
            fg_color = colors.get(line[:2], 'black')
            self.results.itemconfigure(END, fg=fg_color)
            self.results.update()
        self.root.configure(cursor='')

def Run(args):
    """launch pylint gui from args"""
    if args:
        print 'USAGE: pylint-gui\n launch a simple pylint gui using Tk'
        return
    gui = LintGui()
    gui.mainloop()

if __name__ == '__main__':
    Run(sys.argv[1:]) 
