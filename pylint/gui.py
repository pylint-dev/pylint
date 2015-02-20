# Copyright (c) 2003-2013 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""Tkinker gui for pylint"""
from __future__ import print_function

import os
import sys
import re
from threading import Thread

import six

from six.moves.tkinter import (
    Tk, Frame, Listbox, Entry, Label, Button, Scrollbar,
    Checkbutton, Radiobutton, IntVar, StringVar, PanedWindow,
    TOP, LEFT, RIGHT, BOTTOM, END, X, Y, BOTH, SUNKEN, W,
    HORIZONTAL, DISABLED, NORMAL, W,
)
from six.moves.tkinter_tkfiledialog import (
    askopenfilename, askdirectory,
)

import pylint.lint
from pylint.reporters.guireporter import GUIReporter

HOME = os.path.expanduser('~/')
HISTORY = '.pylint-gui-history'
COLORS = {'(I)':'green',
          '(C)':'blue', '(R)':'darkblue',
          '(W)':'black', '(E)':'darkred',
          '(F)':'red'}


def convert_to_string(msg):
    """make a string representation of a message"""
    module_object = msg.module
    if msg.obj:
        module_object += ".%s" % msg.obj
    return "(%s) %s [%d]: %s" % (msg.C, module_object, msg.line, msg.msg)

class BasicStream(object):
    '''
    used in gui reporter instead of writing to stdout, it is written to
    this stream and saved in contents
    '''
    def __init__(self, gui):
        """init"""
        self.curline = ""
        self.gui = gui
        self.contents = []
        self.outdict = {}
        self.currout = None
        self.next_title = None

    def write(self, text):
        """write text to the stream"""
        if re.match('^--+$', text.strip()) or re.match('^==+$', text.strip()):
            if self.currout:
                self.outdict[self.currout].remove(self.next_title)
                self.outdict[self.currout].pop()
            self.currout = self.next_title
            self.outdict[self.currout] = ['']

        if text.strip():
            self.next_title = text.strip()

        if text.startswith(os.linesep):
            self.contents.append('')
            if self.currout:
                self.outdict[self.currout].append('')
        self.contents[-1] += text.strip(os.linesep)
        if self.currout:
            self.outdict[self.currout][-1] += text.strip(os.linesep)
        if text.endswith(os.linesep) and text.strip():
            self.contents.append('')
            if self.currout:
                self.outdict[self.currout].append('')

    def fix_contents(self):
        """finalize what the contents of the dict should look like before output"""
        for item in self.outdict:
            num_empty = self.outdict[item].count('')
            for _ in range(num_empty):
                self.outdict[item].remove('')
            if self.outdict[item]:
                self.outdict[item].pop(0)

    def output_contents(self):
        """output contents of dict to the gui, and set the rating"""
        self.fix_contents()
        self.gui.tabs = self.outdict
        try:
            self.gui.rating.set(self.outdict['Global evaluation'][0])
        except KeyError:
            self.gui.rating.set('Error')
        self.gui.refresh_results_window()

        #reset stream variables for next run
        self.contents = []
        self.outdict = {}
        self.currout = None
        self.next_title = None


class LintGui(object):
    """Build and control a window to interact with pylint"""

    def __init__(self, root=None):
        """init"""
        self.root = root or Tk()
        self.root.title('Pylint')
        #reporter
        self.reporter = None
        #message queue for output from reporter
        self.msg_queue = six.moves.queue.Queue()
        self.msgs = []
        self.visible_msgs = []
        self.filenames = []
        self.rating = StringVar()
        self.tabs = {}
        self.report_stream = BasicStream(self)
        #gui objects
        self.lb_messages = None
        self.showhistory = None
        self.results = None
        self.btnRun = None
        self.information_box = None
        self.convention_box = None
        self.refactor_box = None
        self.warning_box = None
        self.error_box = None
        self.fatal_box = None
        self.txtModule = None
        self.status = None
        self.msg_type_dict = None
        self.init_gui()

    def init_gui(self):
        """init helper"""

        window = PanedWindow(self.root, orient="vertical")
        window.pack(side=TOP, fill=BOTH, expand=True)

        top_pane = Frame(window)
        window.add(top_pane)
        mid_pane = Frame(window)
        window.add(mid_pane)
        bottom_pane = Frame(window)
        window.add(bottom_pane)

        #setting up frames
        top_frame = Frame(top_pane)
        mid_frame = Frame(top_pane)
        history_frame = Frame(top_pane)
        radio_frame = Frame(mid_pane)
        rating_frame = Frame(mid_pane)
        res_frame = Frame(mid_pane)
        check_frame = Frame(bottom_pane)
        msg_frame = Frame(bottom_pane)
        btn_frame = Frame(bottom_pane)
        top_frame.pack(side=TOP, fill=X)
        mid_frame.pack(side=TOP, fill=X)
        history_frame.pack(side=TOP, fill=BOTH, expand=True)
        radio_frame.pack(side=TOP, fill=X)
        rating_frame.pack(side=TOP, fill=X)
        res_frame.pack(side=TOP, fill=BOTH, expand=True)
        check_frame.pack(side=TOP, fill=X)
        msg_frame.pack(side=TOP, fill=BOTH, expand=True)
        btn_frame.pack(side=TOP, fill=X)

        # Binding F5 application-wide to run lint
        self.root.bind('<F5>', self.run_lint)

        #Message ListBox
        rightscrollbar = Scrollbar(msg_frame)
        rightscrollbar.pack(side=RIGHT, fill=Y)
        bottomscrollbar = Scrollbar(msg_frame, orient=HORIZONTAL)
        bottomscrollbar.pack(side=BOTTOM, fill=X)
        self.lb_messages = Listbox(
            msg_frame,
            yscrollcommand=rightscrollbar.set,
            xscrollcommand=bottomscrollbar.set,
            bg="white")
        self.lb_messages.bind("<Double-Button-1>", self.show_sourcefile)
        self.lb_messages.pack(expand=True, fill=BOTH)
        rightscrollbar.config(command=self.lb_messages.yview)
        bottomscrollbar.config(command=self.lb_messages.xview)

        #History ListBoxes
        rightscrollbar2 = Scrollbar(history_frame)
        rightscrollbar2.pack(side=RIGHT, fill=Y)
        bottomscrollbar2 = Scrollbar(history_frame, orient=HORIZONTAL)
        bottomscrollbar2.pack(side=BOTTOM, fill=X)
        self.showhistory = Listbox(
            history_frame,
            yscrollcommand=rightscrollbar2.set,
            xscrollcommand=bottomscrollbar2.set,
            bg="white")
        self.showhistory.pack(expand=True, fill=BOTH)
        rightscrollbar2.config(command=self.showhistory.yview)
        bottomscrollbar2.config(command=self.showhistory.xview)
        self.showhistory.bind('<Double-Button-1>', self.select_recent_file)
        self.set_history_window()

        #status bar
        self.status = Label(self.root, text="", bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)

        #labelbl_ratingls
        lbl_rating_label = Label(rating_frame, text='Rating:')
        lbl_rating_label.pack(side=LEFT)
        lbl_rating = Label(rating_frame, textvariable=self.rating)
        lbl_rating.pack(side=LEFT)
        Label(mid_frame, text='Recently Used:').pack(side=LEFT)
        Label(top_frame, text='Module or package').pack(side=LEFT)

        #file textbox
        self.txt_module = Entry(top_frame, background='white')
        self.txt_module.bind('<Return>', self.run_lint)
        self.txt_module.pack(side=LEFT, expand=True, fill=X)

        #results box
        rightscrollbar = Scrollbar(res_frame)
        rightscrollbar.pack(side=RIGHT, fill=Y)
        bottomscrollbar = Scrollbar(res_frame, orient=HORIZONTAL)
        bottomscrollbar.pack(side=BOTTOM, fill=X)
        self.results = Listbox(
            res_frame,
            yscrollcommand=rightscrollbar.set,
            xscrollcommand=bottomscrollbar.set,
            bg="white", font="Courier")
        self.results.pack(expand=True, fill=BOTH, side=BOTTOM)
        rightscrollbar.config(command=self.results.yview)
        bottomscrollbar.config(command=self.results.xview)

        #buttons
        Button(top_frame, text='Open', command=self.file_open).pack(side=LEFT)
        Button(top_frame, text='Open Package',
               command=(lambda: self.file_open(package=True))).pack(side=LEFT)

        self.btnRun = Button(top_frame, text='Run', command=self.run_lint)
        self.btnRun.pack(side=LEFT)
        Button(btn_frame, text='Quit', command=self.quit).pack(side=BOTTOM)

        #radio buttons
        self.information_box = IntVar()
        self.convention_box = IntVar()
        self.refactor_box = IntVar()
        self.warning_box = IntVar()
        self.error_box = IntVar()
        self.fatal_box = IntVar()
        i = Checkbutton(check_frame, text="Information", fg=COLORS['(I)'],
                        variable=self.information_box, command=self.refresh_msg_window)
        c = Checkbutton(check_frame, text="Convention", fg=COLORS['(C)'],
                        variable=self.convention_box, command=self.refresh_msg_window)
        r = Checkbutton(check_frame, text="Refactor", fg=COLORS['(R)'],
                        variable=self.refactor_box, command=self.refresh_msg_window)
        w = Checkbutton(check_frame, text="Warning", fg=COLORS['(W)'],
                        variable=self.warning_box, command=self.refresh_msg_window)
        e = Checkbutton(check_frame, text="Error", fg=COLORS['(E)'],
                        variable=self.error_box, command=self.refresh_msg_window)
        f = Checkbutton(check_frame, text="Fatal", fg=COLORS['(F)'],
                        variable=self.fatal_box, command=self.refresh_msg_window)
        i.select()
        c.select()
        r.select()
        w.select()
        e.select()
        f.select()
        i.pack(side=LEFT)
        c.pack(side=LEFT)
        r.pack(side=LEFT)
        w.pack(side=LEFT)
        e.pack(side=LEFT)
        f.pack(side=LEFT)

        #check boxes
        self.box = StringVar()
        # XXX should be generated
        report = Radiobutton(
            radio_frame, text="Report", variable=self.box,
            value="Report", command=self.refresh_results_window)
        raw_met = Radiobutton(
            radio_frame, text="Raw metrics", variable=self.box,
            value="Raw metrics", command=self.refresh_results_window)
        dup = Radiobutton(
            radio_frame, text="Duplication", variable=self.box,
            value="Duplication", command=self.refresh_results_window)
        ext = Radiobutton(
            radio_frame, text="External dependencies",
            variable=self.box, value="External dependencies",
            command=self.refresh_results_window)
        stat = Radiobutton(
            radio_frame, text="Statistics by type",
            variable=self.box, value="Statistics by type",
            command=self.refresh_results_window)
        msg_cat = Radiobutton(
            radio_frame, text="Messages by category",
            variable=self.box, value="Messages by category",
            command=self.refresh_results_window)
        msg = Radiobutton(
            radio_frame, text="Messages", variable=self.box,
            value="Messages", command=self.refresh_results_window)
        source_file = Radiobutton(
            radio_frame, text="Source File", variable=self.box,
            value="Source File", command=self.refresh_results_window)
        report.select()
        report.grid(column=0, row=0, sticky=W)
        raw_met.grid(column=1, row=0, sticky=W)
        dup.grid(column=2, row=0, sticky=W)
        msg.grid(column=3, row=0, sticky=W)
        stat.grid(column=0, row=1, sticky=W)
        msg_cat.grid(column=1, row=1, sticky=W)
        ext.grid(column=2, row=1, sticky=W)
        source_file.grid(column=3, row=1, sticky=W)

        #dictionary for check boxes and associated error term
        self.msg_type_dict = {
            'I': lambda: self.information_box.get() == 1,
            'C': lambda: self.convention_box.get() == 1,
            'R': lambda: self.refactor_box.get() == 1,
            'E': lambda: self.error_box.get() == 1,
            'W': lambda: self.warning_box.get() == 1,
            'F': lambda: self.fatal_box.get() == 1
        }
        self.txt_module.focus_set()


    def select_recent_file(self, event): # pylint: disable=unused-argument
        """adds the selected file in the history listbox to the Module box"""
        if not self.showhistory.size():
            return

        selected = self.showhistory.curselection()
        item = self.showhistory.get(selected)
        #update module
        self.txt_module.delete(0, END)
        self.txt_module.insert(0, item)

    def refresh_msg_window(self):
        """refresh the message window with current output"""
        #clear the window
        self.lb_messages.delete(0, END)
        self.visible_msgs = []
        for msg in self.msgs:
            if self.msg_type_dict.get(msg.C)():
                self.visible_msgs.append(msg)
                msg_str = convert_to_string(msg)
                self.lb_messages.insert(END, msg_str)
                fg_color = COLORS.get(msg_str[:3], 'black')
                self.lb_messages.itemconfigure(END, fg=fg_color)

    def refresh_results_window(self):
        """refresh the results window with current output"""
        #clear the window
        self.results.delete(0, END)
        try:
            for res in self.tabs[self.box.get()]:
                self.results.insert(END, res)
        except KeyError:
            pass

    def process_incoming(self):
        """process the incoming messages from running pylint"""
        while self.msg_queue.qsize():
            try:
                msg = self.msg_queue.get(0)
                if msg == "DONE":
                    self.report_stream.output_contents()
                    return False

                #adding message to list of msgs
                self.msgs.append(msg)

                #displaying msg if message type is selected in check box
                if self.msg_type_dict.get(msg.C)():
                    self.visible_msgs.append(msg)
                    msg_str = convert_to_string(msg)
                    self.lb_messages.insert(END, msg_str)
                    fg_color = COLORS.get(msg_str[:3], 'black')
                    self.lb_messages.itemconfigure(END, fg=fg_color)

            except six.moves.queue.Empty:
                pass
        return True

    def periodic_call(self):
        """determine when to unlock the run button"""
        if self.process_incoming():
            self.root.after(100, self.periodic_call)
        else:
            #enabling button so it can be run again
            self.btnRun.config(state=NORMAL)

    def mainloop(self):
        """launch the mainloop of the application"""
        self.root.mainloop()

    def quit(self, _=None):
        """quit the application"""
        self.root.quit()

    def halt(self): # pylint: disable=no-self-use
        """program halt placeholder"""
        return

    def file_open(self, package=False, _=None):
        """launch a file browser"""
        if not package:
            filename = askopenfilename(parent=self.root,
                                       filetypes=[('pythonfiles', '*.py'),
                                                  ('allfiles', '*')],
                                       title='Select Module')
        else:
            filename = askdirectory(title="Select A Folder", mustexist=1)

        if filename == ():
            return

        self.txt_module.delete(0, END)
        self.txt_module.insert(0, filename)

    def update_filenames(self):
        """update the list of recent filenames"""
        filename = self.txt_module.get()
        if not filename:
            filename = os.getcwd()
        if filename+'\n' in self.filenames:
            index = self.filenames.index(filename+'\n')
            self.filenames.pop(index)

        #ensure only 10 most recent are stored
        if len(self.filenames) == 10:
            self.filenames.pop()
        self.filenames.insert(0, filename+'\n')

    def set_history_window(self):
        """update the history window with info from the history file"""
        #clear the window
        self.showhistory.delete(0, END)
        # keep the last 10 most recent files
        try:
            view_history = open(HOME+HISTORY, 'r')
            for hist in view_history.readlines():
                if not hist in self.filenames:
                    self.filenames.append(hist)
                self.showhistory.insert(END, hist.split('\n')[0])
            view_history.close()
        except IOError:
            # do nothing since history file will be created later
            return

    def run_lint(self, _=None):
        """launches pylint"""
        self.update_filenames()
        self.root.configure(cursor='watch')
        self.reporter = GUIReporter(self, output=self.report_stream)
        module = self.txt_module.get()
        if not module:
            module = os.getcwd()

        #cleaning up msgs and windows
        self.msgs = []
        self.visible_msgs = []
        self.lb_messages.delete(0, END)
        self.tabs = {}
        self.results.delete(0, END)
        self.btnRun.config(state=DISABLED)

        #setting up a worker thread to run pylint
        worker = Thread(target=lint_thread, args=(module, self.reporter, self,))
        self.periodic_call()
        worker.start()

        # Overwrite the .pylint-gui-history file with all the new recently added files
        # in order from filenames but only save last 10 files
        write_history = open(HOME+HISTORY, 'w')
        write_history.writelines(self.filenames)
        write_history.close()
        self.set_history_window()

        self.root.configure(cursor='')

    def show_sourcefile(self, event=None):  # pylint: disable=unused-argument
        selected = self.lb_messages.curselection()
        if not selected:
            return

        msg = self.visible_msgs[int(selected[0])]
        scroll = msg.line - 3
        if scroll < 0:
            scroll = 0

        self.tabs["Source File"] = open(msg.path, "r").readlines()
        self.box.set("Source File")
        self.refresh_results_window()
        self.results.yview(scroll)
        self.results.select_set(msg.line - 1)


def lint_thread(module, reporter, gui):
    """thread for pylint"""
    gui.status.text = "processing module(s)"
    pylint.lint.Run(args=[module], reporter=reporter, exit=False)
    gui.msg_queue.put("DONE")


def Run(args):
    """launch pylint gui from args"""
    if args:
        print('USAGE: pylint-gui\n launch a simple pylint gui using Tk')
        sys.exit(1)
    gui = LintGui()
    gui.mainloop()
    sys.exit(0)

if __name__ == '__main__':
    Run(sys.argv[1:])
